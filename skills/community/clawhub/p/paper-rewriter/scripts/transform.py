# -*- coding: utf-8 -*-
"""transform.py — 确定性机械清洗（语法安全层；深度改写由 agent 按指南执行）。

清洗范围（全部可逆、可审计，不改数字/引用/术语）:
  1. 各家模型残留 bug（oaicite/turn0search/[cite:]/grok_card/attached_file…）
  2. 聊天客套句与知识截止声明（整句删除）
  3. Markdown 残留（加粗/标题井号/行内代码，纯文本语境）
  4. 英文 filler 短语与 AI 高频词机械替换（语法安全清单）
  5. 中文半角标点全角化（CJK 语境判定，小数点/URL 不受影响）
  -a/--aggressive: 追加破折号降噪、空泛开场删除（英文）

用法:
    python scripts/transform.py in.txt -o out.txt
    python scripts/transform.py in.txt -a          # 激进档，就地输出到 stdout
    echo "文本" | python scripts/transform.py

退出码: 0 成功 | 2 用法/文件错误
"""

import argparse
import json
import shutil
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core


def load_fixes(lang, aggressive, lexicon=None):
    """返回 (rx, repl, note, guards) 四元组；guards 来自词库 term_guards，
    机械替换执行前先过守卫——financial leverage 这类正当搭配绝不改写。
    lexicon（v5.11.0）：外挂词表路径，透传 load_patterns 合并。"""
    fixes = []
    for code in ([lang] if lang in ("zh", "en") else ["zh", "en"]):
        pats = hxt_core.load_patterns(code, extra=lexicon)
        guards = pats.get("term_guards", [])
        fixes += [(re.compile(f["pattern"], re.IGNORECASE), f["replacement"], f["note"], guards)
                  for f in pats.get("auto_fixes", [])]
        if aggressive:
            fixes += [(re.compile(f["pattern"], re.IGNORECASE), f["replacement"], f["note"], guards)
                      for f in pats.get("aggressive_fixes", [])]
    return fixes


def apply_auto_fixes(text, fixes):
    applied = {}
    for rx, repl, note, guards in fixes:
        def _sub(m):
            # 术语守卫：命中属于正当学术用法（如 financial leverage）→ 原样保留
            if guards:
                before = text[max(0, m.start() - 30):m.start()]
                after = text[m.end():m.end() + 30]
                if hxt_core.guard_hit(m.group(0), before, after, guards):
                    return m.group(0)
            # 智能大小写：句首命中 Utilize → Use（替换词首字母跟随原词）
            r = m.expand(repl)
            if m.group(0)[:1].isupper() and r[:1].islower():
                r = r[0].upper() + r[1:]
            return r
        text, n = rx.subn(_sub, text)
        if n:
            applied[note] = applied.get(note, 0) + n
    return text, applied


def drop_flagged_sentences(text):
    """整句删除：聊天客套 / 知识截止 / AI 自我声明（中英）。

    按 span 精确删除，未命中的文本（含换行/空格）逐字节保留。
    英文以「句号+空白」为句尾，小数点（后无空白）不切句——防止
    一段里一句客套话导致整段被删。
    """
    removed = []
    # 非贪婪体 + 终止符三选一：句末标点 / 句号+空白 / 换行或串尾。
    # 体类包含 ASCII '.' 以保护小数（3.5 后无空白不终止）。
    rx = re.compile(r"[^。！？!?;\n]*?(?:[。！？!?;]+|\.(?=\s)|\n+|$)")
    # 整句删除只针对「整句性质」的残留：聊天客套/免责声明/知识截止。
    # 模型残留（oaicite/[cite:] 等）是行内垃圾，只做行内清除（auto_fixes），
    # 绝不能触发整句删除——否则会吞掉带引用标记的正常学术句。
    trigger = []
    for code in ("zh", "en"):
        pats = hxt_core.load_patterns(code)
        trigger += pats["chatbot_artifacts"] + pats["knowledge_cutoff"]

    spans_to_drop = []
    flagged_kept = []
    for m in rx.finditer(text):
        piece = m.group(0)
        if not piece.strip():
            continue
        for t in trigger:
            tm = t["_re"].search(piece)
            if tm:
                # 删除门槛：trigger 须覆盖 piece 主要部分（≥45%，分母不含句尾标点），
                # 且 piece 不含数字——防止连坐「客服话术+联系电话」这类混合句
                core = piece.strip().rstrip("。！？!?；;.")
                coverage = len(tm.group(0)) / max(1, len(core))
                if coverage >= 0.45 and not re.search(r"\d", piece):
                    spans_to_drop.append(m.span())
                    removed.append({"text": piece.strip()[:60],
                                    "reason": t.get("desc", t["pattern"])})
                else:
                    flagged_kept.append({"text": piece.strip()[:60],
                                         "reason": t.get("desc", t["pattern"]),
                                         "coverage": round(coverage, 2), "kept": True})
                break
    # 跨行触发词兜底：触发语被换行拆开时逐段匹配不到——在空白归一文本上
    # 复查一次，命中则标记待审（不自动删，防止误吞）
    if not spans_to_drop:
        normalized = re.sub(r"\s+", " ", text)
        for t in trigger:
            m = t["_re"].search(normalized)
            if m:
                flagged_kept.append({"text": m.group(0)[:60],
                                     "reason": t.get("desc", t["pattern"]) + "（跨行命中，请人工处理）",
                                     "kept": True})
                break
    out = text
    for s2, e in reversed(spans_to_drop):
        out = out[:s2] + out[e:]
    return out, removed + flagged_kept


