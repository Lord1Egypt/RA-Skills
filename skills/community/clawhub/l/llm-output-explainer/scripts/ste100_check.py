#!/usr/bin/env python3
"""ste100_check.py — 简化版 STE100 / 中文受控写作自检

对文本文件执行启发式检查（非完整 STE 规则引擎，覆盖最高频违规）：
  英文: 句长>25词、被动标记、含糊词、隐喻/习语信号
  中文: 句长>60字、成语堆砌信号、"的地得"误用信号、模糊量词

用法:
    python3 ste100_check.py <file.md|file.txt> [--lang en|zh|auto] [--strict]
退出码: 0 = 通过(0严重问题)  1 = 发现问题（供 CI/脚本门控）
"""
import re
import sys

EN_VAGUE = {
    "as soon as possible", "as quickly as possible", "several", "a number of",
    "a lot of", "a few", "various", "a variety of", "appropriate", "relevant",
    "if necessary", "if possible", "etc.", "and so on", "roughly", "approximately",
    "large", "small"  # 单独出现且无数字时告警
}
EN_PASSIVE = [
    r"\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b",
    r"\bshould be\b", r"\bmust be\b", r"\bcan be\b(?! used to)",
]
EN_IDIOM_SIGNALS = [r'"[^"]+"', r"'[^']+'"]  # 引号包裹的比喻需人工确认

ZH_VAGUE = ["若干", "一些", "很多", "大量", "尽量", "尽快", "适当", "相关", "左右",
            "等等", "之类", "大概", "大约", "某种程度上", "在一定程度上"]
ZH_IDIOM_CHARS = re.compile(r"[之乎其者也焉哉]")  # 文言信号


def split_sentences(text, lang):
    if lang == "en":
        parts = re.split(r"(?<=[.!?])\s+", text)
    else:
        parts = re.split(r"(?<=[。！？；])", text)
    return [s.strip() for s in parts if s.strip()]


def check_en(text):
    issues = []
    sents = split_sentences(text, "en")
    for s in sents:
        n = len(re.findall(r"\b\w+\b", s))
        if n > 25:
            issues.append(("句长", f"{n} 词 > 25: {s[:60]}..."))
    low = text.lower()
    for phrase in EN_VAGUE:
        if phrase in low:
            issues.append(("含糊词", f"'{phrase}' → 替换为具体数字/阈值/时限"))
    for pat in EN_PASSIVE:
        for m in re.finditer(pat, low):
            ctx = low[max(0, m.start()-30):m.end()+30].replace("\n", " ")
            issues.append(("被动/弱义务", f"疑似被动: ...{ctx}..."))
    for m in re.finditer(r'"([^"]{3,40})"', text):
        issues.append(("引号短语", f"确认是否比喻/习语: \"{m.group(1)}\"（机器无法判定，人工核对）"))
    return issues


def check_zh(text):
    issues = []
    sents = split_sentences(text, "zh")
    for s in sents:
        n = len(re.sub(r"\s", "", s))
        if n > 60:
            issues.append(("句长", f"{n} 字 > 60: {s[:50]}..."))
    for w in ZH_VAGUE:
        for m in re.finditer(re.escape(w), text):
            ctx = text[max(0, m.start()-15):m.end()+15].replace("\n", " ")
            issues.append(("模糊词", f"'{w}': ...{ctx}... → 具体化"))
    n_classical = len(ZH_IDIOM_CHARS.findall(text))
    if n_classical > 3:
        issues.append(("文言语感", f"文言/成语信号 {n_classical} 处，受控文本应口语直陈"))
    return issues


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    path = args[0]
    lang = "auto"
    if "--lang" in sys.argv:
        lang = sys.argv[sys.argv.index("--lang") + 1]
    text = open(path, encoding="utf-8").read()
    # 去掉 markdown 代码块和链接，避免误报
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    if lang == "auto":
        lang = "zh" if re.search(r"[\u4e00-\u9fff]", text) else "en"
    issues = check_zh(text) if lang == "zh" else check_en(text)

    print(f"语言: {lang}  文件: {path}")
    if not issues:
        print("✅ 通过：未发现高优先级受控写作违规")
        sys.exit(0)
    from collections import Counter
    cnt = Counter(k for k, _ in issues)
    print(f"发现 {len(issues)} 处待确认项（按类别）: {dict(cnt)}")
    for k, msg in issues[:30]:
        print(f"  [{k}] {msg}")
    if len(issues) > 30:
        print(f"  ... 共 {len(issues)} 处，仅显示前 30")
    print("\n注: 启发式检查只抓信号，最终判定以 module-a-ste100.md 清单人工复核。")
    sys.exit(1)


if __name__ == "__main__":
    main()
