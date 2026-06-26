#!/usr/bin/env python3
"""
对 Perfetto trace 文件执行 SQL 查询（通过 trace_processor）。

依赖: pip install perfetto

用法:
  python query_trace.py <trace.pftrace> "<SQL>"
  python query_trace.py <trace.pftrace> -f query.sql
  python query_trace.py <trace.pftrace> -f query.sql --csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="对 Perfetto trace 执行 SQL 查询（调用 trace_processor）"
    )
    parser.add_argument(
        "trace",
        type=Path,
        help="trace 文件路径（.pftrace / .perfetto-trace）",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-q", "--query",
        type=str,
        help="要执行的 SQL 字符串",
    )
    group.add_argument(
        "-f", "--file",
        type=Path,
        metavar="SQL_FILE",
        help="包含 SQL 的文件路径",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="输出 CSV（默认输出为制表符分隔）",
    )
    args = parser.parse_args()

    trace_path = args.trace.resolve()
    if not trace_path.exists():
        print(f"错误: trace 文件不存在: {trace_path}", file=sys.stderr)
        return 1

    if args.query:
        sql = args.query
    else:
        sql_path = args.file.resolve()
        if not sql_path.exists():
            print(f"错误: SQL 文件不存在: {sql_path}", file=sys.stderr)
            return 1
        sql = sql_path.read_text(encoding="utf-8", errors="replace").strip()

    if not sql:
        print("错误: SQL 为空", file=sys.stderr)
        return 1

    try:
        from perfetto.trace_processor import TraceProcessor
    except ImportError:
        print(
            "错误: 未安装 perfetto。请执行: pip install perfetto",
            file=sys.stderr,
        )
        return 1

    try:
        with TraceProcessor(trace=str(trace_path)) as tp:
            it = tp.query(sql)
            rows = list(it)
    except Exception as e:
        print(f"查询失败: {e}", file=sys.stderr)
        return 1

    if not rows:
        print("(无结果)")
        return 0

    # 从第一行推断列名（perfetto 返回的 row 通常支持 _asdict 或为 namedtuple）
    row0 = rows[0]
    if hasattr(row0, "_asdict"):
        columns = list(row0._asdict().keys())
    elif hasattr(row0, "_fields"):
        columns = list(row0._fields)
    elif isinstance(row0, dict):
        columns = list(row0.keys())
    else:
        columns = [k for k in dir(row0) if not k.startswith("_") and not callable(getattr(row0, k, None))]

    sep = "," if args.csv else "\t"
    if args.csv:
        print(sep.join(columns))
    for row in rows:
        if hasattr(row, "_asdict"):
            d = row._asdict()
        elif isinstance(row, dict):
            d = row
        else:
            d = {c: getattr(row, c, "") for c in columns}
        values = [str(d.get(c, "")) for c in columns]
        print(sep.join(values))

    return 0


if __name__ == "__main__":
    sys.exit(main())
