#!/usr/bin/env python3
"""Generate podcast script from article text."""

import argparse, os, sys, re

SOLO = """# 🎙️ 播客脚本

**标题**: {title} | **格式**: 单人主播 | **时长**: ~{dur}分钟

---

## 开场白

大家好，欢迎收听本期节目！今天聊一个有意思的话题——{title}。

## 话题引入

{intro}

{segments}

## 总结

来回顾一下今天的要点：

{takes}

## 结尾

以上就是本期全部内容，觉得有收获的话别忘了订阅，我们下期再见！
"""

DIAL = """# 🎙️ 播客脚本

**标题**: {title} | **格式**: 双人对谈 | **时长**: ~{dur}分钟

---

## 开场白

**A**: 大家好！欢迎收听，我是主播A。

**B**: 我是主播B！今天聊——{title}。

**A**: 话题很火，咱们开始吧。

## 话题引入

**B**: 先介绍一下背景。

**A**: {intro}

{segments}

## 总结

**A**: 来总结一下。

{takes}

## 结尾

**B**: 今天就到这了！

**A**: 喜欢的话记得订阅，下期见！

**B**: 拜拜！
"""

TRANSITIONS_A = ["说得对，我补充一下。", "没错，还有一点。", "确实，另外呢——", "说到这个，我想到——", "对，我们接着聊。"]
TRANSITIONS_B = ["嗯，展开讲讲。", "有意思，继续。", "这点很关键。", "同意，而且——", "好观点，接着说。"]


def title(text):
    for l in text.strip().split("\n"):
        l = l.strip()
        if l:
            return re.sub(r'^#+\s*', '', l)[:60]
    return "未命名话题"


def paragraphs(text):
    ps, cur = [], []
    for l in text.split("\n"):
        s = l.strip()
        if not s:
            if cur:
                ps.append(" ".join(cur))
                cur = []
        elif not s.startswith("#"):
            cur.append(s)
    if cur:
        ps.append(" ".join(cur))
    return [p for p in ps if len(p) > 15]


def solo_segs(ps):
    parts = []
    for i, p in enumerate(ps):
        parts.append(f"## 第{i+1}部分\n\n{p}\n")
    return "\n---\n\n".join(parts)


def dial_segs(ps):
    parts = []
    for i, p in enumerate(ps):
        sp = "A" if i % 2 == 0 else "B"
        other = "B" if sp == "A" else "A"
        tr = (TRANSITIONS_A if other == "A" else TRANSITIONS_B)[i % 5]
        parts.append(f"## 第{i+1}部分\n\n**{sp}**: {p}\n\n**{other}**: {tr}\n")
    return "\n---\n\n".join(parts)


def takes(ps, fmt):
    out = []
    for i, p in enumerate(ps[:5]):
        s = p.split("。")[0]
        if len(s) > 80:
            s = s[:80] + "…"
        if fmt == "dialogue":
            sp = "A" if i % 2 == 0 else "B"
            out.append(f"**{sp}**: {i+1}. {s}")
        else:
            out.append(f"{i+1}. {s}")
    return "\n\n".join(out)


def generate(text, fmt="solo"):
    t = title(text)
    ps = paragraphs(text)
    if not ps:
        return "Error: 文本内容不足"
    dur = max(3, len(text) // 200)
    intro = ps[0]
    body = ps[1:] if len(ps) > 1 else ps
    tpl = DIAL if fmt == "dialogue" else SOLO
    segs = dial_segs(body) if fmt == "dialogue" else solo_segs(body)
    return tpl.format(title=t, dur=dur, intro=intro, segments=segs, takes=takes(body, fmt))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="File path or '-' for stdin")
    p.add_argument("--format", choices=["solo", "dialogue"], default="solo")
    p.add_argument("--output", default=None)
    a = p.parse_args()

    if a.input == "-":
        txt = sys.stdin.read()
    elif os.path.isfile(a.input):
        txt = open(a.input, encoding="utf-8").read()
    else:
        txt = a.input

    result = generate(txt, a.format)
    if a.output:
        open(a.output, "w", encoding="utf-8").write(result)
        print(f"✅ 脚本已生成: {a.output}")
    else:
        print(result)
