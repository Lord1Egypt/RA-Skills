# -*- coding: utf-8 -*-
"""check_terms.py — 术语一致性检查器（v1.9.0 实质功能，竞品零有）。

扫描文档内同一概念的多种称谓（如「患者/病人」「ID/identifier」），
逐处报告位置与建议统一形式。支持内置中文/英文常见对 + 用户自定义对。
"""
import argparse
import json
import os
import re
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

# v3.1.0 变体组制（v3.0.0 域包制升级）：同组变体可 >2 个——HF 组直接带 心衰，
# 告诉引擎「这 N 个写法指同一概念」即可，无需两两复制对。嵌套铁律不变：
# 任何变体不得是另一变体的子串（狼疮/肝功教训），validate_packs() 断言。
_TERM_GROUPS = [
    {"pack": "通用", "variants": ["患者", "病人"]},
    {"pack": "通用", "variants": ["肾功能", "肾脏功能"]},
    {"pack": "通用", "variants": ["副作用", "不良反应"]},
    {"pack": "通用", "variants": ["禁忌症", "禁忌证"]},
    {"pack": "通用", "variants": ["适应症", "适应证"]},
    {"pack": "通用", "variants": ["血象", "血液常规"]},
    {"pack": "通用", "variants": ["identifier", "ID"]},
    {"pack": "通用", "variants": ["health care", "healthcare"]},
    {"pack": "风湿免疫", "variants": ["SLE", "系统性红斑狼疮"]},
    {"pack": "内分泌", "variants": ["T2DM", "2型糖尿病"]},
    {"pack": "内分泌", "variants": ["HbA1c", "糖化血红蛋白"]},
    {"pack": "内分泌", "variants": ["甲减", "甲状腺功能减退"]},
    {"pack": "内分泌", "variants": ["DKA", "糖尿病酮症酸中毒"]},
    {"pack": "心血管", "variants": ["HF", "心力衰竭", "心衰"]},
    {"pack": "心血管", "variants": ["AMI", "急性心肌梗死"]},
    {"pack": "心血管", "variants": ["AF", "心房颤动"]},
    {"pack": "心血管", "variants": ["PCI", "经皮冠状动脉介入治疗"]},
    {"pack": "心血管", "variants": ["CHD", "冠心病"]},
    {"pack": "肿瘤", "variants": ["NSCLC", "非小细胞肺癌"]},
    {"pack": "肿瘤", "variants": ["化疗", "化学治疗"]},
    {"pack": "肿瘤", "variants": ["实体瘤", "实体肿瘤"]},
    {"pack": "呼吸", "variants": ["COPD", "慢性阻塞性肺疾病"]},
    {"pack": "呼吸", "variants": ["ARDS", "急性呼吸窘迫综合征"]},
    {"pack": "消化", "variants": ["GERD", "胃食管反流病"]},
    {"pack": "消化", "variants": ["IBS", "肠易激综合征"]},
    {"pack": "神经", "variants": ["脑卒中", "中风"]},
    {"pack": "神经", "variants": ["TIA", "短暂性脑缺血发作"]},
]

# 兼容视图：_TERM_PACKS[域]=组列表；_BUILTIN_PAIRS=每组前两变体的平面投影
_TERM_PACKS = {}
for _g in _TERM_GROUPS:
    _TERM_PACKS.setdefault(_g["pack"], []).append(list(_g["variants"]))

_BUILTIN_PAIRS = [(g["variants"][0], g["variants"][1]) for g in _TERM_GROUPS]

_PAIR_PACK = {}
for _g in _TERM_GROUPS:
    for _i, _a in enumerate(_g["variants"]):
        for _b in _g["variants"][_i + 1:]:
            _PAIR_PACK[(_a, _b)] = _g["pack"]
            _PAIR_PACK[(_b, _a)] = _g["pack"]


def _pair_in_builtin(a, b):
    """(a,b) 是否同属某内置组（任意两个成员，不限相邻）——去重与域归属共用。"""
    for _g in _TERM_GROUPS:
        if a in _g["variants"] and b in _g["variants"]:
            return _g["pack"]
    return None


