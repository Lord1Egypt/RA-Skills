#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup_boundary.py — 清除「相邻片段边界重复」

【问题】滑动窗口切片会让相邻片段边界重叠 1–2 段，两片各译一遍 →
        合并后同一段出现两次（实测：8 处，每处 1–2 句）。

【策略】保留前一片 A 的完整译文，删除后一片 B 开头的重复段：
        · 纯重复句        → 整行删除
        · 页边码 + 重复句 → 只保留页边码（页码是核校锚点，不能丢）

【安全】默认 dry-run 只报告不写盘；确认无误后加 --apply 才修改。

用法:
    python dedup_boundary.py <chunks_dir>              # 试运行，只报告
    python dedup_boundary.py <chunks_dir> --apply      # 实际修复

【重要】删除前务必先排除「源文本身的结构性重复」：
        纲要条目 + 正文节标题可能文字相同（如著作纲要的 "I. xxx" 与
        正文中舒展字体的节标题 "I. xxx"），那不是缺陷，不可删！
        判据：回查源文 .txt，看该句是否真的出现两次。
"""
import re
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _common import die, warn, opt, ensure_chunks, safe_read
except ImportError:
    print("[出错] 找不到 _common.py —— 请确保它与本脚本在同一目录（scripts/）。",
          file=sys.stderr)
    sys.exit(1)

# ==================== CONFIG ====================
PAGE = re.compile(r'〔S\.\s*\d+\s*〕')
# 只有这三个才算「注释节」；#### 四级小节标题属于正文，不可据此截断
NOTE_KEYS = ("原注", "译注", "新术语")
MINLEN = 15          # 短于此长度的短行不参与重复判定
SCAN_HEAD = 60       # 只扫描 B 的开头 N 行（重复只可能出现在开头）
# ================================================


def is_note(line):
    s = line.strip()
    return s.startswith("#### ") and any(k in s for k in NOTE_KEYS)


def strip_page(s):
    return PAGE.sub('', s).strip()


def body_lines(path):
    """取正文行（遇到 原注/译注/新术语 节即止）。"""
    out = []
    for l in open(path, encoding="utf-8", errors="ignore").read().split("\n"):
        if is_note(l):
            break
        out.append(l)
    return out


def collapse_blanks(lines):
    out = []
    for l in lines:
        if l.strip() == "" and out and out[-1].strip() == "":
            continue
        out.append(l)
    return out


def dedup_pair(a_path, b_path, apply=False):
    """返回 (删除行数, 保留页边码数, 明细list)"""
    a_body = body_lines(a_path)
    a_norm = {strip_page(l.strip()) for l in a_body if len(l.strip()) >= MINLEN}

    B = open(b_path, encoding="utf-8").read().split("\n")
    out = []
    in_body, cnt = True, 0
    removed = kept_page = 0
    details = []

    for l in B:
        s = l.strip()
        if is_note(l):
            in_body = False
        if (in_body and cnt < SCAN_HEAD and len(s) >= MINLEN
                and not s.startswith(">")      # 承前页残句：必要，不删
                and not s.startswith("#")):    # 标题：不删
            core = strip_page(s)
            if core and core in a_norm:
                pages = PAGE.findall(s)
                if pages:
                    out.append("".join(pages))       # 只留页边码
                    kept_page += 1
                    details.append(("保留页边码", "".join(pages), s[:45]))
                else:
                    removed += 1
                    details.append(("删除", "", s[:45]))
                    cnt += 1
                    continue                          # ← 关键：不再 append 原行
        out.append(l)
        cnt += 1

    if apply and (removed or kept_page):
        open(b_path, "w", encoding="utf-8").write("\n".join(collapse_blanks(out)))
    return removed, kept_page, details


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n示例：python dedup_boundary.py output/chunks")
        sys.exit(1)
    chunks_dir = sys.argv[1]
    apply = "--apply" in sys.argv

    # 目录校验：路径写错时必须报错，不能静默输出「✅ 未发现边界重复」这种假通过
    files = ensure_chunks(chunks_dir, ".md")
    files = [f for f in files
             if not os.path.basename(f).startswith("04_index")]
    if apply and files:
        warn("即将修改磁盘文件。建议先备份 output/chunks/，或确认已纳入版本控制。")

    print(f"=== 边界重复{'修复' if apply else '检测（dry-run）'}：{len(files)} 个片段 ===\n")
    total_r = total_k = 0
    hit_pairs = 0

    for a, b in zip(files, files[1:]):
        na, nb = os.path.basename(a), os.path.basename(b)
        # 只在同一「部」内比较（01_phil / 02_theol ...）
        if "_".join(na.split("_")[:2]) != "_".join(nb.split("_")[:2]):
            continue
        r, k, det = dedup_pair(a, b, apply=apply)
        if r or k:
            hit_pairs += 1
            total_r += r
            total_k += k
            print(f"【{na} ⟷ {nb}】删除 {r} 行、保留页边码 {k} 处")
            for act, pg, txt in det:
                print(f"    {act}: {pg} {txt}…")
            print()

    if hit_pairs == 0:
        print("✅ 未发现边界重复。")
    else:
        print(f"{'已修复' if apply else '检测到'}：{hit_pairs} 对，删除 {total_r} 行，保留页边码 {total_k} 处")
        if not apply:
            print("\n确认无误后加 --apply 执行；删除前请回查源文，排除结构性重复（见文件头说明）。")


if __name__ == "__main__":
    main()
