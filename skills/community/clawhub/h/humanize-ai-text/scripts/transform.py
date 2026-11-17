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
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core


def load_fixes(lang, aggressive):
    """返回 (rx, repl, note, guards) 四元组；guards 来自词库 term_guards，
    机械替换执行前先过守卫——financial leverage 这类正当搭配绝不改写。"""
    fixes = []
    for code in ([lang] if lang in ("zh", "en") else ["zh", "en"]):
        pats = hxt_core.load_patterns(code)
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


def main():
    ap = argparse.ArgumentParser(description="确定性机械清洗（不改数据/引用/术语）")
    ap.add_argument("file", nargs="?", help="输入文件；缺省读 stdin")
    ap.add_argument("-o", "--output", help="输出文件（缺省 stdout）")
    ap.add_argument("-a", "--aggressive", action="store_true", help="激进档")
    ap.add_argument("--track", help="输出修订记录到此路径（同时生成 .md 与 .json）")
    ap.add_argument("-q", "--quiet", action="store_true", help="只写文件不打印报告")
    ap.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

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
    fixes = load_fixes(None, args.aggressive)
    out, applied = apply_auto_fixes(text, fixes)
    out, removed = drop_flagged_sentences(out)
    out, n_quotes = normalize_quotes(out)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out)
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
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
