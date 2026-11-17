#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 2 —— 台本 + 词级 ASR -> 精确时间轴

用法:
    python align_gen.py <script.txt> <words.txt> <out_ja.srt>

原理:
  字幕「文本」100% 取自台本（零识别错误），只让 ASR 负责「什么时候说」。
  把台本与 ASR 各自归一化成字符流，用 SequenceMatcher 求字符级匹配，
  再把匹配到的字符映射回 ASR 的 word 时间戳（词内按字符位置线性插值）。
  未命中的行用相邻已知行插值补齐，最后做单调化 + 最小时长保护。

关键: 序号必须是「台本非空行」连续编号（1-based），翻译字典要和它对齐。
"""
import re, difflib, sys

if len(sys.argv) < 4:
    sys.exit(__doc__)
script, words, out = sys.argv[1], sys.argv[2], sys.argv[3]

MIN_DUR = 0.7                     # 单条字幕最短时长（秒）
DROP = re.compile(r"[^ぁ-んァ-ヶー一-龥々〆a-zA-Z0-9]")


def norm(s):
    """只保留可用于比对的字形"""
    return DROP.sub("", s)


# ---------- 台本 ----------
lines, line_chars = [], []
for raw in open(script, encoding="utf-8"):
    line = raw.strip()
    if not line:
        continue
    lines.append(line)
    line_chars.append(norm(line))
script_full = "".join(line_chars)

# ---------- ASR（词级） ----------
wlist = []
for raw in open(words, encoding="utf-8"):
    if not raw.strip():
        continue
    a, b, t = raw.rstrip("\n").split("\t", 2)
    chs = norm(t)
    if chs:
        wlist.append((float(a), float(b), chs))

asr_full, char_word, word_span = "", [], []
pos = 0
for wi, (a, b, chs) in enumerate(wlist):
    asr_full += chs
    char_word.extend([wi] * len(chs))
    word_span.append((pos, pos + len(chs)))
    pos += len(chs)

# ---------- 字符级对齐 ----------
sm = difflib.SequenceMatcher(None, asr_full, script_full, autojunk=False)
char_map = {}                     # 台本字符位置 -> ASR 字符位置
for ia, isc, n in sm.get_matching_blocks():
    for k in range(n):
        char_map[isc + k] = ia + k


def time_at(p, is_end=False):
    if p is None or not char_word:
        return 0.0
    wi = char_word[min(p, len(char_word) - 1)]
    t0, t1 = wlist[wi][0], wlist[wi][1]
    cs, ce = word_span[wi]
    frac = (p - cs + (1 if is_end else 0)) / max(ce - cs, 1)
    return t0 + min(max(frac, 0.0), 1.0) * (t1 - t0)


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ---------- 每行分配时间 ----------
p = 0
resolved = []
for li, chs in enumerate(line_chars):
    s0, s1 = p, p + len(chs)
    p = s1
    hits = [char_map[i] for i in range(s0, s1) if i in char_map]
    if hits:
        resolved.append((time_at(min(hits)), time_at(max(hits), True), li))
    else:
        resolved.append((None, None, li))

for i, (a, b, li) in enumerate(resolved):
    if a is None:
        prev_end = next((resolved[j][1] for j in range(i - 1, -1, -1)
                         if resolved[j][1] is not None), wlist[0][0])
        next_start = next((resolved[j][0] for j in range(i + 1, len(resolved))
                           if resolved[j][0] is not None), wlist[-1][1])
        resolved[i] = ((prev_end + next_start) / 2, next_start, li)

for i in range(1, len(resolved)):                      # 单调化
    if resolved[i][0] < resolved[i - 1][1]:
        resolved[i] = (resolved[i - 1][1], max(resolved[i][1], resolved[i - 1][1] + 0.4),
                       resolved[i][2])

for i in range(len(resolved)):                         # 最小时长
    a, b, li = resolved[i]
    if b - a < MIN_DUR:
        b = a + MIN_DUR
        if i + 1 < len(resolved) and b > resolved[i + 1][0]:
            b = resolved[i + 1][0]
        if b <= a:
            b = a + MIN_DUR
        resolved[i] = (a, b, li)

with open(out, "w", encoding="utf-8") as f:
    for n, (a, b, li) in enumerate(resolved, 1):
        f.write(f"{n}\n{fmt(a)} --> {fmt(b)}\n{lines[li]}\n\n")

print("台本行数:", len(lines), "| ASR 词数:", len(wlist))
print("字符匹配率: %.1f%%" % (len(char_map) / max(len(script_full), 1) * 100))
print("输出:", out)
