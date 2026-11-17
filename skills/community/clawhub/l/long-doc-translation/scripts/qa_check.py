#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qa_check.py — 长篇翻译合并前质检（7 项）

用法:
    python qa_check.py <chunks_dir>

检查项:
    1 片段完整性        译文片段数与预期一致（可用 --expect N）
    2 体例三节          每片含 #### 原注 / #### 译注 / #### 新术语
    3 未译残留          正文无「>N 字符且无目标语言字符」的整行外文
    4 OCR 残痕          正文区错字 == 0（注释区豁免！见陷阱2）
    5 页边码连续        全稿页码无断档
    6 重复段            正文关键句重复（长行完全相同且出现 >1 次）
    7 空文件/占位       行数过少的文件
"""
import re
import sys
import os
import glob
from collections import Counter

# 友好错误提示：确保从任意目录运行都能找到同目录的 _common.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _common import die, warn, opt, ensure_chunks, safe_read
except ImportError:
    print("[出错] 找不到 _common.py —— 请确保它与本脚本在同一目录（scripts/）。",
          file=sys.stderr)
    sys.exit(1)

# ==================== CONFIG：按项目改这里 ====================
# 目标语言字符（中文）：用于判断「未译残留」
TARGET_LANG = re.compile(r'[\u4e00-\u9fff]')
# 页边码
PAGE_MARK = re.compile(r'〔S\.\s*(\d+)\s*〕|\[S\.\s*(\d+)\s*\]')
# 体例三节（每个片段必须有）
REQUIRED_SECTIONS = ("#### 原注", "#### 译注", "#### 新术语")
# OCR 错字映射 {标签: 正则} —— 只替换【正文区】，注释区豁免
OCR_TYPOS = {
    "ζ.B.(应为z.B.)": r'ζ\.\s*B\.',
    "Sdiell(应为Schell)": r'Sdiell',
    "Erkentnis(应为Erkenntnis)": r'Erkentnis',
    "Venunflsystematik": r'Venunflsystematik',
    "小写schleiermacher": r'schleiermacher',
    "孤立Audi(应为Auch)": r'(?<![A-Za-z])Audi(?![A-Za-z])',
    "§SO(应为§50)": r'§\s*SO\b',
    "sdiule(应为schule)": r'sdiule',
}
# 被视为「注释区」的标题关键词（其后的行豁免 OCR 替换 / 未译残留检查）
NOTE_HEADINGS = ("原注", "译注", "新术语")
# 不参与检查的文件（如出版社德文书目/广告页，按体例保留原文）
EXCLUDE_FILES = ("04_index_003.md",)
# 【重要】不参与「体例三节」检查的文件名前缀 —— 索引/书目/版权页等
# 只做格式整理、本身不是译文的文件，本就没有原注/译注/新术语。
# （实测：不豁免会把 4 个索引片误报为「缺节」）
SECTION_EXEMPT_PREFIX = ("04_index",)
# 页边码间隙分级（实测：切片边界常见 1–3 页的正常接缝，一律报警会淹没真问题）
#   间隙 <= SEAM_GAP  → 正常接缝（仅计数，不列明细）
#   间隙 >  SEAM_GAP  → 疑似断档（列明细，需人工核查）
SEAM_GAP = 3
# 未译残留判定：整行长度 > N 且无目标语言字符且含连续外文单词
MIN_UNTRANSLATED_LEN = 60
LATIN_WORD = re.compile(r'[A-Za-z]{4,}')
# 空文件/占位判定
MIN_LINES = 15
# 重复段判定：行长度阈值
DUP_MIN_LEN = 25
# =============================================================


def in_note_flags(lines):
    """返回每行是否位于 #### 原注/译注/新术语 区内。

    【关键】注释区豁免：译注里常写「原文 ζ.B. 应为 z.B.」——这是正确的
    纠错说明，绝不能被批量替换掉。
    """
    flags = [False] * len(lines)
    cur = False
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("#### "):
            cur = any(k in s for k in NOTE_HEADINGS)
            continue
        if s.startswith("##") or s.startswith("# "):   # 大标题切分
            cur = False
            continue
        flags[i] = cur
    return flags


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n示例：python qa_check.py output/chunks --expect 140")
        sys.exit(1)
    chunks_dir = sys.argv[1]
    expect = opt(sys.argv[1:], "--expect", default=None, cast=int,
                 usage="python qa_check.py <chunks_dir> --expect 140")

    # 目录校验：路径写错时必须报错退出，绝不能静默输出「0 个片段 + 全绿 ✅」
    files = ensure_chunks(chunks_dir, ".md", extra_skip=EXCLUDE_FILES)
    print(f"=== 翻译质检报告：{len(files)} 个片段 ===\n")

    # ---- 1 完整性 ----
    print("【1】片段完整性")
    print(f"  实际片段数：{len(files)}" +
          (f"；预期：{expect} → {'✅ 一致' if len(files)==expect else '❌ 不一致'}"
           if expect else "（未指定预期，加 --expect N 可校验）"))

    missing_sec, small_files = [], []
    untranslated, ocr_body, dup_counter = [], [], Counter()
    all_pages = []
    exempt_count = 0

    for f in files:
        name = os.path.basename(f)
        text = safe_read(f)
        lines = text.split("\n")
        flags = in_note_flags(lines)

        # ---- 2 体例三节（索引/格式件豁免）----
        if name.startswith(SECTION_EXEMPT_PREFIX):
            exempt_count += 1
        else:
            for sec in REQUIRED_SECTIONS:
                if sec not in text:
                    missing_sec.append((name, sec))

        # ---- 7 空文件/占位 ----
        if len(lines) < MIN_LINES:
            small_files.append((name, len(lines)))

        for i, (l, is_note) in enumerate(zip(lines, flags)):
            s = l.strip()
            if not s or s.startswith("#") or s.startswith(">"):
                continue
            if PAGE_MARK.search(s):
                continue
            if is_note:
                continue

            # ---- 3 未译残留 ----
            if (len(s) > MIN_UNTRANSLATED_LEN and not TARGET_LANG.search(s)
                    and LATIN_WORD.search(s)):
                untranslated.append((name, i + 1, s[:80]))

            # ---- 4 OCR 残痕（仅正文区）----
            for label, pat in OCR_TYPOS.items():
                if re.search(pat, s):
                    ocr_body.append((name, i + 1, label, s[:70]))

            # ---- 6 重复段 ----
            if len(s) >= DUP_MIN_LEN:
                dup_counter[s] += 1

    # 页边码连续性（跨文件汇总）
    for f in files:
        text = safe_read(f)
        nums = []
        for m in PAGE_MARK.finditer(text):
            g = m.group(1) or m.group(2)
            if g:
                nums.append(int(g))
        if nums:
            all_pages.append((os.path.basename(f), nums[0], nums[-1]))

    print("\n【2】体例三节（原注/译注/新术语）")
    print(f"  （豁免 {exempt_count} 个索引/格式件：{SECTION_EXEMPT_PREFIX}）")
    if missing_sec:
        print(f"  ❌ {len(missing_sec)} 处缺失：")
        for n, s in missing_sec[:20]:
            print(f"     {n} 缺 {s}")
        print("  修复：在文件末尾补 `#### 新术语` + `（无）`；缺原注则插在译注节之前。")
    else:
        print("  ✅ 全部译文片段齐全")

    print("\n【3】未译残留（正文长行无中文）")
    if untranslated:
        print(f"  ⚠ {len(untranslated)} 处（先确认是否属应保留原文的 书目/索引/广告页）：")
        for n, i, s in untranslated[:20]:
            print(f"     {n}:{i} | {s}")
    else:
        print("  ✅ 无")

    print("\n【4】正文 OCR 残痕（注释区豁免）")
    if ocr_body:
        print(f"  ❌ 正文区 {len(ocr_body)} 处，需修正：")
        for n, i, lbl, s in ocr_body[:30]:
            print(f"     {n}:{i} [{lbl}] | {s}")
    else:
        print("  ✅ 正文区无残痕（注释区的纠错说明已正确豁免）")

    print("\n【5】页边码连续性（分级：接缝 / 断档）")
    seams, gaps = [], []
    for a, b in zip(all_pages, all_pages[1:]):
        # 跨索引/格式件不比较（页码体系不同）
        if (a[0].startswith(SECTION_EXEMPT_PREFIX)
                or b[0].startswith(SECTION_EXEMPT_PREFIX)):
            continue
        d = b[1] - a[2] - 1          # 中间缺失的页数
        if d > SEAM_GAP:
            gaps.append((a[0], a[2], b[0], b[1], d))
        elif d > 0:
            seams.append((a[0], a[2], b[0], b[1], d))
    print(f"  · 正常接缝（缺 1–{SEAM_GAP} 页，切片边界常见）：{len(seams)} 处，无需处理")
    if gaps:
        print(f"  ⚠ 疑似断档（缺 >{SEAM_GAP} 页）：{len(gaps)} 处，需人工核查：")
        for n1, e1, n2, s2, d in gaps[:15]:
            print(f"     {n1} 止 S.{e1} → {n2} 起 S.{s2}  （缺 {d} 页）")
    else:
        print(f"  ✅ 无 >{SEAM_GAP} 页的断档")

    print("\n【6】重复段（相同长行出现 >1 次）")
    dups = [(s, c) for s, c in dup_counter.items() if c > 1]
    if dups:
        print(f"  ⚠ {len(dups)} 条（术语表/列表项重复属正常；正文句重复需核查是否切片重叠）：")
        for s, c in sorted(dups, key=lambda x: -x[1])[:15]:
            print(f"     {c}× : {s[:70]}")
    else:
        print("  ✅ 无重复")

    print("\n【7】空文件/占位文件")
    if small_files:
        print(f"  ❌ {len(small_files)} 个文件行数 < {MIN_LINES}（疑似未译/占位）：")
        for n, c in small_files:
            print(f"     {n}: {c} 行")
    else:
        print("  ✅ 无")

    print("\n=== 结束 ===")
    print("提示：发现切片重叠请用 overlap_check.py，修复后再跑 merge_build.py。")


if __name__ == "__main__":
    main()
