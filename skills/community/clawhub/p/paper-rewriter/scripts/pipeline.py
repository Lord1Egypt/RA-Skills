# -*- coding: utf-8 -*-
"""pipeline.py — 一键管线：自查 → 机械清理 → 深改任务简报 → 完整性守卫。

把 SKILL.md 的五步工作流合成一条命令（面向不想串多个脚本的用户/agent）：

    python scripts/pipeline.py draft.txt -o final.txt [--terms terms.txt] [--json]

产物:
    final.txt        机械清理后的文本（深度改写由 agent 按指南执行）
    (stdout)         管线报告：前后特征分、完整性判定、给 agent 的深改任务简报

--rewrite rewritten.txt: 已有人工/agent 改稿时，直接对改稿跑守卫+对比（跳过清理）。

退出码: 0 完成（完整性 FAIL 也算完成，看报告）| 2 用法/文件错误
--exit-verdict（v2.3.0 自动化集成档）: 0=干净 | 1=完整性 FAIL（与 verify 契约同义）
    | 3=风格特征中及以上（需深改）| 4=命中模型残留 | 2=用法/文件错误不变。
    pipeline 是唯一提供 1/3/4 全档判定的命令——CI/agent 门禁推荐用它。
"""

import argparse
import json
import re
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core
import transform as tf
import verify as vf

GUIDE = {"zh": "references/style_guide_zh.md", "en": "references/style_guide_en.md",
         "mix": "references/style_guide_zh.md + _en.md"}