def normalize_quotes(text):
    """英文语境弯引号→直引号（中文引号“”是正当用法，CJK 占比>5% 时跳过）。"""
    if hxt_core.cjk_ratio(text) > 0.05:
        return text, 0
    n = text.count("\u201c") + text.count("\u201d") + text.count("\u2018") + text.count("\u2019")
    if not n:
        return text, 0
    text = (text.replace("\u201c", '"').replace("\u201d", '"')
                .replace("\u2018", "'").replace("\u2019", "'"))
    return text, n


# ---------------------------------------------------------------------------
# 确定性深改档（v2.4.0 --deep）：句式级安全转换。
# 口径：只做「零信息损失」操作——删除纯套话标记、把排除式连接改成平铺连接；
# 不做同义改写、不碰数字/引用/术语（verify 仍整文守卫）。英文套腔在
# auto_fixes 已覆盖（如 It is important to note that → 删），此处不重复。
# ---------------------------------------------------------------------------

_ZH_DEEP_OPENERS = ["综上所述", "值得注意的是", "值得一提的是", "众所周知",
                    "不难发现", "由此可见", "总而言之", "总的来说"]
_ZH_OPENER_RX = re.compile(
    r"(^|[。！？!?]|\n)([ \t]*)(%s)[，,]\s*" % "|".join(_ZH_DEEP_OPENERS))
_ZH_NOT_ONLY_RX = re.compile(r"不仅([^，。；\n]{1,60})，而且")
_ZH_NOT_ALSO_RX = re.compile(r"不仅([^，。；\n]{1,60})，(还|也)")

def deep_polish(text):
    """确定性深改（v2.4.0）：句式级转换，返回 (text, ops)。

    ops 为 [{"op": 名称, "count": 处数}]，进 --track 修订记录可审计。
    两类操作：
      1. 句首八股删除——「综上所述，」「值得注意的是，」等纯套话标记
         （仅在句首/行首匹配，句中出现的「值得注意的是」不动，防误删）；
      2. 排除式连接合并——「不仅X，而且Y」→「X，且Y」（「还/也」→「也」），
         去掉宣言式框架、保留并列信息。
    """
    ops = []
    text, n1 = _ZH_OPENER_RX.subn(lambda m: m.group(1) + m.group(2), text)
    if n1:
        ops.append({"op": "句首八股删除", "count": n1})
    text, n2 = _ZH_NOT_ONLY_RX.subn(r"\1，且", text)
    # 「还」脱离「不仅」框架后改「也」，学术散文语感更平（「也」原样保留）
    text, n3 = _ZH_NOT_ALSO_RX.subn(lambda m: "%s，%s" % (m.group(1), "也"), text)
    if n2 + n3:
        ops.append({"op": "排除式连接合并", "count": n2 + n3})
    return text, ops


def deep_polish_ex(text):
    """deep_polish 的带改写句集合版（v3.1.1）：返回 (text, ops, changed_sents)。

    changed_sents = 改写后新出现的完整句集合——pipeline 传给 verify 做
    W_SENT_ADDED 精准豁免（--deep 自己改写的句不再触发「新增句子」告警；
    agent 真正擅自加的句子照拦）。零信息损失口径由此可审计。"""
    import hxt_core as _hc
    before = set(s for s in _hc.split_sentences(text) if len(s) >= 8)
    out, ops = deep_polish(text)
    after = set(s for s in _hc.split_sentences(out) if len(s) >= 8)
    return out, ops, after - before


