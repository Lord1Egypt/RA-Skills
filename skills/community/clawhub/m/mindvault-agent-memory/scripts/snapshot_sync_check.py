#!/usr/bin/env python3
"""MindVault — 双文档联动核账校验（snapshot_sync_check）

Layer 3 项目快照产出双文档：PROJECT_SNAPSHOT.md（唯一真相源）+ PROJECT.md（详细版）。
「关键字段 diff 通过」不等于真正同步：实测出现过更新日志条数不等、同日期条目重复、
同日期文本漂移、章节正文残留旧事实等断裂。本脚本对两文档做六维核账，
发现断裂即返回非 0 退出码，供 Agent 在联动更新后强制自检。

六项校验：
  1. 更新日志条数对照    — 两文档条目数必须相同
  2. 日期序列逐条比对    — 逐条日期必须一致
  3. 逐字一致性          — 每条「日期 + 更新内容」文本必须逐字一致
  4. 倒序校验            — 两文档更新日志必须严格倒序（日期非递增）
  5. 章节标题集合差异    — 二/三级标题集合必须一致（已登记的有意差异除外）
  6. 头部元数据差异      — 数据来源 / 生成方式 / 生成日期 / 最近更新 必须一致

已登记的有意差异（不计为断裂）：
  - 第十五章标题：「对外索引」（快照）vs「面向评审与语言 Agent」（详细版），
    含其 15.x 子标题，属设计上的有意精简（快照为对外索引表，详细版为评审展开）。

退出码：
  0 = 通过；1 = 发现断裂；2 = 入参 / 文件错误（文件不存在、更新日志表缺失）

用法：
  python3 snapshot_sync_check.py --snapshot PROJECT_SNAPSHOT.md --detail PROJECT.md
  python3 snapshot_sync_check.py            # 默认取当前目录下的两文件
  python3 snapshot_sync_check.py --help
"""

import argparse
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

LOG_HEADING_RE = re.compile(r"^##\s*更新日志\s*$")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# 已登记的有意差异：第十五章（快照侧「对外索引」/ 详细版「面向评审与语言 Agent」）
INTENTIONAL_H2_RE = re.compile(r"^十五、")
INTENTIONAL_H3_RE = re.compile(r"^15\.")
HEAD_KEYS = ("数据来源", "生成方式", "生成日期", "最近更新")


def read_lines(path):
    """按行读取文本文件（容错解码）。"""
    return Path(path).read_text(encoding="utf-8", errors="replace").splitlines()


def parse_update_log(lines):
    """解析「## 更新日志」下的 Markdown 表格。

    返回 [(日期, 更新内容), ...]；文档中不存在该章节时返回 None。
    """
    start = None
    for idx, line in enumerate(lines):
        if LOG_HEADING_RE.match(line.strip()):
            start = idx
            break
    if start is None:
        return None

    entries = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        # 跳过表头行与分隔行
        if cells[0] == "日期" or set(cells[0]) <= set("-: "):
            continue
        entries.append((cells[0], cells[1]))
    return entries


def parse_headings(lines):
    """收集二 / 三级标题（跳过代码块内内容）。"""
    h2, h3 = [], []
    in_fence = False
    for line in lines:
        stripped = line.rstrip()
        if stripped.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("### "):
            h3.append(stripped[4:].strip())
        elif stripped.startswith("## "):
            h2.append(stripped[3:].strip())
    return h2, h3


def parse_head_meta(lines):
    """解析头部引用块中的元数据（数据来源 / 生成方式 / 生成日期 / 最近更新）。"""
    meta = {}
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith(">"):
            continue
        for key in ("数据来源", "生成方式"):
            if key in meta:
                continue
            matched = re.match(r"^>\s*" + key + r"：\s*(.+?)\s*$", stripped)
            if matched:
                meta[key] = matched.group(1)
        if "生成日期" not in meta:
            matched = re.match(r"^>\s*生成日期：\s*(.+?)\s*$", stripped)
            if matched:
                body = matched.group(1)
                inner = re.match(r"^(.+?)（最近更新：\s*(.+?)）$", body)
                if inner:
                    meta["生成日期"] = inner.group(1).strip()
                    meta["最近更新"] = inner.group(2).strip()
                else:
                    meta["生成日期"] = body.strip()
    return meta


def date_key(text):
    """从日期单元格提取 YYYY-MM-DD；提取不到返回 None。"""
    matched = DATE_RE.search(text or "")
    return matched.group(1) if matched else None


