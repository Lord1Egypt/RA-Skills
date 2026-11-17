#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
overlap_check.py — 长篇翻译「切片重叠检测」

【为什么必须在翻译开工前跑】
长文本按滑动窗口/字符数切片时，相邻片段边界常常重叠。若两个片段是
「父集 / 子集」关系而各自被完整翻译一遍，合并后同一段会出现两次，
且极难在通读时发现（本次实战：024 是 023 的子集窗口，导致 12 页重复）。

用法:
    python overlap_check.py <chunks_dir>            # 扫描译文 *.md 的页边码
    python overlap_check.py <chunks_dir> --src work/chunks --ext .txt
                                                    # 扫描源切片（无页边码时退化为字符数比对）

输出: 每个片段的页码覆盖区间，以及相邻重叠告警。
"""
import re
import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _common import die, warn, opt, ensure_chunks, safe_read
except ImportError:
    print("[出错] 找不到 _common.py —— 请确保它与本脚本在同一目录（scripts/）。",
          file=sys.stderr)
    sys.exit(1)

# ==================== CONFIG：按项目改这里 ====================
# 页边码正则（译文里通常形如 〔S. 123〕 / [S. 123] / 〔S.123〕）
PAGE_MARK = re.compile(r'〔S\.\s*(\d+)\s*〕|\[S\.\s*(\d+)\s*\]')
# 忽略这些目录（如冗余备份）
EXCLUDE_DIRS = {"_redundant", "_backup", ".git"}
# 【重要】分组比较：只在同一「部/篇」内部比较页码连续性。
# 不同部（正文 vs 索引/附录）的页码本就不连续，跨部比较必然误报。
# 分组规则：取文件名前两段，如 01_phil_018.md -> 01_phil
GROUP_RE = re.compile(r'^([A-Za-z0-9]+_[A-Za-z0-9]+)_')
# 【重要】索引/引用型片段：其页边码是「条目引用页码」而非正文顺序
# （实测：索引片出现 S.392–S.216 这种首页>尾页的逆序）。此类跳过比较。
SKIP_REVERSED = True
# =============================================================


# 命名不匹配 GROUP_RE 时统一归入此组。
# 【关键】绝不能退化为「每个文件自成一组」——那样组内只有 1 片，
# 相邻比较一次都不会发生，脚本会打印「✅ 未发现重叠」而实际什么都没查（静默假通过）。
FALLBACK_GROUP = "_all"


def group_key(name):
    m = GROUP_RE.match(name)
    return m.group(1) if m else FALLBACK_GROUP


def page_range(text):
    """返回 (首页码, 尾页码)；无页边码返回 (None, None)。"""
    nums = []
    for m in PAGE_MARK.finditer(text):
        g = m.group(1) or m.group(2)
        if g:
            nums.append(int(g))
    if not nums:
        return (None, None)
    return (nums[0], nums[-1])


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        print("\n示例：python overlap_check.py output/chunks")
        sys.exit(1)

    chunks_dir = args[0]
    ext = opt(args, "--ext", default=".md", cast=str,
              usage="python overlap_check.py <chunks_dir> --ext .txt")
    if ext and not ext.startswith("."):
        ext = "." + ext          # 容错：写 --ext txt 也能用

    files = ensure_chunks(chunks_dir, ext)
    files = [f for f in files if not any(d in f for d in EXCLUDE_DIRS)]

    if not files:
        die(f"排除目录 {sorted(EXCLUDE_DIRS)} 后没有剩余文件：{chunks_dir}",
            "检查脚本顶部的 EXCLUDE_DIRS 配置是否把目标文件都排除了。")

    # 按「部/篇」分组，只在组内比较（跨部页码本不连续）
    groups = {}
    for f in files:
        groups.setdefault(group_key(os.path.basename(f)), []).append(f)

    print(f"=== 切片覆盖与重叠检测（{len(files)} 个片段，{len(groups)} 部）===\n")

    # 命名模式自检：没有文件匹配「部_篇_编号」时，说明已退化为全序列比较
    matched = sum(1 for f in files if GROUP_RE.match(os.path.basename(f)))
    if matched == 0 and len(files) > 1:
        warn(f"没有文件名匹配「部_篇_编号」模式（如 01_phil_018.md），"
             f"已退化为「全部视为同一部」做全序列比较。\n"
             f"   若本项目确有多部（正文/索引/附录页码各自起算），请改用具名模式或调整 GROUP_RE，"
             f"否则跨部比较会误报。")

    has_page = False
    overlaps = []
    skipped = []
    compared = 0          # 实际发生过的相邻比较次数（用于识别「什么都没比」）

    for gname in sorted(groups):
        items = sorted(groups[gname])
        if len(items) == 1 and len(files) > 1:
            print(f"─ 部：{gname}   （仅 1 片，无相邻片可比较）")
        else:
            print(f"─ 部：{gname}")
        prev = None            # (name, first, last)
        for f in items:
            text = open(f, encoding="utf-8", errors="ignore").read()
            first, last = page_range(text)
            name = os.path.basename(f)

            if first is None:
                print(f"    {name}: 无页边码（{len(text)} 字符）")
                prev = None
                continue

            # 索引/引用型：首页 > 尾页（逆序）→ 页边码是引用页码，跳过
            if SKIP_REVERSED and first > last:
                print(f"    {name}: S.{first} – S.{last}  [索引/引用型，逆序，跳过比较]")
                skipped.append(name)
                prev = None
                continue

            has_page = True
            flag = ""
            if prev and prev[2] is not None:
                compared += 1          # 真正做过一次相邻比较
                if first <= prev[2]:
                    flag = (f"   <== 重叠！上一片尾 S.{prev[2]}，本片首 S.{first}"
                            f"（重叠约 {prev[2]-first+1} 页）")
                    overlaps.append((prev[0], name, first, prev[2]))
            print(f"    {name}: S.{first} – S.{last}{flag}")
            prev = (name, first, last)
        print()

    print()
    if not has_page:
        print("⚠ 所有片段均无页边码，无法做内容重叠判定。")
        print("  建议：译文务必保留原书页边码（如 〔S. 123〕），这是检测重叠与断档的唯一可靠锚点。")
        sys.exit(0)

    if compared == 0 and len(files) > 1:
        # 每组都只有 1 片 → 一次相邻比较都没发生，此时「未发现重叠」是假结论
        print("⚠ 未对任何相邻片段做过比较（每个分组都只有 1 个片段）。")
        print("  本次「未发现重叠」不成立，请勿据此放行。")
        print("  处理：统一命名后重跑；若确实是多部结构，用「部_篇_编号」命名或改 GROUP_RE。")
        sys.exit(3)

    if overlaps:
        print(f"❌ 发现 {len(overlaps)} 处相邻片段重叠：\n")
        for a, b, s, e in overlaps:
            print(f"   {a} ⟷ {b}  →  重叠区间约 S.{s}–S.{e}")
        print("\n处理建议：")
        print("  1) 比较两片，确认谁是「超集」（覆盖页数多者通常为正本）；")
        print("  2) 把子集片的【独有内容】（新术语条目、独有注解）并入超集片；")
        print("  3) 子集片移入 <chunks_dir>/_redundant/ ，不参与合并；")
        print("  4) 重新合并后，用 qa_check.py 复查正文关键句出现次数 == 1。")
        sys.exit(2)
    else:
        print("✅ 未发现相邻片段重叠，可以继续翻译 / 合并。")


if __name__ == "__main__":
    main()