# 全角字母/数字 → 半角（v2.9.0）。学术稿件规范用半角；中文输入法滑键常把
# 2025 打成 ２０２５（v2.8.0 verify E_NUM_WIDTH 红线的对症修复）。只动字母与
# 数字——全角标点是中文正当用法，不在此列。
_FW_ALNUM_MAP = str.maketrans(
    "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
    "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
    "０１２３４５６７８９",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789")


def normalize_fullwidth_alnum(text):
    """全角字母/数字归一为半角（v2.9.0），返回 (text, 改写数)。"""
    out = text.translate(_FW_ALNUM_MAP)
    n = sum(1 for a, b in zip(text, out) if a != b)
    return out, n


def main():
    ap = argparse.ArgumentParser(description="确定性机械清洗（不改数据/引用/术语）")
    ap.add_argument("file", nargs="?", help="输入文件；缺省读 stdin")
    ap.add_argument("-o", "--output", help="输出文件（缺省 stdout）")
    ap.add_argument("-a", "--aggressive", action="store_true", help="激进档")
    ap.add_argument("--deep", action="store_true",
                    help="深改档（v2.4.0）：句式级确定性转换——句首八股删除、"
                         "「不仅X而且Y」→「X，且Y」。零信息损失；不替代 agent 深改，"
                         "操作全部进 --track 可审计")
    ap.add_argument("--track", help="输出修订记录到此路径（同时生成 .md 与 .json）")
    ap.add_argument("-q", "--quiet", action="store_true", help="只写文件不打印报告")
    ap.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    ap.add_argument("--lexicon", metavar="文件",
                    help="外挂词表 JSON（v5.11.0）：同名键逐项追加，多 skill 共享同一外部词表")
    ap.add_argument("--dry-run", action="store_true",
                    help="预览模式：只报告将执行的替换与删除，不写输出文件、不改文本")
    ap.add_argument("--batch", metavar="目录",
                    help="批量清洗（v5.19.0）：目录内全部 .txt/.md 逐文件清洗，写 <名>_clean.txt"
                         "（输出已存在=跳过，断点续跑）；--in-place 则原地覆盖。互斥 file/-o/--dry-run")
    ap.add_argument("--in-place", action="store_true",
                    help="配合 --batch：原地覆盖原文件（不生成 _clean 副本，先备份 .bak）")
    ap.add_argument("--csv", metavar="文件",
                    help="批量汇总 CSV（v5.19.0：文件/替换类数/替换次数/删除句数）——配 --batch")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    # ── 批量清洗（v5.19.0）：目录逐文件，输出已存在=跳过（断点续跑）──
    if getattr(args, "batch", None):
        # v5.20 审计 P1：--batch 与单文件旗标互斥——同给响亮拒绝（防 --dry-run 静默写盘）
        if getattr(args, "dry_run", False) or args.file or args.output:
            print("错误: --batch 与 --dry-run/-o/单文件输入互斥——预览请去掉 --batch 单跑 --dry-run",
                  file=sys.stderr)
            sys.exit(2)
        import glob as _glob
        import csv as _csvmod
        _files = sorted(x for x in _glob.glob(os.path.join(args.batch, "*.txt"))
                        + _glob.glob(os.path.join(args.batch, "*.md"))
                        if "_clean" not in os.path.basename(x))
        if not _files:
            print("错误: 目录无 .txt/.md（%s）" % args.batch, file=sys.stderr)
            sys.exit(2)
        fixes = load_fixes(None, args.aggressive, lexicon=getattr(args, "lexicon", None))
        _rows = []
        _done = _skip = 0
        for fp in _files:
            _stem, _ext = os.path.splitext(fp)
            outp = fp if args.in_place else _stem + "_clean" + (_ext or ".txt")
            # 断点判定：副本形态看输出存在；in-place 形态看 .bak 备份存在（原文件恒存在不可作判据）
            _is_done = (os.path.exists(fp + ".bak") if args.in_place
                        else os.path.exists(outp))
            if _is_done:
                _skip += 1
                _rows.append([os.path.basename(fp), "skip", 0, 0, 0])
                continue
            try:
                t = hxt_core.read_text(fp)
            except (OSError, ValueError) as e:
                print("跳过 %s：%s" % (fp, e), file=sys.stderr)
                _rows.append([os.path.basename(fp), "error", 0, 0, 0])
                continue
            o, applied = apply_auto_fixes(t, fixes)
            o, removed = drop_flagged_sentences(o)
            o, _nq = normalize_quotes(o)
            o, _fw = normalize_fullwidth_alnum(o)
            if _fw:
                applied["全角字母数字归一"] = _fw
            if args.deep:
                o, deep_ops = deep_polish(o)
                for op in deep_ops:
                    applied["深改档:%s" % op["op"]] = op["count"]
            if args.in_place:
                shutil.copy2(fp, fp + ".bak")
            with open(outp, "w", encoding="utf-8") as of:
                of.write(o)
            _done += 1
            _rows.append([os.path.basename(fp), "ok",
                          len(applied), sum(applied.values()), len(removed)])
            print("%s：替换 %d 次（%d 类）、删句 %d" % (
                os.path.basename(fp), sum(applied.values()), len(applied), len(removed)),
                file=sys.stderr)
        if args.csv:
            try:
                with open(args.csv, "w", encoding="utf-8-sig", newline="") as cf:
                    w = _csvmod.writer(cf)
                    w.writerow(["file", "status", "categories", "replacements", "sentences_removed"])
                    w.writerows(_rows)
                print("批量汇总 CSV 已写入 %s" % args.csv, file=sys.stderr)
            except OSError as e:
                print("错误: 无法写入 CSV（%s）" % e, file=sys.stderr)
        print("批量清洗完成：%d 清洗 / %d 跳过（共 %d 文件）" % (_done, _skip, len(_files)),
              file=sys.stderr)
        sys.exit(0)

    if args.file:
        try:
            text = hxt_core.read_text(args.file)
        except OSError as e:
            print("错误: 无法读取文件（%s）" % e, file=sys.stderr)
            sys.exit(2)
        except ValueError as e:
            print("错误: %s" % e, file=sys.stderr)
            sys.exit(2)
    else:
        text = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")

    if not text.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(2)

    lang = None if args.lang == "auto" else args.lang
    detected = hxt_core.detect_language(text)
    if lang is None:
        lang = detected

    # 机械修复始终双语加载：中文文本照样可能有英文模型残留（[cite:]/oaicite），
    # 反之亦然；词表本身语言互斥，双语应用无误伤。--lang 仅影响诊断语言报告。
    fixes = load_fixes(None, args.aggressive, lexicon=getattr(args, "lexicon", None))
    out, applied = apply_auto_fixes(text, fixes)
    out, removed = drop_flagged_sentences(out)
    out, n_quotes = normalize_quotes(out)
    out, n_fw = normalize_fullwidth_alnum(out)
    if n_fw:
        applied["全角字母数字归一"] = n_fw
        if not args.quiet:
            print("全角字母/数字→半角: %d 字符" % n_fw, file=sys.stderr)
    deep_ops = []
    if args.deep:
        out, deep_ops = deep_polish(out)
        for op in deep_ops:
            applied["深改档:%s" % op["op"]] = op["count"]
        if not args.quiet:
            for op in deep_ops:
                print("深改档: %s ×%d" % (op["op"], op["count"]), file=sys.stderr)

    if getattr(args, "dry_run", False):
        # v5.16.0 预览模式：文本已算好但不落盘不输出——只报将执行的动作
        print("── dry-run 预览（不写盘、不输出文本）──", file=sys.stderr)
        if applied:
            for note, cnt in sorted(applied.items(), key=lambda kv: -kv[1]):
                print("  将替换: %s ×%d" % (note, cnt), file=sys.stderr)
        else:
            print("  无机械替换", file=sys.stderr)
        if removed:
            print("  将删除句: %d 句" % len(removed), file=sys.stderr)
            for _r in removed[:5]:
                print("    - %s" % str(_r)[:60], file=sys.stderr)
        if deep_ops:
            for op in deep_ops:
                print("  深改档将做: %s ×%d" % (op["op"], op["count"]), file=sys.stderr)
        print("── 预览结束（去掉 --dry-run 实际执行）──", file=sys.stderr)
        sys.exit(0)
    if args.output:
        try:
            hxt_core.write_output(out, args.output, src_path=args.file)
        except OSError as e:
            print("错误: 无法写入 %s（%s）" % (args.output, e), file=sys.stderr)
            sys.exit(2)

    if getattr(args, "track", None):
        md, jobj = hxt_core.build_revision_log(applied, removed,
                                               source=args.file or "(stdin)")
        base = args.track
        try:
            with open(base + ".md", "w", encoding="utf-8") as f:
                f.write(md + "\n")
            with open(base + ".json", "w", encoding="utf-8") as f:
                json.dump(jobj, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print("错误: 无法写入修订记录（%s）" % e, file=sys.stderr)
            sys.exit(2)
        print("修订记录已写入 %s.md / %s.json" % (base, base), file=sys.stderr)

    if not args.quiet:
        report = {
            "aggressive_warning": (
                "激进模式(-a)适用场景：非正式文本的破折号堆叠、空泛开场白（如 in today's world）。"
                "不适用：学术方法段（破折号可能是插入语）、数值范围（守卫已跳过）、"
                "任何将直接提交的文本——改写后请人工复核全文再使用。"
                if args.aggressive else None),
            "input_chars": len(text),
            "output_chars": len(out),
            "output": args.output or "(stdout)",
            "applied_fixes": applied,
            "removed_sentences": removed,
            "quotes_normalized": n_quotes,
            "note": "机械清洗只覆盖语法安全层；黑话/八股/节奏需 agent 按 references 指南深改，"
                    "改完必须跑 verify.py 守卫完整性",
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    hxt_core.cli_entry(main)