def _read(path):
    try:
        return hxt_core.read_text(path)
    except OSError as e:
        print("错误: 无法读取 %s（%s）" % (path, e), file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="一键管线：自查→清理→深改简报→守卫")
    ap.add_argument("file", nargs="?", help="原稿（--batch 模式下传目录）")
    ap.add_argument("-o", "--output", help="清理结果落盘文件（建议必填）")
    ap.add_argument("--rewrite", help="已有改稿（提供则跳过机械清理，直接守卫+对比）")
    ap.add_argument("--terms", help="术语表文件（每行一个）；传 auto 则先自动生成"
                    "术语草稿（extract_terms 口径）再用——草稿未经人工确认，"
                    "守卫口径偏松，正式稿件建议人工过一遍后重跑")
    ap.add_argument("--lang", choices=["zh", "en", "mix", "auto"], default="auto")
    ap.add_argument("--profile", choices=["academic", "general"], default="academic",
                    help="academic=论文口径（默认）；general=非学术文本")
    ap.add_argument("--max-length-change", type=float, default=25.0)
    ap.add_argument("--suggestions", help="输出修订建议工作单（markdown 侧车）到此路径")
    ap.add_argument("--handoff", metavar="文件",
                    help="深改交接块（v3.8.0）：随管线一并生成句级改写指令单"
                         "（哪句→什么操作→守什么→怎么验，plan --handoff 同款），"
                         "执行改写的 agent 可直接照做——省去单独跑 plan 一步")
    ap.add_argument("--html", help="生成单文件 HTML 报告到此路径")
    ap.add_argument("--track", help="输出修订记录（.md+.json）到此路径基名")
    ap.add_argument("--batch", help="批量模式：目录内全部 .txt/.md/.docx/.pdf 逐个「清理+守卫」，汇总 CSV 输出到 stdout/此路径")
    ap.add_argument("--resume", action="store_true",
                    help="断点续传（v3.7.0，配 --batch）：跳过上次已完成的文件（进度存于目录下 "
                         ".pr_batch_state.json）；文件有变动（大小/修改时间）或上次失败的自动重跑。"
                         "不加本旗标则从头重建进度；请以与首跑相同的参数续跑"
                         "（进度只存结果不存参数，换参续跑会混口径）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--bundle", metavar="目录",
                    help="投稿自查包（v3.4.0）：在指定目录下生成带时间戳子目录，汇集"
                         "检测报告/修订记录/风格画像/统计一致性/术语一致性/完整性判定等各件")
    ap.add_argument("--raw-markdown", action="store_true",
                    help="对 .md 输入保留 markdown 标记扫描（缺省 v3.6.0 起自动剥离"
                         "结构后扫描正文；清理与完整性守卫始终基于原文）")
    ap.add_argument("--check-stats", action="store_true", dest="check_stats",
                    help="统计一致性阶段（v3.3.0）：对原稿跑 check_stats 三查"
                         "（百分比求和/分组 n/风格混用），结果进报告与 JSON；仅提示不改退出码")
    ap.add_argument("--pdf-min-confidence", choices=["高", "中", "低"], default="中",
                 help="PDF 最低置信度门闸（v3.3.0 引入；v3.8.0 起缺省=中）：低于阈值即拒收"
                      "并给处置建议——乱码形态的抽取不再混进报告与守卫；"
                      "--pdf-min-confidence 低 恢复「只标注不拦」旧行为")
    ap.add_argument("--exit-verdict", action="store_true",
                    help="自动化集成（CI/agent 门禁）：按判定设退出码——0=干净，"
                         "1=完整性 FAIL，3=风格特征中及以上，4=模型残留；"
                         "批量/单文件降级（覆盖不全）fail-closed=2。缺省恒 0")
    ap.add_argument("--ci", action="store_true", dest="exit_verdict",
                 help="CI 门禁模式：--exit-verdict 的短别名（机器退出码 0/1/3/4）")
    ap.add_argument("--deep", action="store_true",
                    help="深改档（v2.4.0）：清理阶段追加句式级确定性转换"
                         "（句首八股删除/排除式连接合并），操作进 --track 可审计。"
                         "--rewrite/--batch 下不生效")
    ap.add_argument("--step-timeout", type=float, default=hxt_core.SCAN_TIME_BUDGET,
                    help="单步墙钟预算秒（v2.5.0，缺省 120，须 >0）：清理与扫描各阶段"
                         "超时即干净报错（exit 2）并给拆分建议；分块扫描时为每块独立"
                         "预算（最坏 k 块 k 倍）；JSON 报告含各步耗时")
    ap.add_argument("--lexicon", metavar="文件",
                    help="外挂词表 JSON（v5.11.0）：同名键逐项追加——多 skill 共享同一外部词表；"
                         "透传扫描与清理")
    ap.add_argument("--summary-json", action="store_true",
                    help="单行 JSON 摘要（v5.20.0）：score 前后/guard/violations/残留——与 --summary 互斥，优先级更高")
    ap.add_argument("--summary", action="store_true",
                    help="一行速览：单文件=SUMMARY 行替换详细报告（分数前后/档位/守卫/违规数）；"
                         "--batch=逐文件 SUMMARY 行——agent/CI 快消费")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    # ── 批量模式：逐文件 清理+守卫 汇总 ──
    if getattr(args, "step_timeout", 0) is not None and args.step_timeout <= 0:
        hxt_core.fail("--step-timeout 必须为正数（收到 %s）" % args.step_timeout,
                      hint="秒数请 >0；缺省 120 秒")
    if getattr(args, "resume", False) and not args.batch:
        print("[提示] --resume 仅在 --batch 下生效（本次按普通单文件处理）",
              file=sys.stderr)
    if args.batch:
        import csv as _csv
        root = args.batch
        if not os.path.isdir(root):
            print("错误: --batch 需要目录（%s）" % root, file=sys.stderr)
            sys.exit(2)

        def _process_one(fp, time_budget):
            """单文件「读入→清理→守卫→前后扫描」（v3.7.0 收拢：首遍/重试遍共用）。
            返回行元组；失败抛 OSError/ValueError 由调用方处置。"""
            if fp.lower().endswith(".pdf"):
                o, _pm = hxt_core.read_text_ex(fp)
                if _pm and not hxt_core.pdf_confidence_ok(
                        _pm.get("confidence"), args.pdf_min_confidence):
                    raise hxt_core.pdf_gate_error(_pm.get("confidence"),
                                                  args.pdf_min_confidence,
                                                  notes=_pm.get("notes"))
                pdf_conf = _pm.get("confidence", "")
            else:
                o = hxt_core.read_text(fp)
                pdf_conf = ""
            if not o.strip():
                return (os.path.basename(fp), "-", "-", "空文件", "-")
            fx = tf.load_fixes(None, False, lexicon=getattr(args, "lexicon", None))
            n, _af = tf.apply_auto_fixes(o, fx)
            n, _rm = tf.drop_flagged_sentences(n)
            n, _nq = tf.normalize_quotes(n)
            v = vf.verify(o, n)
            deg = 0
            if max(len(o), len(n)) > 1_000_000:
                # v4.2.0 接降级（遗留缺口）：批量内超大文件不再整体失败——
                # 单块超时 2× 重试后标记降级继续；行内带标记，门禁拦停
                before = hxt_core.scan_chunked(o, time_budget=time_budget, degrade=True)
                after = hxt_core.scan_chunked(n, time_budget=time_budget, degrade=True)
                deg = len(before.get("degraded_chunks") or []) + \
                      len(after.get("degraded_chunks") or [])
                if deg:
                    print("[降级] %s：%d 块超时未评分（重试未恢复），该行仅覆盖部分正文"
                          % (os.path.basename(fp), deg), file=sys.stderr)
            else:
                before = hxt_core.scan(o, time_budget=time_budget,
                                       lexicon=getattr(args, "lexicon", None))
                after = hxt_core.scan(n, time_budget=time_budget,
                                      lexicon=getattr(args, "lexicon", None))
            conf_suffix = (" [置信度:%s]" % pdf_conf) if pdf_conf else ""
            deg_mark = " ⚠[降级:%d 块]" % deg if deg else ""
            if getattr(args, "track", None):
                batch_track[os.path.basename(fp)] = (_af, _rm, o)
            return (os.path.basename(fp),
                    "%d[%s]" % (before["score"], before["level"]),
                    "%d[%s]%s%s" % (after["score"], after["level"], conf_suffix, deg_mark),
                    "PASS" if v["ok"] else "FAIL(%d)" % len(v["violations"]),
                    "%+d%%" % v["stats"]["length_delta_pct"])

        rows_out = []
        batch_track = {}  # v5.3.0 --track：fn → (applied, removed, 原文)
        pending = []  # (fp, 行索引)——二遍重试队列（v2.5.0 stability 处方）
        gate_rej = 0  # 置信度门闸拒收计数（v3.8.0 批量熔断）
        done, state = hxt_core.batch_resume_prepare(root, args.resume, kind="pipeline", row_len=5)
        if args.resume and done:
            print("[续传] 跳过 %d 个已完成文件（进度 .pr_batch_state.json；"
                  "文件有变动或上次失败的会重跑）" % len(done), file=sys.stderr)
        n_state_fail = 0
        for fn in sorted(os.listdir(root)):
            if not fn.lower().endswith((".txt", ".md", ".docx", ".pdf")):
                continue
            fp = os.path.join(root, fn)
            if fn in done:
                rows_out.append(tuple(done[fn]))
                continue
            try:
                row = _process_one(fp, args.step_timeout)
                rows_out.append(row)
                if not hxt_core.batch_state_store(state, root, fn, fp, "done", row, kind="pipeline"):
                    n_state_fail += 1
            except hxt_core.PdfGateRejected as e:
                # 门闸拒收=确定性失败（v3.8.0）：不进重试队列，计入批级熔断
                gate_rej += 1
                rows_out.append((fn, "-", "-", "错误: %s" % str(e)[:200], "-"))
                hxt_core.batch_state_store(state, root, fn, fp, "error",
                                           rows_out[-1], kind="pipeline")
            except (OSError, ValueError):
                # 首遍失败不放弃：进二遍重试队列（超时/IO 抖动多为瞬时态）
                pending.append((fp, len(rows_out)))
                rows_out.append((fn, "-", "-", "错误（待重试）", "-"))
        retried = {}
        for fp, idx in pending:
            fn = rows_out[idx][0]
            try:
                row = _process_one(fp, hxt_core.SCAN_TIME_BUDGET * 2)
                rows_out[idx] = row
                retried[fn] = True
                if not hxt_core.batch_state_store(state, root, fn, fp, "done", row, kind="pipeline"):
                    n_state_fail += 1
            except hxt_core.PdfGateRejected as e:
                # 门闸拒收在重试遍出现（首遍瞬时失败+重试遭拒）：同样终态+熔断计数
                gate_rej += 1
                rows_out[idx] = (fn, "-", "-", "错误: %s" % str(e)[:200], "-")
                retried[fn] = False
                if not hxt_core.batch_state_store(state, root, fn, fp, "error", rows_out[idx], kind="pipeline"):
                    n_state_fail += 1
            except (OSError, ValueError) as e:
                rows_out[idx] = (fn, "-", "-", "错误: %s（已重试 1 次）" % str(e)[:200], "-")
                retried[fn] = False
                if not hxt_core.batch_state_store(state, root, fn, fp, "error", rows_out[idx], kind="pipeline"):
                    n_state_fail += 1
        if retried:
            n_ok = sum(1 for v in retried.values() if v)
            print("[重试] 二遍处理：%d 个失败文件重试，%d 个恢复" % (len(retried), n_ok),
                  file=sys.stderr)
        if n_state_fail:
            print("[提示] 断点进度写盘失败 %d 次（不影响本次结果，但本目录 --resume 不可用）"
                  % n_state_fail, file=sys.stderr)
        if gate_rej >= 3:
            # 批量熔断（v3.8.0）：同批多个 PDF 被拒=源头质量问题，不是逐文件偶发
            print("[熔断] %d 个 PDF 低于置信度门闸被拒——疑似这批 PDF 源头质量问题"
                  "（扫描件/嵌入字体缺失）。建议：检查来源，或统一导出 UTF-8 文本后重跑；"
                  "确要逐个强收可加 --pdf-min-confidence 低（输出需人工复核）" % gate_rej,
                  file=sys.stderr)

        if getattr(args, "track", None) and batch_track:
            # v5.3.0 批量修订记录落盘（transform 同款 build_revision_log，逐文件审计）
            os.makedirs(args.track, exist_ok=True)
            n_t = 0
            for fn_t, (_af, _rm, _o) in batch_track.items():
                try:
                    md_t, j_t = hxt_core.build_revision_log(_af, _rm, source=fn_t)
                    stem = os.path.splitext(fn_t)[0]
                    with open(os.path.join(args.track, "base_%s.md" % stem), "w",
                              encoding="utf-8") as f:
                        f.write(md_t + "\n")
                    with open(os.path.join(args.track, "base_%s.json" % stem), "w",
                              encoding="utf-8") as f:
                        json.dump(j_t, f, ensure_ascii=False, indent=1)
                    n_t += 1
                except OSError as e:
                    print("[提示] %s 修订记录写盘失败：%s" % (fn_t, e), file=sys.stderr)
            print("[批量修订记录] %d 个文件 → %s（transform 同款口径）"
                  % (n_t, args.track), file=sys.stderr)
        if getattr(args, "html", None):
            print("[提示] pipeline --batch 暂不生成 --html（可用 detect --batch --html）", file=sys.stderr)
        if getattr(args, "bundle", None):
            print("[提示] pipeline --batch 暂不生成 --bundle（可对关键单稿用 --bundle）", file=sys.stderr)
        if getattr(args, "check_stats", False):
            print("[提示] pipeline --batch 暂不跑 --check-stats（可用 check_stats --batch 目录）", file=sys.stderr)
        if getattr(args, "track", None):
            print("[提示] pipeline --batch 暂不生成 --track 修订记录", file=sys.stderr)
        if getattr(args, "suggestions", None):
            print("[提示] pipeline --batch 暂不生成 --suggestions 工作单", file=sys.stderr)
        if getattr(args, "deep", False):
            print("[提示] --deep 在 --batch 下暂不生效（逐文件请单跑 pipeline --deep）", file=sys.stderr)
        if getattr(args, "handoff", None):
            print("[提示] pipeline --batch 暂不生成 --handoff（可对重点单稿单跑）", file=sys.stderr)
        if getattr(args, "summary", False):
            # v5.19.0 批量一行速览：逐文件 SUMMARY 行（agent/CI 快消费）
            for row in rows_out:
                print("SUMMARY | %s | score %s→%s | guard %s | delta %s"
                      % (row[0], row[1], row[2].split("[")[0], row[3], row[4]))
        else:
            writer = _csv.writer(sys.stdout)
            writer.writerow(["file", "before", "after", "integrity", "len_delta"])
            for row in rows_out:
                writer.writerow(row)
        if args.output:
            if args.output.lower().endswith(".docx"):
                print("[提示] --batch 的 -o 是汇总 CSV（逐文件评分表），"
                      "不支持 docx 回写——改用 .csv 后缀", file=sys.stderr)
            try:
                with open(args.output, "w", encoding="utf-8", newline="") as cf:
                    cw = _csv.writer(cf)
                    cw.writerow(["file", "before", "after", "integrity", "len_delta"])
                    cw.writerows(rows_out)
                print("汇总 CSV 已写入 %s" % args.output, file=sys.stderr)
            except OSError as e:
                print("错误: 无法写入 %s（%s）" % (args.output, e), file=sys.stderr)
                sys.exit(2)
        if getattr(args, "exit_verdict", False):
            # 聚合最坏行：integrity FAIL 优先（1），其次残留（4）/分数档（3）
            worst = 0
            for row in rows_out:
                integrity, after = row[3], row[2]
                if "⚠[降级" in str(after):
                    # 降级 fail-closed（v4.2.0）：残缺扫描门禁不放行
                    worst = max(worst, 2)
                    continue
                if str(integrity).startswith("FAIL"):
                    worst = max(worst, 1)
                    continue
                if str(integrity).startswith("错误"):
                    # fail-closed：扫描不出的文件门禁不放行
                    worst = max(worst, 2)
                    continue
                m = re.match(r"^(\d+)", str(after))
                score = int(m.group(1)) if m else 0
                worst = max(worst, hxt_core.verdict_exit_code(score))
            sys.exit(worst)
        sys.exit(0)

    if not args.file:
        print("错误: 需要 原稿 参数（或使用 --batch 目录模式）", file=sys.stderr)
        sys.exit(2)
    pdf_meta = None
    if args.file.lower().endswith(".pdf"):
        try:
            orig, pdf_meta = hxt_core.read_text_ex(args.file)
            if pdf_meta and not hxt_core.pdf_confidence_ok(
                    pdf_meta.get("confidence"), args.pdf_min_confidence):
                raise hxt_core.pdf_gate_error(
                    pdf_meta.get("confidence"), args.pdf_min_confidence,
                    notes=pdf_meta.get("notes"))
        except (OSError, ValueError) as e:
            print("错误: %s" % e, file=sys.stderr)
            sys.exit(2)
    else:
        orig = _read(args.file)
    track_base = getattr(args, "track", None)
    deep_changed = set()  # rewrite 分支无 --deep 改写（防 UnboundLocal，v3.4.0 审计）
    profile = args.profile
    terms = None
    terms_note = ""
    if args.terms == "auto":
        import extract_terms as _et
        draft_path = (os.path.splitext(args.output or args.file)[0]
                      + ".terms.auto.txt")
        cands = _et.extract(orig, min_count=1)  # auto 档放宽到 1 次（去噪仍在），草稿供人工筛
        with open(draft_path, "w", encoding="utf-8") as _tf:
            for term, _n, _kind in cands:
                _tf.write(term + "\n")
        terms = vf.load_terms(draft_path)
        terms_note = ("术语表=自动草稿 %s（%d 条，未经人工确认）——正式稿件建议"
                      "人工过一遍后重跑" % (draft_path, len(cands)))
        print("[术语] " + terms_note, file=sys.stderr)
    elif args.terms:
        terms = vf.load_terms(args.terms)

    if args.rewrite:
        if getattr(args, "deep", False):
            print("[提示] --deep 在 --rewrite 下不生效（无清理阶段）", file=sys.stderr)
        if getattr(args, "handoff", None):
            print("[提示] --handoff 将基于你提供的改稿（--rewrite）生成指令单", file=sys.stderr)
        new = _read(args.rewrite)
        mode = "对已有改稿守卫"
        applied, removed = {}, []
        cleanup_s = None
    else:
        t_clean = time.monotonic()
        _deadline = t_clean + args.step_timeout
        fixes = tf.load_fixes(None, False, lexicon=getattr(args, "lexicon", None))
        new, applied = tf.apply_auto_fixes(orig, fixes)
        if time.monotonic() > _deadline:
            hxt_core.fail("清理阶段超时（预算 %g 秒）" % args.step_timeout,
                          hint="文件较大时请按章节拆分后分别处理，或调大 --step-timeout")
        new, removed = tf.drop_flagged_sentences(new)
        new, _ = tf.normalize_quotes(new)
        new, _nfw = tf.normalize_fullwidth_alnum(new)
        if _nfw:
            applied["全角字母数字归一"] = _nfw
        deep_ops = []
        deep_changed = set()
        if getattr(args, "deep", False):
            new, deep_ops, deep_changed = tf.deep_polish_ex(new)
        # 记账必须在 if 外（v3.7.0 评测员 P0：原错置 else 分支，deep_ops 恒空，
        # --deep 的操作从不进 --track/--bundle 修订记录=审计日志失真）
        for op in deep_ops:
            applied["深改档:%s" % op["op"]] = op["count"]
        if time.monotonic() > _deadline:
            hxt_core.fail("清理阶段超时（预算 %g 秒）" % args.step_timeout,
                          hint="文件较大时请按章节拆分后分别处理，或调大 --step-timeout")
        cleanup_s = time.monotonic() - t_clean
        mode = "机械清理" + ("+深改档" if deep_ops else "")
        if args.output:
            try:
                hxt_core.write_output(new, args.output, src_path=args.file)
            except OSError as e:
                print("错误: 无法写入 %s（%s）" % (args.output, e), file=sys.stderr)
                sys.exit(2)

    if max(len(orig), len(new)) > 1_000_000:
        def scan_fn(txt, **kw):
            # v3.9.0 降级机制：单块超时→2×重试→标记降级继续（degraded_chunks 透出）
            return hxt_core.scan_chunked(txt, degrade=True, **kw)
    else:
        scan_fn = hxt_core.scan
    # markdown 感知（v3.6.0）：风格扫描基于剥离结构后的正文；清理与 verify 仍用原文
    # （双口径：风格看散文，守卫看全文档）；--raw-markdown 保留原样
    _is_md = (args.file or "").lower().endswith((".md", ".markdown"))
    _md_struct = None
    scan_orig, scan_new = orig, new
    if _is_md and not getattr(args, "raw_markdown", False):
        scan_orig, _md_struct = hxt_core.strip_markdown(orig)
        scan_new, _ = hxt_core.strip_markdown(new)
    t_scan = time.monotonic()
    try:
        ro = scan_fn(scan_orig, profile=profile, time_budget=args.step_timeout)
        rn = scan_fn(scan_new, profile=profile, time_budget=args.step_timeout)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)
    scan_s = time.monotonic() - t_scan
    _deg = (ro.get("degraded_chunks") or []) + (rn.get("degraded_chunks") or [])
    for _d in _deg:
        print("[降级] 分块 %d–%d 字符超时未评分（2× 预算重试未恢复）——报告覆盖不全，"
              "缺失块特征可能漏检；建议按章节拆分后分次处理" % (_d["start"], _d["end"]),
              file=sys.stderr)
    t_ver = time.monotonic()
    vr = vf.verify(orig, new, terms, args.max_length_change,
                   expected_new=(deep_changed if args.deep else None))
    verify_s = time.monotonic() - t_ver

    lang = rn["lang"]
    top = sorted(rn["categories"].items(),
                 key=lambda kv: -kv[1]["count"] * kv[1]["weight"])[:5]
    brief = {
        "guide": GUIDE.get(lang, GUIDE["mix"]),
        "remaining_patterns": ["%s ×%d" % (v["label"], v["count"]) for _, v in top],
        "auto_fixes_applied": applied,
        "sentences_removed": len(removed),
        "next_action": ("agent 按 %s 对 %s 做深度改写（保护数字/引用/术语），"
                        "然后重跑本命令 --rewrite 改稿文件复核" % (GUIDE.get(lang, ""), args.output or "改稿"))
                      if rn["score"] >= 28 else
                      ("特征已低；按 %s 复核语义自然度即可" % GUIDE.get(lang, "指南")),
    }

    if args.suggestions:
        guide = {"zh": "references/style_guide_zh.md",
                 "en": "references/style_guide_en.md"}.get(lang,
                                                           "references/style_guide_zh.md")
        try:
            with open(args.suggestions, "w", encoding="utf-8") as f:
                f.write(hxt_core.build_suggestions(orig, rn, guide))
        except OSError as e:
            print("错误: 无法写入 %s（%s）" % (args.suggestions, e), file=sys.stderr)
            sys.exit(2)

    stats_issues = None
    if getattr(args, "check_stats", False):
        import check_stats as _cst
        _g, stats_issues = _cst.run_checks(scan_orig)

    report = {
        "mode": mode,
        "before": {"score": ro["score"], "level": ro["level"], "critical": ro["critical_hit"]},
        "after": {"score": rn["score"], "level": rn["level"], "critical": rn["critical_hit"]},
        "verify": vr,
        "agent_brief": brief,
        # 降级 fail-closed（v3.9.0）：分块超时未评分=扫描不完整，CI 门禁不放行
        "exit_verdict": (2 if ((ro.get("degraded_chunks") or [])
                               + (rn.get("degraded_chunks") or []))
                         else hxt_core.verdict_exit_code(rn["score"], rn["critical_hit"],
                                                         verify_ok=vr["ok"])),
        "hints": hxt_core.build_hints(new, rn, profile=profile),
        "terms_note": terms_note,
        "md_struct": _md_struct,
        # 降级信息（v3.9.0 审计 P0：赋值必须在 report 字面量之后，否则
        # 部分降级场景 UnboundLocalError 崩溃——降级以崩溃形式复活）
        **({"degraded": {"chunks": _deg,
                         "note": "部分分块超时未评分（已重试）；覆盖不完整，"
                                 "勿当完整报告使用"}} if _deg else {}),
        "stats_consistency": (
            {"total": len(stats_issues), "issues": stats_issues,
             "note": "内部一致性启发式，非统计审查；以原始数据为准"}
            if stats_issues is not None else None),
        "pdf_meta": pdf_meta,
        "timings": ({"cleanup_s": round(cleanup_s, 2), "scan_s": round(scan_s, 2),
                     "verify_s": round(verify_s, 2),
                     "total_s": round(cleanup_s + scan_s + verify_s, 2)}
                    if cleanup_s is not None else
                    {"cleanup_s": None, "scan_s": round(scan_s, 2),
                     "verify_s": round(verify_s, 2),
                     "total_s": round(scan_s + verify_s, 2)}),
        "honest_note": "本地启发式风格特征评分，非任何官方检测分数",
    }

    if track_base:
        md, jobj = hxt_core.build_revision_log(applied, removed, source=args.file)
        try:
            with open(track_base + ".md", "w", encoding="utf-8") as f:
                f.write(md + "\n")
            with open(track_base + ".json", "w", encoding="utf-8") as f:
                json.dump(jobj, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print("错误: 无法写入修订记录（%s）" % e, file=sys.stderr)
            sys.exit(2)
        print("修订记录: " + track_base + ".md/.json", file=sys.stderr)

    if getattr(args, "bundle", None):
        try:
            import datetime as _dt
            import check_stats as _cst
            import check_terms as _ctm
            import reporter as _rep
            broot = args.bundle
            os.makedirs(broot, exist_ok=True)
            stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            bdir = os.path.join(broot, "自查包_" + stamp)
            if os.path.exists(bdir):  # 同秒重跑：后缀避让，不静默覆盖
                k = 2
                while os.path.exists(bdir + "_%d" % k):
                    k += 1
                bdir += "_%d" % k
            os.makedirs(bdir, exist_ok=True)
            # ⓪ 写入清单（v5.4.0 权限自证：本次运行全部写入路径的实测工件）
            _manifest = {"generated_by": "pipeline --bundle",
                         "note": "本次运行全部写入路径实测清单（权限自证工件）",
                         "writes": []}

            def _reg(path, kind, flag):
                _manifest["writes"].append({"path": path, "kind": kind, "flag": flag})

            _reg(os.path.join(bdir, "00_写入清单.json"), "manifest", "--bundle")

            # ① 检测报告（改稿口径）
            prof = hxt_core.style_profile(new)
            _reg(os.path.join(bdir, "01_风格自查报告.html"), "风格自查报告（改稿口径）", "--bundle")
            with open(os.path.join(bdir, "01_风格自查报告.html"), "w", encoding="utf-8") as f:
                f.write(_rep.render_style_profile(prof, os.path.basename(str(args.file or "stdin"))))
            # ② 修订记录
            md, jobj = hxt_core.build_revision_log(applied, removed, source=args.file)
            _reg(os.path.join(bdir, "02_修订记录.md"), "修订记录 markdown", "--bundle")
            with open(os.path.join(bdir, "02_修订记录.md"), "w", encoding="utf-8") as f:
                f.write(md + "\n")
            _reg(os.path.join(bdir, "02_修订记录.json"), "修订记录 JSON", "--bundle")
            with open(os.path.join(bdir, "02_修订记录.json"), "w", encoding="utf-8") as f:
                json.dump(jobj, f, ensure_ascii=False, indent=1)
            # ③ 风格画像差值
            _reg(os.path.join(bdir, "03_风格画像对比.md"), "风格画像对比", "--bundle")
            with open(os.path.join(bdir, "03_风格画像对比.md"), "w", encoding="utf-8") as f:
                f.write(_render_profile_compare(orig, new))
            # ④ 统计一致性（原稿）
            _g, st_issues = _cst.run_checks(orig)
            _reg(os.path.join(bdir, "04_统计一致性.md"), "统计一致性", "--bundle")
            with open(os.path.join(bdir, "04_统计一致性.md"), "w", encoding="utf-8") as f:
                f.write(_cst.build_report(_g, st_issues, source=args.file) + "\n")
            # ⑤ 术语一致性（原稿）
            t_issues = _ctm.find_group_inconsistencies(
                orig, [dict(g) for g in _ctm._TERM_GROUPS])
            t_lines = ["# 术语一致性检查", ""]
            if not t_issues:
                t_lines.append("未发现术语不一致。")
            else:
                for x in t_issues:
                    vs = " / ".join("%s(%d)" % (v, c) for v, c in sorted(
                        x["variants"].items(), key=lambda kv: -kv[1]))
                    t_lines.append("- [%s] %s → 建议「%s」" % (
                        x.get("pack", ""), vs, x.get("suggestion", "")))
            _reg(os.path.join(bdir, "05_术语一致性.md"), "术语一致性", "--bundle")
            with open(os.path.join(bdir, "05_术语一致性.md"), "w", encoding="utf-8") as f:
                f.write("\n".join(t_lines) + "\n")
            # ⑥ 完整性判定
            _reg(os.path.join(bdir, "06_完整性判定.json"), "完整性判定 JSON", "--bundle")
            with open(os.path.join(bdir, "06_完整性判定.json"), "w", encoding="utf-8") as f:
                json.dump(vr, f, ensure_ascii=False, indent=1)
            # ⑦ 问题台账（v3.5.0 模块移植）：逐类 resolved/partial/unresolved + 预算行
            _g0, st_b = _cst.run_checks(orig)
            t_b = _ctm.find_group_inconsistencies(
                orig, [dict(g) for g in _ctm._TERM_GROUPS])
            led = []
            for cid, c in (ro.get("categories") or {}).items():
                before = c.get("count", 0)
                if before <= 0:
                    continue
                after = (rn.get("categories") or {}).get(cid, {}).get("count", 0)
                status = ("resolved" if after == 0 else
                          "partially answered" if after < before else "unresolved")
                led.append((cid, c.get("label", ""), before, after, status))
            _g2, st_after = _cst.run_checks(new)
            led.append(("stats_consistency", "统计一致性（求和/分组 n/风格）",
                        len(st_b), len(st_after),
                        "resolved" if not st_after else
                        ("partially answered" if len(st_after) < len(st_b) else "unresolved")))
            t_after = _ctm.find_group_inconsistencies(
                new, [dict(g) for g in _ctm._TERM_GROUPS])
            led.append(("terms_consistency", "术语一致性（变体组）",
                        len(t_b), len(t_after),
                        "resolved" if not t_after else
                        ("partially answered" if len(t_after) < len(t_b) else "unresolved")))
            _reg(os.path.join(bdir, "07_问题台账.md"), "问题台账", "--bundle")
            with open(os.path.join(bdir, "07_问题台账.md"), "w", encoding="utf-8") as f:
                f.write("# 问题台账（finding ledger）\n\n")
                f.write("> 逐项标记 answered / partially answered / unresolved；"
                        "预算台账：已用轮次 1（本次 pipeline），剩余轮次由作者决定"
                        "——再跑一轮本命令即更新。\n\n")
                f.write("| 问题 | 说明 | 改前 | 改后 | 状态 |\n|---|---|---|---|---|\n")
                for cid, label, b, a, st in led:
                    f.write("| %s | %s | %d | %d | %s |\n" % (cid, label, b, a, st))
            # ⑧ 体检报告 dashboard（v5.0.0 旗舰：单页交互聚合——各件数据一页读）
            try:
                _reg(os.path.join(bdir, "08_体检报告.html"), "体检报告 dashboard", "--bundle")
                with open(os.path.join(bdir, "08_体检报告.html"), "w", encoding="utf-8") as f:
                    f.write(_rep.render_dashboard(
                        ro, rn, vr, prof, st_issues, t_issues, led,
                        meta=os.path.basename(str(args.file or "stdin"))))
                print("[体检报告] 08_体检报告.html 已并入自查包", file=sys.stderr)
            except Exception as e:
                print("[提示] 体检报告写盘失败（不影响其余件）：%s" % str(e)[:80], file=sys.stderr)
            # ⑨ 深改指令单（v5.3.0：08 行动清单②段直连——bundle 自包含「改哪里+怎么改」）
            try:
                import plan as _plan_mod
                _src9 = orig
                if (args.file or "").lower().endswith((".md", ".markdown")) and not getattr(args, "raw_markdown", False):
                    _src9 = hxt_core.strip_markdown(orig)[0]
                _top, _secs, _full = _plan_mod.build_queue(
                    _src9, lang=None, profile=profile, source_ext=".txt")
                _hd = _plan_mod.build_handoff(_top, _secs, source=str(args.file or "stdin"),
                                              lang=_full.get("lang"))
                _reg(os.path.join(bdir, "09_深改指令单.md"), "深改指令单", "--bundle")
                with open(os.path.join(bdir, "09_深改指令单.md"), "w", encoding="utf-8") as f:
                    f.write(_hd + "\n")
                print("[深改指令单] 09_深改指令单.md 已并入自查包（%d 句）" % len(_top),
                      file=sys.stderr)
            except ValueError as e:
                print("[提示] 深改指令单跳过（%s）" % str(e)[:80], file=sys.stderr)
            except OSError as e:
                print("[提示] 深改指令单写盘失败（不影响其余件）：%s" % e, file=sys.stderr)
            # ⑩ 前后对照（v5.6.0：体检报告行动清单的复核件——render_compare 直出）
            try:
                _reg(os.path.join(bdir, "10_前后对照.html"), "前后对照", "--bundle")
                with open(os.path.join(bdir, "10_前后对照.html"), "w", encoding="utf-8") as f:
                    f.write(_rep.render_compare(orig, new, ro, rn, vr))
                print("[前后对照] 10_前后对照.html 已并入自查包", file=sys.stderr)
            except Exception as e:
                print("[提示] 前后对照写盘失败（不影响其余件）：%s" % str(e)[:80], file=sys.stderr)
            # ⑪ 守卫处方（v5.8.0：verify 处方报告随包——单页可打印，FAIL 带三步处方）
            try:
                import verify as _vf
                _rem11 = _vf.build_remedies(orig, vr)
                _reg(os.path.join(bdir, "11_守卫处方.html"), "守卫处方报告", "--bundle")
                with open(os.path.join(bdir, "11_守卫处方.html"), "w", encoding="utf-8") as f:
                    f.write(_vf.render_report_html(vr, _rem11,
                                                   terms_flag=bool(getattr(args, "terms", None))))
                print("[守卫处方] 11_守卫处方.html 已并入自查包", file=sys.stderr)
            except Exception as e:
                print("[提示] 守卫处方写盘失败（不影响其余件）：%s" % str(e)[:80], file=sys.stderr)
            _reg(os.path.join(bdir, "README.txt"), "包说明", "--bundle")
            with open(os.path.join(bdir, "README.txt"), "w", encoding="utf-8") as f:
                f.write(
                    "投稿自查包（paper-rewriter v%s，模式=%s）\n生成时间: %s\n原稿: %s\n\n"
                    "各件说明：01 改稿风格自查报告（本地启发式口径，非任何官方检测）；"
                    "02 机械清理修订记录（可审计；--rewrite 模式下本件为空属正常）；"
                    "03 前后风格画像对比；04 统计一致性（以原始数据为准）；"
                    "05 术语一致性；06 完整性守卫判定（ok=true 才算过）；07 问题台账（逐项标记处理状态）；"
                    "08 体检报告（单页聚合——分数卡/命中行号/依据/台账）；09 深改指令单（逐句改哪里怎么改）；"
                    "10 前后对照（L 行号锚）；11 守卫处方（单页修复处方，FAIL 时照修复三步执行）；"
                    "00 写入清单（本次全部写入路径实测）。\n"
                    % (hxt_core.__version__, mode,
                       _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                       str(args.file)))
            _mp = os.path.join(bdir, "00_写入清单.json")
            try:
                with open(_mp, "w", encoding="utf-8") as f:
                    json.dump(_manifest, f, ensure_ascii=False, indent=1)
            except OSError:
                pass
            print("投稿自查包: %s（00-11 共 12 件）" % bdir, file=sys.stderr)
        except Exception as e:  # 自查包是辅助产物：失败降级为警告，主报告照常输出
            print("[提示] 自查包生成失败（%s），主流程结果不受影响" % str(e)[:80],
                  file=sys.stderr)

    if getattr(args, "handoff", None):
        # 深改交接块（v3.8.0）：一句命令产出「清理+守卫+逐句指令单」，
        # 深改不再需要单独跑 plan——usability 处方。
        # v3.8.0 评测员 P1：指令单基于清理稿/改稿（new）而非原稿——深改的
        # 操作对象是 new，基于 orig 会列出已被清理掉的句（与 best_practices
        # 「对清理稿排计划」口径一致）
        _note_dest = sys.stderr if args.json else sys.stdout
        import plan as _plan
        try:
            _top, _secs, _full = _plan.build_queue(
                new, lang=None if args.lang == "auto" else args.lang,
                profile=args.profile,
                source_ext=".txt")
            _md = _plan.build_handoff(_top, _secs,
                                      source=args.rewrite or args.file,
                                      lang=_full.get("lang"))
            with open(args.handoff, "w", encoding="utf-8") as hf:
                hf.write(_md + "\n")
            _base = "改稿" if args.rewrite else "清理稿"
            print("深改交接块: %s（基于%s，%d 句 P0 队列，执行改写的 agent 可直接照做）"
                  % (args.handoff, _base, len(_top)), file=_note_dest)
        except ValueError as e:
            print("[提示] 交接块未生成（%s）" % str(e)[:140], file=sys.stderr)
        except OSError as e:
            print("错误: 无法写入 %s（%s）" % (args.handoff, e), file=sys.stderr)
            sys.exit(2)

    if getattr(args, "summary_json", False):
        print(json.dumps({"mode": mode,
                          "before": {"score": ro["score"], "level": ro["level"]},
                          "after": {"score": rn["score"], "level": rn["level"]},
                          "guard": "PASS" if vr["ok"] else "FAIL",
                          "violations": len(vr.get("violations") or []),
                          "warnings": len(vr.get("warnings") or []),
                          "residue": bool(rn.get("critical_hit")),
                          "exit_verdict": report.get("exit_verdict")},
                         ensure_ascii=False))
        if args.exit_verdict:
            sys.exit(report["exit_verdict"])
        sys.exit(0)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if args.exit_verdict:
            sys.exit(report["exit_verdict"])
        sys.exit(0)
    else:
        print("=" * 62)
        print("一键管线报告（%s）" % mode)
        print("=" * 62)
        if _deg:
            print("⚠ 降级：%d 块超时未评分（已重试）——覆盖不完整，勿当完整报告使用"
                  % len(_deg))
        if getattr(args, "summary", False):
            # v5.16.0 一行速览：agent/CI 快消费（详细报告照常在各文件/JSON）
            _bad = len(vr.get("violations") or [])
            _warn = len(vr.get("warnings") or [])
            print("SUMMARY | score %d[%s]→%d[%s] | guard %s | violations %d | warnings %d | residue %s"
                  % (ro["score"], ro["level"], rn["score"], rn["level"],
                     "PASS" if vr["ok"] else "FAIL", _bad, _warn,
                     "yes" if rn["critical_hit"] else "no"))
        else:
            print("风格特征分: %d [%s] → %d [%s]%s" % (
                ro["score"], ro["level"], rn["score"], rn["level"],
                "  ⚠ 仍含模型残留" if rn["critical_hit"] else ""))
            print("完整性守卫: %s" % ("PASS ✓" if vr["ok"] else "FAIL ✗"))
        _remedies = vf.build_remedies(orig, vr)
        for v in vr["violations"]:
            print("  ✗ [%s] %s" % (v["check"], v["detail"]))
            rem = next((x for x in _remedies if x["check"] == v["check"]
                        and not x.get("warning")), None)
            if rem:
                for ctx in rem.get("context", [])[:1]:
                    print("      原句锚点: %s" % ctx)
                print("      怎么修: %s" % rem["remedy"])
        for w in vr["warnings"]:
            print("  ⚠ [%s] %s" % (w["check"], w["detail"]))
        print("深改任务简报:")
        print("  指南: " + brief["guide"])
        for p in brief["remaining_patterns"]:
            print("  · 剩余特征: " + p)
        print("  下一步: " + brief["next_action"])
        if getattr(args, "suggestions", None):
            print("修订建议工作单: " + args.suggestions)
        if getattr(args, "html", None):
            import reporter
            try:
                with open(args.html, "w", encoding="utf-8") as hf:
                    hf.write(reporter.render_pipeline(orig, new, ro, rn, vr, brief,
                                                      chunked=getattr(rn, "get", lambda k: None)("chunked")))
            except OSError as e:
                print("错误: 无法写入 %s（%s）" % (args.html, e), file=sys.stderr)
                sys.exit(2)
            print("HTML 报告: " + args.html)
        sc = report.get("stats_consistency")
        if sc is not None:
            print("")
            if sc["total"]:
                print("统计一致性：%d 项" % sc["total"])
                for x in sc["issues"]:
                    print("  [%s] %s" % (x["kind"], x["detail"]))
            else:
                print("统计一致性：未发现问题")
            print("口径: " + sc["note"])
        tm = report["timings"]
        clean_disp = "—" if tm["cleanup_s"] is None else "%.1fs" % tm["cleanup_s"]
        print("耗时: 清理 %s | 扫描 %.1fs | 守卫 %.1fs（合计 %.1fs，单步预算 %g 秒）"
              % (clean_disp, tm["scan_s"], tm["verify_s"], tm["total_s"],
                 args.step_timeout))
        if report.get("md_struct"):
            m = report["md_struct"]
            print("Markdown 结构: 标题 %d · 表格行 %d · 代码块 %d（已剥离，不计风格分；守卫仍基于原文）"
                  % (m["headings"], m["table_rows"], m["code_blocks"]))
        if report["hints"]:
            print("处置提示:")
            for h in report["hints"]:
                print("  → " + h)
        if rn["stats"].get("uniform_flag"):
            print("节奏规整旗: 句长高度集中（统计倾向信号，规整文体也可能触发，非检测结论）")
        if pdf_meta:
            print("PDF 抽取置信度: %s" % pdf_meta["confidence"])
            for note in pdf_meta["notes"]:
                print("  ⚠ " + note)
        print("口径: " + report["honest_note"])
    if args.exit_verdict:
        sys.exit(report["exit_verdict"])
    sys.exit(0)


def _render_profile_compare(orig_text, new_text):
    """--bundle 用：前后画像差值的轻量 markdown（复用 stylecheck 的渲染器）。"""
    import stylecheck as _sc
    pa, pb = hxt_core.style_profile(orig_text), hxt_core.style_profile(new_text)
    return _sc.render_compare(pa, pb, "(原稿)", "(改稿)")


if __name__ == "__main__":
    hxt_core.cli_entry(main)