def find_group_inconsistencies(text, groups):
    """变体组检查（v3.1.0）：同组 ≥2 个变体各自出现 → 一行报告。

    行结构兼容 v3.0.x 的 a/b/a_count/b_count（取出现次数最多的前两变体），
    并新增 canonical/variants 字段（variants=全部变体计数 dict）。"""
    results = []
    for g in groups:
        counts = {v: len(re.findall(re.escape(v), text)) for v in g["variants"]}
        present = {v: c for v, c in counts.items() if c > 0}
        if len(present) >= 2:
            ranked = sorted(present.items(), key=lambda x: -x[1])
            (a, ca), (b, cb) = ranked[0], ranked[1]
            results.append({
                "pack": g["pack"], "canonical": g["variants"][0],
                "variants": present, "a": a, "b": b, "a_count": ca, "b_count": cb,
                "suggestion": a})
    return results


def find_inconsistencies(text, pairs):
    """v3.0.x 二元对接口（保留兼容）：内部转为变体组复用同引擎。"""
    groups = [{"pack": _pair_in_builtin(a, b) or "用户自定义",
               "variants": [a, b]} for a, b in pairs]
    return find_group_inconsistencies(text, groups)


def validate_packs():
    """嵌套安全校验：返回违规清单 [(变体A, 变体B, 所属域)]（A 是 B 的子串）。
    空列表=全部安全。测试套件对此断言为空。"""
    bad = []
    allvars = [(v, g["pack"]) for g in _TERM_GROUPS for v in g["variants"]]
    for v1, p1 in allvars:
        for v2, p2 in allvars:
            if v1 != v2 and v1 in v2:
                bad.append((v1, v2, p1))
    return bad


def load_user_pairs(path):
    txt = hxt_core.read_text(path)
    out = []
    for ln in txt.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split("|")
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            if a and b:
                out.append((a, b))
    return out


