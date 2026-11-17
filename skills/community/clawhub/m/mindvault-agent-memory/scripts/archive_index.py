#!/usr/bin/env python3
"""MindVault — _index.json 管理工具（基础版 · 免费）

基础版命令：stats, pending
更多命令（mark / search / summary）需按版本核对，对照表见https://www.jinengpu.chat/mindvault-detail.html

子命令：
  stats      — 统计：文件数 / 总条目 / 轮次 / processed 比例
  pending    — 列出 processed=false 的文件
  mark       — （赞赏版）将指定文件标记为 processed=true，写入前做 if_version 读前校验
  search     — （赞赏版）按日期/轮次范围搜索文件
  summary    — （赞赏版）输出 JSON 摘要（供 Agent 消费）

写入纪律（B9/B15，适用于写入类操作）：
  - 写入类操作（mark）必须先确认 _index.json 存在（不存在即异常），
    禁止在索引缺失时静默创建或静默返回空。
  - 每次写索引 index_version +1，作为乐观版本令牌；
    并发/多端写入前应先读取并核对 version，避免覆盖他人写入。

用法（基础版）：
  python archive_index.py <archive_dir> stats
  python archive_index.py <archive_dir> pending
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def parse_rounds(f: dict):
    """从归档文件条目解析轮次区间，返回 (start, end) 或 None。

    兼容 archive_export 实际写入的 rounds 字符串（如 "16-30"），
    并向后兼容的 round_start / round_end 数字字段。
    """
    rs = f.get("rounds")
    if rs and isinstance(rs, str) and "-" in rs:
        try:
            a, b = rs.split("-")
            return int(a), int(b)
        except ValueError:
            pass
    if "round_start" in f or "round_end" in f:
        return int(f.get("round_start", 0) or 0), int(f.get("round_end", 0) or 0)
    return None


def load_index(index_dir: str) -> dict:
    """从 index_dir 往上溯一层找 _index.json，找不到则返回空结构。"""
    # 支持传入子目录（如 archive_dir/conv_label）或 archive_dir 本身
    path = Path(index_dir)
    candidates = [path / "_index.json", path.parent / "_index.json"]
    for p in candidates:
        if p.exists():
            with open(p, "r") as f:
                return json.load(f)
    return {}


def save_index(index_dir: str, data: dict):
    path = Path(index_dir)
    if path.is_dir():
        out = path / "_index.json"
    else:
        out = path.parent / "_index.json"
    with open(out, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def cmd_stats(index_dir: str):
    idx = load_index(index_dir)
    files = idx.get("files", [])
    total_entries = sum(f.get("entries", 0) for f in files)
    total_rounds = sum(f.get("round_count", f.get("entries", 0)) for f in files)
    # 消息数 = 每条 JSONL 记录（entries）即为一条消息；兼容旧 total_messages 字段
    total_msgs = sum(f.get("total_messages", 0) or f.get("entries", 0) for f in files)
    processed = sum(1 for f in files if f.get("processed", False))
    pending = len(files) - processed

    print(f"文件数:       {len(files)}")
    print(f"已处理:       {processed}")
    print(f"未处理:       {pending}")
    print(f"总条目数:     {total_entries}")
    print(f"总轮次数:     {total_rounds}")
    print(f"总消息数:     {total_msgs}")
    print(f"处理比例:     {processed/len(files)*100:.1f}%" if files else "0.0%")


def cmd_pending(index_dir: str):
    idx = load_index(index_dir)
    files = idx.get("files", [])
    pending = [f for f in files if not f.get("processed", False)]
    if not pending:
        print("没有未处理的归档文件。")
        return
    print(f"未处理文件数: {len(pending)}")
    if len(pending) >= 5:
        print("⚠️  积压严重，建议执行进化引擎。")
    for f in pending:
        rr = parse_rounds(f)
        rng = f"{rr[0]:04d}-{rr[1]:04d}" if rr else f.get('rounds', '?')
        print(f"  - {f.get('file', '?')}  (rounds: {rng}, "
              f"round_count: {f.get('round_count', '?')}, "
              f"messages: {f.get('entries', '?')}, "
              f"date: {f.get('date', '?')})")


def cmd_mark(index_dir: str, filename: str, expect_version: int = None):
    """标记文件为 processed（B9 乐观版本令牌 + B15 不存在即异常）。

    expect_version：调用方在读取索引后携带的版本号；若与当前索引 version
    不一致，说明索引在你读取之后被其他端修改过，拒绝写入以避免覆盖。
    """
    idx = load_index(index_dir)
    if not idx:
        print(f"错误：未找到 _index.json（{index_dir}）——索引缺失时禁止静默写入。")
        sys.exit(1)
    files = idx.get("files", [])
    if not files:
        print("错误：_index.json 缺少 files 列表，索引结构异常。")
        sys.exit(1)
    current_version = idx.get("index_version", 0)
    if expect_version is not None and current_version != expect_version:
        print(f"冲突：索引版本已变化（期望 {expect_version}，当前 {current_version}）。"
              f"请重新读取索引核对后再写入，避免覆盖其他端的修改。")
        sys.exit(1)
    found = False
    for f in files:
        if f.get("file") == filename:
            f["processed"] = True
            f["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break
    if not found:
        print(f"错误：未找到文件 '{filename}'")
        sys.exit(1)
    idx["files"] = files
    idx["index_version"] = current_version + 1
    save_index(index_dir, idx)
    print(f"已标记: {filename}  (index_version {current_version} -> {idx['index_version']})")


def cmd_search(index_dir: str, date_str: str = None, rounds_range: str = None):
    idx = load_index(index_dir)
    files = idx.get("files", [])
    results = files

    if date_str:
        results = [f for f in results if f.get("date", "") == date_str]

    if rounds_range:
        try:
            lo, hi = rounds_range.split("-")
            lo, hi = int(lo), int(hi)
        except ValueError:
            print("错误：rounds 范围格式应为 '20-40'")
            sys.exit(1)
        # 解析 export 写入的 rounds 字符串（rounds: "16-30"）
        # P1-2 修复：区间重叠判定应为 `s <= hi and e >= lo`（含完全包含场景），
        # 旧版 `lo <= s <= hi or lo <= e <= hi` 漏掉「目标区间完全覆盖文件区间」的情形。
        matched = []
        for f in results:
            rr = parse_rounds(f)
            if rr is None:
                continue
            s, e = rr
            if s <= hi and e >= lo:
                matched.append(f)
        results = matched

    if not results:
        print("无匹配结果。")
        return
    for f in results:
        rr = parse_rounds(f)
        rng = f"{rr[0]:04d}-{rr[1]:04d}" if rr else f.get('rounds', '?')
        print(f"{f.get('file', '?')}  date={f.get('date','?')} "
              f"rounds=[{rng}] "
              f"entries={f.get('entries','?')}  msgs={f.get('entries','?')}  "
              f"processed={f.get('processed',False)}")


def cmd_summary(index_dir: str):
    idx = load_index(index_dir)
    summary = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_count": len(idx.get("files", [])),
        "total_entries": sum(f.get("entries", 0) for f in idx.get("files", [])),
        "total_messages": sum(f.get("total_messages", 0) or f.get("entries", 0) for f in idx.get("files", [])),
        "processed_count": sum(1 for f in idx.get("files", []) if f.get("processed", False)),
        "pending_count": sum(1 for f in idx.get("files", []) if not f.get("processed", False)),
        "date_range": {
            "earliest": min((f.get("date", "9999") for f in idx.get("files", []) if f.get("date")), default=None),
            "latest": max((f.get("date", "0000") for f in idx.get("files", []) if f.get("date")), default=None),
        },
        "pending_files": [
            f.get("file") for f in idx.get("files", []) if not f.get("processed", False)
        ],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    index_dir = sys.argv[1]
    cmd = sys.argv[2]
    args = sys.argv[3:]

    if cmd == "stats":
        cmd_stats(index_dir)
    elif cmd == "pending":
        cmd_pending(index_dir)
    elif cmd == "mark":
        print("mark 需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html）；本包开放 stats / pending")
        sys.exit(1)
    elif cmd == "search":
        print("search 需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html）；本包开放 stats / pending")
        sys.exit(1)
    elif cmd == "summary":
        print("summary 需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html）；本包开放 stats / pending")
        sys.exit(1)
    else:
        print(f"未知子命令: {cmd}")
        sys.exit(1)