def split_intentional(headings, pattern):
    """把标题列表拆成 (常规, 已登记有意差异)。"""
    normal, intentional = [], []
    for item in headings:
        (intentional if pattern.match(item) else normal).append(item)
    return normal, intentional


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="snapshot_sync_check.py",
        description="MindVault 双文档联动核账校验：校验 PROJECT_SNAPSHOT.md 与 PROJECT.md 是否真正同步。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python3 snapshot_sync_check.py --snapshot PROJECT_SNAPSHOT.md --detail PROJECT.md\n"
            "  python3 snapshot_sync_check.py            # 默认取当前目录下两文件\n"
            "\n"
            "退出码：0 = 通过；1 = 存在断裂；2 = 入参 / 文件错误\n"
        ),
    )
    parser.add_argument("--snapshot", default="PROJECT_SNAPSHOT.md",
                        help="唯一真相源文档路径（默认 PROJECT_SNAPSHOT.md）")
    parser.add_argument("--detail", default="PROJECT.md",
                        help="详细版文档路径（默认 PROJECT.md）")
    args = parser.parse_args(argv)

    snap_path = Path(args.snapshot).expanduser().resolve()
    detail_path = Path(args.detail).expanduser().resolve()

    out = []
    out.append("=== MindVault 双文档联动核账校验 v%s ===" % VERSION)
    out.append("snapshot: %s" % snap_path)
    out.append("detail  : %s" % detail_path)
    out.append("（快照为唯一真相源，冲突以快照为准）")
    out.append("")

    for path in (snap_path, detail_path):
        if not path.is_file():
            sys.stderr.write("[错误] 文件不存在：%s\n" % path)
            return 2

    snap_lines = read_lines(snap_path)
    detail_lines = read_lines(detail_path)
    snap_log = parse_update_log(snap_lines)
    detail_log = parse_update_log(detail_lines)

    if snap_log is None or detail_log is None:
        missing = []
        if snap_log is None:
            missing.append(str(snap_path))
        if detail_log is None:
            missing.append(str(detail_path))
        sys.stderr.write("[错误] 未找到「## 更新日志」表格：%s\n" % "、".join(missing))
        return 2

    problems = []

    # [1] 更新日志条数对照
    out.append("[1/6] 更新日志条数对照")
    out.append("  snapshot: %d 条" % len(snap_log))
    out.append("  detail  : %d 条" % len(detail_log))
    if len(snap_log) == len(detail_log):
        out.append("  ✓ 条数一致")
    else:
        gap = abs(len(snap_log) - len(detail_log))
        out.append("  ✗ 条数不一致（差 %d 条）" % gap)
        problems.append("更新日志条数不一致：snapshot %d 条 / detail %d 条"
                        % (len(snap_log), len(detail_log)))
    out.append("")

    pair_count = min(len(snap_log), len(detail_log))

    # [2] 日期序列逐条比对
    out.append("[2/6] 日期序列逐条比对")
    date_diffs = [(i, snap_log[i][0], detail_log[i][0])
                  for i in range(pair_count) if snap_log[i][0] != detail_log[i][0]]
    if not date_diffs:
        out.append("  ✓ 前 %d 条日期逐条一致" % pair_count)
        if pair_count and len(snap_log) != len(detail_log):
            out.append("  ⚠ 条数不同，仅比对前 %d 条" % pair_count)
    else:
        out.append("  ✗ %d 条日期不一致：" % len(date_diffs))
        for idx, s_date, d_date in date_diffs[:10]:
            out.append("    第 %d 条：snapshot=%s / detail=%s" % (idx + 1, s_date, d_date))
        if len(date_diffs) > 10:
            out.append("    …（其余 %d 条略）" % (len(date_diffs) - 10))
        problems.extend("日期序列第 %d 条不一致" % (i + 1) for i, _, _ in date_diffs)
    out.append("")

    # [3] 逐字一致性
    out.append("[3/6] 逐字一致性（日期 + 更新内容）")
    text_diffs = [(i, snap_log[i], detail_log[i])
                  for i in range(pair_count) if snap_log[i] != detail_log[i]]
    if not text_diffs:
        out.append("  ✓ 前 %d 条逐字一致" % pair_count)
    else:
        out.append("  ✗ %d 条内容不一致：" % len(text_diffs))
        for idx, s_item, d_item in text_diffs[:5]:
            out.append("    第 %d 条：" % (idx + 1))
            out.append("      snapshot: %s | %s" % (s_item[0], s_item[1][:60]))
            out.append("      detail  : %s | %s" % (d_item[0], d_item[1][:60]))
        if len(text_diffs) > 5:
            out.append("    …（其余 %d 条略）" % (len(text_diffs) - 5))
        problems.extend("更新日志第 %d 条文本漂移" % (i + 1) for i, _, _ in text_diffs)
    out.append("")

    # [4] 倒序校验
    out.append("[4/6] 倒序校验（日期非递增）")
    order_ok = True
    for label, entries in (("snapshot", snap_log), ("detail", detail_log)):
        keys = [date_key(item[0]) for item in entries]
        if any(k is None for k in keys):
            out.append("  ⚠ %s：存在无法解析日期的条目，跳过倒序校验" % label)
            continue
        bad = [i for i in range(len(keys) - 1) if keys[i] < keys[i + 1]]
        if bad:
            out.append("  ✗ %s 非严格倒序，首次逆序在第 %d 条（%s → %s）"
                       % (label, bad[0] + 1, keys[bad[0]], keys[bad[0] + 1]))
            problems.append("%s 更新日志未严格倒序" % label)
            order_ok = False
        else:
            out.append("  ✓ %s 严格倒序（%d 条）" % (label, len(keys)))
    if not order_ok:
        pass
    out.append("")

    # [5] 章节标题集合差异
    out.append("[5/6] 章节标题集合差异")
    snap_h2, snap_h3 = parse_headings(snap_lines)
    detail_h2, detail_h3 = parse_headings(detail_lines)
    norm_snap_h2, intent_snap_h2 = split_intentional(snap_h2, INTENTIONAL_H2_RE)
    norm_detail_h2, intent_detail_h2 = split_intentional(detail_h2, INTENTIONAL_H2_RE)
    norm_snap_h3, intent_snap_h3 = split_intentional(snap_h3, INTENTIONAL_H3_RE)
    norm_detail_h3, intent_detail_h3 = split_intentional(detail_h3, INTENTIONAL_H3_RE)

    only_snap_h2 = sorted(set(norm_snap_h2) - set(norm_detail_h2))
    only_detail_h2 = sorted(set(norm_detail_h2) - set(norm_snap_h2))
    only_snap_h3 = sorted(set(norm_snap_h3) - set(norm_detail_h3))
    only_detail_h3 = sorted(set(norm_detail_h3) - set(norm_snap_h3))

    out.append("  snapshot: 二级 %d 项 / 三级 %d 项" % (len(snap_h2), len(snap_h3)))
    out.append("  detail  : 二级 %d 项 / 三级 %d 项" % (len(detail_h2), len(detail_h3)))
    if not (only_snap_h2 or only_detail_h2 or only_snap_h3 or only_detail_h3):
        out.append("  ✓ 二/三级标题集合一致")
    else:
        if only_snap_h2:
            out.append("  ✗ snapshot 独有二级标题：%s" % "；".join(only_snap_h2))
            problems.extend("snapshot 独有二级标题：%s" % t for t in only_snap_h2)
        if only_detail_h2:
            out.append("  ✗ detail 独有二级标题：%s" % "；".join(only_detail_h2))
            problems.extend("detail 独有二级标题：%s" % t for t in only_detail_h2)
        if only_snap_h3:
            out.append("  ✗ snapshot 独有三级标题：%s" % "；".join(only_snap_h3))
            problems.extend("snapshot 独有三级标题：%s" % t for t in only_snap_h3)
        if only_detail_h3:
            out.append("  ✗ detail 独有三级标题：%s" % "；".join(only_detail_h3))
            problems.extend("detail 独有三级标题：%s" % t for t in only_detail_h3)

    intent_h2_count = max(len(intent_snap_h2), len(intent_detail_h2))
    intent_h3_count = max(len(intent_snap_h3), len(intent_detail_h3))
    if intent_h2_count or intent_h3_count:
        out.append("  ℹ 已登记有意差异（第十五章，不计断裂）：二级 %d 项 / 三级 %d 项"
                   % (intent_h2_count, intent_h3_count))
        out.append("    snapshot 二级：%s" % "；".join(intent_snap_h2))
        out.append("    detail   二级：%s" % "；".join(intent_detail_h2))
    out.append("")

    # [6] 头部元数据差异
    out.append("[6/6] 头部元数据差异")
    snap_meta = parse_head_meta(snap_lines)
    detail_meta = parse_head_meta(detail_lines)
    meta_ok = True
    for key in HEAD_KEYS:
        s_val = snap_meta.get(key)
        d_val = detail_meta.get(key)
        if s_val is None or d_val is None:
            out.append("  ✗ %s：%s" % (key, "snapshot 缺失" if s_val is None else "detail 缺失"))
            problems.append("头部元数据缺失：%s" % key)
            meta_ok = False
        elif s_val != d_val:
            out.append("  ✗ %s：snapshot=%s / detail=%s" % (key, s_val, d_val))
            problems.append("头部元数据不一致：%s" % key)
            meta_ok = False
        else:
            out.append("  ✓ %s：%s" % (key, s_val))
    if not meta_ok:
        pass
    out.append("")

    out.append("─" * 46)
    print("\n".join(out))

    if problems:
        print("结果：FAIL — 发现 %d 处断裂：" % len(problems))
        for item in problems:
            print("  - %s" % item)
        print("断裂未清零前，禁止结束联动更新（见 SKILL.md Layer 3 双文档联动与核账校验）。")
        return 1

    print("结果：PASS — 六项校验全部通过，双文档未发现联动断裂")
    return 0


if __name__ == "__main__":
    sys.exit(main())
