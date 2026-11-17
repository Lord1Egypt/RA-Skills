#!/usr/bin/env python3
"""sentence_load.py — 中文句子负荷扫描器（hekouwang-writer-skill）

句法纪律（asd-ste100 迁移 + 中文阈值）：
  - 一句一事：分号连接两个事实 = 拆开
  - 句长：单句 ≥45 字告警，≥60 字必拆
  - 分句堆叠：句内逗号/分号 ≥5 → 考虑列表化
  - 修饰嵌套：句内「的」≥3 → 拆句
  - 模态保留：本脚本永不把「可能/约」当错误——那是内容不是噪音

放行项（命中时标注，由人工决定拆不拆）：公式行（含 = ÷）、等式链、
UI 操作路径（含 →）、联系人/电话行、政策条款引用行。

用法：
    sentence_load.py FILE [FILE ...]
    echo "文本" | sentence_load.py
    sentence_load.py --warn 40 --split 55 FILE

退出码：恒为 0（advisory，只报告不阻断）。
"""

import argparse
import json
import re
import sys

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
SENT_END = "。！？；!?;"           # 断句字符（含分号：分号连接两事实=拆开）
SPLIT_CHARS = SENT_END
CLAUSE_CHARS = "，,、；;"           # 分句堆叠计数字符

# 放行行特征：命中任意一条，长句标注「放行候选」而非「必拆」
RELEASE_HINTS = [
    ("公式", re.compile(r"[=＝÷＋+]")),
    ("等式链", re.compile(r"\d[\d,\.]*\s*[+＋]\s*\d")),
    ("UI路径", re.compile(r"→")),
    ("联系人/电话", re.compile(r"\d{3,}[-\s]?\d{4,}|\d{7,}")),
    ("条款引用", re.compile(r"[〔\[（(].{0,12}(号|条|款|文)")),
]

DEFAULT_WARN = 45
DEFAULT_SPLIT = 60


def cjk_len(s):
    return len(CJK_RE.findall(s))


def sentences(text):
    """按中文句末标点+分号切句，返回 [(句子, 所在行号)]。

    跳过非行文行：Markdown 表格行（|）、标题行（#）、分隔线（---）、代码围栏（```）。
    表格单元格不是句子；标题是标签不是论证。
    """
    out = []
    in_fence = False
    for ln, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.startswith(("|", "#", "---", "***")):
            continue
        buf = ""
        for ch in line:
            buf += ch
            if ch in SENT_END:
                if buf.strip():
                    out.append((buf, ln))
                buf = ""
        if buf.strip():
            out.append((buf, ln))
    return out


def release_kind(sent):
    for name, rx in RELEASE_HINTS:
        if rx.search(sent):
            return name
    return None


def analyze(text, warn, split):
    """返回 (句子列表, 必拆项, 告警项, 分句堆叠, 修饰嵌套)。"""
    sents = sentences(text)
    over, warn_l, stacked, nested = [], [], [], []
    for sent, ln in sents:
        n = cjk_len(sent)
        kind = release_kind(sent)
        entry = (ln, n, sent.strip(), kind)
        if n >= split:
            over.append(entry)
        elif n >= warn:
            warn_l.append(entry)
        if sum(sent.count(c) for c in CLAUSE_CHARS) >= 5:
            stacked.append(entry)
        if sent.count("的") >= 3:
            nested.append(entry)
    return sents, over, warn_l, stacked, nested


def selftest():
    """内置自测：长句必拆、公式/路径放行、短句不误报、分号即断句。"""
    long_sent = ("这是一个用来测试句长阈值的特别长的句子它没有任何公式路径电话条款政策文号等放行特征"
                 "所以必须被判定为超过必拆线需要按照语义边界拆成两句")
    formula_sent = ("个人账户养老金月标准 = 个人账户全部储存额 ÷ 计发月数一百三十九，"
                    "且参保人死亡的个人账户余额可以依法继承，支付终身不终止，"
                    "并且基础养老金标准会随国家政策调整而提高")
    cases = [
        ("长句必拆", long_sent, lambda r: len(r[1]) == 1 and not r[1][0][3]),
        ("公式放行", formula_sent, lambda r: r[1] and r[1][0][3] == "公式"),
        ("短句不误报", "这句话很短。", lambda r: not r[1] and not r[2]),
        ("分号断句", "第一句话；第二句话。", lambda r: len(r[0]) == 2),
        ("堆叠检出", "甲，乙，丙，丁，戊，己，庚，这么多分句堆在一句里", lambda r: len(r[3]) == 1),
    ]
    rep = report("<stdin>", long_sent, DEFAULT_WARN, DEFAULT_SPLIT)
    good = rep["hard"] == 1 and rep["over"][0]["release"] is None
    ok_json = good
    print(f"  [{'PASS' if good else 'FAIL'}] JSON 结构（hard=1）")
    ok = True
    for name, text, check in cases:
        r = analyze(text, DEFAULT_WARN, DEFAULT_SPLIT)
        good = check(r)
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}")
    ok = ok and ok_json
    print("selftest:", "全部通过" if ok else "有失败项")
    return 0 if ok else 1