def build_report(results, source=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = ["# 术语一致性检查：%s" % (source or "未命名文稿"), "",
             "> 自动生成（%s）" % now, ""]
    if not results:
        lines.append("未发现术语不一致。")
        return "\n".join(lines)
    lines.append("发现 %d 组术语不一致：" % len(results))
    lines.append("")
    lines.append("| 域 | 变体（出现次数） | 建议统一为 |")
    lines.append("| --- | --- | --- |")
    for r in results:
        vs = " / ".join("%s(%d)" % (v, c) for v, c in sorted(
            r["variants"].items(), key=lambda x: -x[1]))
        lines.append("| %s | %s | %s |" % (r.get("pack", ""), vs, r["suggestion"]))
    lines.append("")
    lines.append("> 术语不统一是审稿人最常见的批注之一。建议通读全文，将"
                 "使用频次较低的变体统一替换。")
    return "\n".join(lines)


# ── 术语统一稿（v4.4.0 --unify）：检查只报不改，统一稿生成同样不静默——
# 逐处替换计数全部透出，建议产物需人工复核后再采用 ──
_HEADER_MARK_TXT = "════ 术语统一稿"
_HEADER_MARK_MD = "<!-- 术语统一稿"


def strip_header_block(text):
    """剥除统一稿头部清单块（v4.5.0 自指安全）：对带头块的统一稿再跑检查/
    --unify 时，头块自己的「A → B」清单行会被当成正文变体（干净文档被工具
    自产物判脏、头块叠加）。txt 块从标记行到结束线、md 块从 <!-- 到 --> 整段剥除。"""
    for mark, is_md in ((_HEADER_MARK_MD, True), (_HEADER_MARK_TXT, False)):
        i = text.find(mark)
        if i < 0:
            continue
        if is_md:
            j = text.find("-->", i)
            if j < 0:
                # 注释未闭合（手改破损）：保守剥到块标记行尾为止
                k = text.find("\n", i)
                return (text[:i] + (text[k + 1:] if k >= 0 else "")).lstrip("\n")
            return (text[:i] + text[j + 3:]).lstrip("\n")
        lines = text.split("\n")
        out, skip = [], False
        for ln in lines:
            if mark in ln:
                skip = True
                continue
            if skip and ln.startswith("════"):
                skip = False
                continue
            if not skip:
                out.append(ln)
        return "\n".join(out).lstrip("\n")
    return text


def build_unify_plan(results):
    """检查结果 → 替换映射 {变体: 统一形}（统一形=每组出现最多的变体，
    与报告「建议统一为」同源）。两级冲突防御，均响亮报错而非静默任选：
    ①同一变体作为源出现在两组且目标不同；②某组的统一形又是别组的待替换
    变体（值域∩键域非空——统一到 A 却又要把 A 统一走，目标自相矛盾）。"""
    mapping = {}
    for r in results:
        target = r["suggestion"]
        for v in r["variants"]:
            if v == target:
                continue
            prev = mapping.get(v)
            if prev is not None and prev != target:
                hxt_core.fail(
                    "变体「%s」同时出现在两组且统一目标不同（%s / %s）"
                    % (v, prev, target),
                    hint="用 --pack 分域检查，或修正自定义术语对后重跑")
            mapping[v] = target
    loop = set(mapping.values()) & set(mapping.keys())
    if loop:
        hxt_core.fail(
            "统一目标自相矛盾：%s 既是要统一到的目标、又是别组的待替换变体"
            % "、".join(sorted(loop)),
            hint="用 --pack 分域检查，或修正自定义术语对后重跑")
    return mapping


def unify_text(text, mapping):
    """按映射生成统一稿：变体按长度降序合成一个 alternation 单遍替换。
    单遍保证替换产生的文本不会被后续 key 再命中；长度降序防跨组嵌套
    （内置组有嵌套校验，用户自定义对没有）。返回 (统一稿, 逐 key 计数)。"""
    if not mapping:
        return text, []
    keys = sorted(mapping, key=len, reverse=True)
    rx = re.compile("|".join(re.escape(k) for k in keys))
    detail = {k: 0 for k in keys}

    def _sub(m):
        k = m.group(0)
        detail[k] += 1
        return mapping[k]

    unified = rx.sub(_sub, text)
    rows = [{"from": k, "to": mapping[k], "count": detail[k]}
            for k in sorted((k for k in keys if detail[k]),
                            key=lambda k: -detail[k])]
    return unified, rows


def main():
    import hxt_core
    ap = argparse.ArgumentParser(description="术语一致性检查器")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + hxt_core.__version__)
    ap.add_argument("file", nargs="?", help="待检文档（.txt/.md/.docx）")
    ap.add_argument("--batch", help="跨文件模式（v3.7.0）：检查目录内全部 .txt/.md/.docx（不含 .pdf）——"
                                    "逐文件组内不一致 + 跨文件变体漂移（各文件各自用词一致、"
                                    "合起来不一致，如摘要用「肝功能」正文用「肝功」）；与 file 互斥")
    ap.add_argument("--pairs", help="用户自定义术语对文件（每行 A|B）")
    ap.add_argument("--pack", help="只跑指定域包（如 心血管）；默认全量")
    ap.add_argument("--list-packs", action="store_true",
                    help="列出全部域包及对数后退出")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", help="生成 markdown 一致性报告")
    ap.add_argument("--unify", help="生成术语统一稿到此路径（v4.4.0）：每组统一为"
                                    "出现最多的变体，逐处替换计数全部透出；输出"
                                    ".docx 后缀即回写 Word。统一稿是建议产物，"
                                    "复核替换清单后再采用；仅单文件模式")
    ap.add_argument("--no-header", action="store_true",
                    help="统一稿不注入头部替换清单块（v4.5.0；缺省在 .txt/.md 稿"
                         "头部注入复核清单注释，.docx 始终不注入）")
    args = ap.parse_args()

    if args.list_packs:
        for pk in sorted(_TERM_PACKS):
            n = sum(len(v) for v in _TERM_PACKS[pk])
            print("%s（%d 组 / %d 变体）" % (pk, len(_TERM_PACKS[pk]), n))
        sys.exit(0)
    if not args.file and not args.batch:
        ap.error("缺少待检文档（或用 --batch 目录做跨文件检查）")
    if args.file and args.batch:
        ap.error("--batch 与单文件模式互斥（只传其一）")
    if args.unify and args.batch:
        ap.error("--unify 暂只支持单文件模式（--batch 请逐文件处理）")
    if args.unify and not args.file:
        ap.error("--unify 需要待检文档")
    if args.unify and args.report:
        ap.error("--unify 与 --report 互斥（统一稿运行自带替换清单；"
                 "要 markdown 报告请分开两次跑）")
    if args.pack and args.pack not in _TERM_PACKS:
        ap.error("未知域包 %r；--list-packs 查看（%s）"
                 % (args.pack, "/".join(sorted(_TERM_PACKS))))

    groups = ([{"pack": args.pack, "variants": list(vs)}
               for vs in _TERM_PACKS[args.pack]] if args.pack
              else [dict(g) for g in _TERM_GROUPS])
    if args.pairs:
        # 用户对去重合并：两变体同属某内置组（任意成员对，不限相邻）的不再追加——
        # 否则同一概念出两行且一行错标「用户自定义」（v3.1.0 评审实锤）
        for a, b in load_user_pairs(args.pairs):
            if _pair_in_builtin(a, b):
                continue
            groups.append({"pack": "用户自定义", "variants": [a, b]})

    # ── 跨文件模式（v3.7.0）：逐文件组内不一致 + 跨文件变体漂移 ──
    if args.batch:
        root = args.batch
        if not os.path.isdir(root):
            print("错误: --batch 需要目录（%s）" % root, file=sys.stderr)
            sys.exit(2)
        texts, load_errs = {}, []
        for fn in sorted(os.listdir(root)):
            if not fn.lower().endswith((".txt", ".md", ".docx")):
                continue
            fp = os.path.join(root, fn)
            try:
                texts[fn] = hxt_core.read_text(fp)
            except (OSError, ValueError) as e:
                load_errs.append((fn, str(e)[:80]))
        if not texts:
            if load_errs:
                # 全部文件读取失败≠「一致」——fail-closed（误报 clean 是最坏的失败态）
                print("错误: 目录内 %d 个文件全部读取失败（%s）" % (len(load_errs), root),
                      file=sys.stderr)
                for fn, msg in load_errs:
                    print("  %s：%s" % (fn, msg), file=sys.stderr)
                sys.exit(2)
            print("错误: 目录内没有 .txt/.md/.docx 文件（%s）" % root, file=sys.stderr)
            sys.exit(2)
        per_file = {fn: find_group_inconsistencies(strip_header_block(tx), groups)
                    for fn, tx in texts.items()}
        # 跨文件漂移同样基于剥头块后的正文（统一稿的头块清单行不参与漂移统计）
        drift_src = {fn: strip_header_block(tx) for fn, tx in texts.items()}
        # 跨文件漂移：各文件「主导变体」（出现最多的）构成集合，≥2 个不同 → 漂移。
        # 单文件各自一致、合起来不一致是多章节论文最隐蔽的术语病，单文件模式看不见。
        drift = []
        for g in groups:
            dominant = {}
            for fn, tx in drift_src.items():
                counts = {v: len(re.findall(re.escape(v), tx)) for v in g["variants"]}
                present = {v: c for v, c in counts.items() if c > 0}
                if present:
                    dominant[fn] = max(present.items(), key=lambda x: x[1])
            if len({v for v, _c in dominant.values()}) >= 2:
                total = {}
                for v, c in dominant.values():
                    total[v] = total.get(v, 0) + c
                drift.append({
                    "pack": g["pack"], "canonical": g["variants"][0],
                    "files": {fn: v for fn, (v, _c) in sorted(dominant.items())},
                    "suggestion": max(total.items(), key=lambda x: x[1])[0]})
        n_issues = sum(len(v) for v in per_file.values()) + len(drift)
        if args.json:
            # 与单文件 --json 同口径：恒 exit 0，机器分支读 total 字段
            print(json.dumps({"files": len(texts), "load_errors": load_errs,
                              "per_file": per_file, "cross_file_drift": drift,
                              "total": n_issues},
                             ensure_ascii=False, indent=2))
            sys.exit(0)
        if args.report:
            lines = ["# 术语一致性检查（跨文件）：%s" % root, "",
                     "> 自动生成（%s） · %d 个文件" % (
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), len(texts)), ""]
            if load_errs:
                lines.append("## 读取失败（跳过）")
                lines.extend("- %s：%s" % (fn, msg) for fn, msg in load_errs)
                lines.append("")
            lines.append("## 跨文件变体漂移（%d 组）" % len(drift))
            if not drift:
                lines.append("未发现跨文件漂移。")
            else:
                lines.append("")
                lines.append("| 域 | 文件 → 主导变体 | 建议统一为 |")
                lines.append("| --- | --- | --- |")
                for d in drift:
                    fmap = " / ".join("%s→%s" % (fn, v)
                                      for fn, v in d["files"].items())
                    lines.append("| %s | %s | %s |" % (d["pack"], fmap, d["suggestion"]))
            lines.append("")
            lines.append("## 各文件内部不一致")
            any_internal = False
            for fn in sorted(per_file):
                rs = per_file[fn]
                if not rs:
                    continue
                any_internal = True
                lines.append("")
                lines.append("### %s（%d 组）" % (fn, len(rs)))
                for r in rs:
                    vs = " / ".join("%s(%d)" % (v, c) for v, c in sorted(
                        r["variants"].items(), key=lambda x: -x[1]))
                    lines.append("- [%s] %s → 建议「%s」" % (
                        r.get("pack", ""), vs, r["suggestion"]))
            if not any_internal:
                lines.append("各文件内部均一致。")
            try:
                with open(args.report, "w", encoding="utf-8") as rf:
                    rf.write("\n".join(lines) + "\n")
                print("报告已写入 %s" % args.report, file=sys.stderr)
            except OSError as e:
                print("错误: 无法写入报告（%s）" % e, file=sys.stderr)
        for fn, msg in load_errs:
            print("[跳过] %s 读取失败：%s" % (fn, msg), file=sys.stderr)
        if drift:
            print("发现 %d 组跨文件变体漂移：" % len(drift))
            for d in drift:
                fmap = " / ".join("%s→%s" % (fn, v)
                                  for fn, v in d["files"].items())
                print("  [%s] %s → 建议「%s」" % (d["pack"], fmap, d["suggestion"]))
        else:
            print("未发现跨文件变体漂移。")
        n_bad = sum(1 for rs in per_file.values() if rs)
        if n_bad:
            print("%d 个文件内部存在术语不一致（--report 看逐文件明细）：" % n_bad)
            for fn in sorted(per_file):
                if per_file[fn]:
                    print("  %s（%d 组）" % (fn, len(per_file[fn])))
        elif not drift:
            print("各文件内部均一致。")
        if load_errs and n_issues == 0:
            # 部分文件读取失败且幸存文件零发现：不判「一致」（跳过的一半漂移对
            # 会伪装成 clean）——exit 1 让调用方看到 [跳过] 明细后人工定夺
            print("有 %d 个文件读取失败被跳过，暂不判定「一致」；排除故障后重跑"
                  % len(load_errs), file=sys.stderr)
            sys.exit(1)
        sys.exit(0 if n_issues == 0 else 1)

    try:
        text = hxt_core.read_text(args.file)
    except (OSError, ValueError) as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)
    # 统一稿再处理自指安全（v4.5.0）：输入带历史头块时先剥除再统计
    text = strip_header_block(text)

    results = find_group_inconsistencies(text, groups)

    # ── 统一稿模式（v4.4.0）：生成 → 透出逐 key 计数 → 建议 verify 复核 ──
    if args.unify:
        mapping = build_unify_plan(results)
        if not mapping:
            if args.json:
                # --json 恒 JSON 契约（batch 模式同款口径）：已一致也出机器口径
                print(json.dumps({"unify_output": None,
                                  "already_consistent": True,
                                  "groups": 0, "replacements": 0,
                                  "detail": [], "inconsistencies": []},
                                 ensure_ascii=False, indent=2))
                sys.exit(0)
            print("未发现术语不一致——已一致，无需生成统一稿。")
            sys.exit(0)
        unified, detail = unify_text(text, mapping)
        # 头部清单注入（v4.5.0，usability 处方：复核零切换——打开统一稿第一屏
        # 就是替换清单）：.txt/.md 注入（md 用 HTML 注释渲染不可见）；.docx 是
        # 交付件不注入（清单看运行输出）。--no-header 关闭。.md 检测到 YAML
        # front matter 时注入其后（front matter 必须居首，pandoc/Jekyll 口径）。
        if detail and not args.no_header and not args.unify.lower().endswith(".docx"):
            head, body = "", unified
            if args.unify.lower().endswith(".md") and unified.startswith("---"):
                k = unified.find("\n---", 3)
                if k >= 0:
                    k = unified.find("\n", k + 1)
                    head, body = unified[:k + 1], unified[k + 1:]
            if args.unify.lower().endswith(".md"):
                block = ("<!-- 术语统一稿（复核后删除本注释块，再跑 verify.py）\n"
                         + "\n".join("  %s → %s（%d 处）" % (x["from"], x["to"], x["count"])
                                     for x in detail)
                         + "\n  共 %d 组 / %d 处替换 -->\n\n"
                             % (len(detail), sum(x["count"] for x in detail)))
            else:
                block = ("════ 术语统一稿 · 复核后删除本块再跑 verify ════\n"
                         + "\n".join("  %s → %s（%d 处）" % (x["from"], x["to"], x["count"])
                                     for x in detail)
                         + "\n  共 %d 组 / %d 处替换\n"
                             "══════════════════════════════\n\n"
                             % (len(detail), sum(x["count"] for x in detail)))
            unified = head + block + body
        try:
            hxt_core.write_output(unified, args.unify, src_path=args.file)
        except OSError as e:
            print("错误: 无法写入统一稿 %s（%s）" % (args.unify, e),
                  file=sys.stderr)
            sys.exit(2)
        total = sum(d["count"] for d in detail)
        if args.json:
            print(json.dumps({"unify_output": args.unify,
                              "groups": len(detail), "replacements": total,
                              "detail": detail, "inconsistencies": results},
                             ensure_ascii=False, indent=2))
            sys.exit(0)
        print("统一稿已写入 %s（%d 组术语 / 共 %d 处替换）"
              % (args.unify, len(detail), total))
        for d in detail:
            print("  %s → %s（%d 处）" % (d["from"], d["to"], d["count"]))
        print("提示：统一稿是建议产物——逐处复核清单后再采用；"
              "随后建议跑 verify.py 确认数字与引用完整性。")
        sys.exit(0)

    if args.json:
        print(json.dumps({"inconsistencies": results, "total": len(results)},
                         ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.report:
        md = build_report(results, source=args.file)
        try:
            with open(args.report, "w", encoding="utf-8") as rf:
                rf.write(md + "\n")
            print("报告已写入 %s" % args.report, file=sys.stderr)
        except OSError as e:
            print("错误: 无法写入报告（%s）" % e, file=sys.stderr)

    if not results:
        print("未发现术语不一致。")
        sys.exit(0)

    print("发现 %d 组术语不一致：" % len(results))
    for r in results:
        vs = " / ".join("%s(%d)" % (v, c) for v, c in sorted(
            r["variants"].items(), key=lambda x: -x[1]))
        print("  [%s] %s → 建议「%s」" % (r.get("pack", ""), vs, r["suggestion"]))
    sys.exit(1)


if __name__ == "__main__":
    hxt_core.cli_entry(main)