def report(path, text, warn, split):
    """单个文本的结构化结果（--json 输出与调用方都用它）。"""
    sents, over, warn_l, stacked, nested = analyze(text, warn, split)

    def items(lst):
        return [{"line": ln, "len": n, "sentence": s, "release": kind} for ln, n, s, kind in lst]

    return {
        "path": path,
        "sentences": len(sents),
        "cjk": sum(cjk_len(s) for s, _ in sents),
        "warn": warn,
        "split": split,
        "over": items(over),
        "warn_items": items(warn_l),
        "stacked": items(stacked),
        "nested": items(nested),
        "hard": len([e for e in over if not e[3]]),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="中文句子负荷扫描（只报告，不修改）")
    ap.add_argument("files", nargs="*", help="待扫描文件；省略时读 stdin")
    ap.add_argument("--warn", type=int, default=DEFAULT_WARN, help="告警线字数")
    ap.add_argument("--split", type=int, default=DEFAULT_SPLIT, help="必拆线字数")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--selftest", action="store_true", help="运行内置自测")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    texts = []
    if args.files:
        for f in args.files:
            try:
                with open(f, encoding="utf-8") as fh:
                    texts.append((f, fh.read()))
            except OSError as e:
                print(f"读取失败：{f}（{e}）", file=sys.stderr)
                return 2
    else:
        texts.append(("<stdin>", sys.stdin.read()))

    if args.json:
        out = [report(path, text, args.warn, args.split) for path, text in texts]
        print(json.dumps(out[0] if len(out) == 1 else out, ensure_ascii=False, indent=2))
        return 0

    for path, text in texts:
        r = report(path, text, args.warn, args.split)

        def back(lst):
            return [(e["line"], e["len"], e["sentence"], e["release"]) for e in lst]

        over, warn, stacked, nested = back(r["over"]), back(r["warn_items"]), back(r["stacked"]), back(r["nested"])
        print(f"文件：{path}")
        print(f"中文句子：{r['sentences']} 句    中文字数：{r['cjk']}")
        print(f"档位阈值：告警 ≥{args.warn} 字　必拆 ≥{args.split} 字")
        print("-" * 64)
        print(f"【必拆线】≥{args.split} 字        {len(over)} 句")
        print(f"【告警线】{args.warn}–{args.split - 1} 字         {len(warn)} 句")
        print(f"【分句堆叠】句内逗号/分号 ≥5   {len(stacked)} 句")
        print(f"【修饰嵌套】句内「的」 ≥3      {len(nested)} 句")
        print("-" * 64)

        def show(title, items):
            if not items:
                return
            print(f"【{title}】")
            for ln, n, sent, kind in items:
                tag = f"（放行候选：{kind}）" if kind else ""
                preview = sent if len(sent) <= 46 else sent[:46] + "…"
                print(f"  L{ln:<5} 句长：{n:<4} {preview}{tag}")

        show(f"必拆线 ≥{args.split} 字", over)
        show(f"告警线 {args.warn}–{args.split - 1} 字", warn)
        show("分句堆叠", stacked)
        show("修饰嵌套", nested)

        print()
        print("【判读纪律】以下多为可放行项，人工确认后再决定是否拆：")
        print("  1) 公式/等式链——拆开破坏可读性；")
        print("  2) 并列枚举——改用 Markdown 列表，不必拆句；")
        print("  3) UI 操作路径、联系人/电话、政策条款引用——字数是硬的，拆了反而不通。")
        print("  修复方向只能是「重排与断句」，不得增删信息；拆句靠断句完成，")
        print("  不靠加「此外/因此/值得注意的是」。")
        if r["hard"]:
            print(f"\n⚠️ 有 {r['hard']} 句超过必拆线且无放行理由，请逐句处理。")
        else:
            print("\n✅ 超线句均有放行理由，或无不达标句。")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
