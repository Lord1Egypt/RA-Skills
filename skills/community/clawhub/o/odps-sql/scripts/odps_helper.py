#!/usr/bin/env python3
"""
ODPS 辅助脚本 - OpenClaw Skill 辅助工具
在 MCP 服务器不可用时，可直接通过命令行使用此脚本操作 ODPS。

依赖:
    pip install pyodps

配置方式（按优先级）：
    1. 系统环境变量（ALIYUN_ACCESS_KEY_ID 等）
    2. skill 目录下的 .env 文件（从 config.example.env 复制并填写）

.env 配置步骤：
    cd skill/
    cp config.example.env .env
    # 然后编辑 .env 填写你的凭证

用法:
    python odps_helper.py --list-tables [--pattern <filter>]
    python odps_helper.py --describe <table_name>
    python odps_helper.py --query "<SQL>" [--limit <n>]
"""

import os
import sys
import argparse

# ---- 配置加载：支持 .env 文件（无需第三方库） ----

def _load_dotenv():
    """
    从 .env 文件加载配置，加载路径按顺序查找：
      1. 当前工作目录下的 .env
      2. 脚本所在目录的上一级（skill/）目录下的 .env
    已有的环境变量不会被覆盖（系统/shell 设置优先）。
    """
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.path.dirname(__file__), "..", ".env"),
    ]
    for dotenv_path in candidates:
        dotenv_path = os.path.normpath(dotenv_path)
        if os.path.isfile(dotenv_path):
            with open(dotenv_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            return dotenv_path  # 返回实际加载的文件路径
    return None

_dotenv_loaded = _load_dotenv()


def get_odps_client():
    """初始化并返回 ODPS 客户端"""
    try:
        from odps import ODPS
    except ImportError:
        print("错误: 请先安装 pyodps: pip install pyodps", file=sys.stderr)
        sys.exit(1)

    access_id = os.environ.get("ALIYUN_ACCESS_KEY_ID")
    secret = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
    project = os.environ.get("ALIYUN_ODPS_PROJECT")
    endpoint = os.environ.get(
        "ALIYUN_ODPS_ENDPOINT",
        "http://service.cn-beijing.maxcompute.aliyun.com/api"
    )

    missing = [k for k, v in {
        "ALIYUN_ACCESS_KEY_ID": access_id,
        "ALIYUN_ACCESS_KEY_SECRET": secret,
        "ALIYUN_ODPS_PROJECT": project
    }.items() if not v]

    if missing:
        skill_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        dotenv_hint = os.path.join(skill_dir, ".env")
        example_hint = os.path.join(skill_dir, "config.example.env")
        if _dotenv_loaded:
            print(f"错误: 已加载 {_dotenv_loaded}，但仍缺少以下配置项：", file=sys.stderr)
        else:
            print("错误: 未找到配置文件，也未设置系统环境变量。", file=sys.stderr)
            print(f"\n请按以下步骤配置：", file=sys.stderr)
            print(f"  1. 复制配置模板: cp {example_hint} {dotenv_hint}", file=sys.stderr)
            print(f"  2. 编辑 .env 文件，填写以下字段：", file=sys.stderr)
        for key in missing:
            print(f"     - {key}", file=sys.stderr)
        sys.exit(1)

    return ODPS(
        access_id=access_id,
        secret_access_key=secret,
        project=project,
        endpoint=endpoint
    )


def cmd_list_tables(odps, pattern=None):
    """列出项目中的表"""
    try:
        tables = list(odps.list_tables())
        if pattern:
            tables = [t for t in tables if pattern.lower() in t.name.lower()]
        names = [t.name for t in tables]
        print(f"共找到 {len(names)} 张表:")
        for name in names:
            print(f"  - {name}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_describe(odps, table_name):
    """获取表结构"""
    try:
        table = odps.get_table(table_name)
        print(f"表: {table_name}")
        print(f"{'列名':<30} {'类型':<20} {'注释'}")
        print("-" * 70)
        for col in table.schema.columns:
            print(f"{col.name:<30} {str(col.type):<20} {col.comment or ''}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_query(odps, sql, limit=100):
    """执行 SQL 查询"""
    try:
        print(f"执行 SQL: {sql}")
        print(f"结果限制: {limit} 行\n")
        with odps.execute_sql(sql).open_reader() as reader:
            records = []
            for i, record in enumerate(reader):
                if i >= limit:
                    break
                records.append(dict(record))

        if not records:
            print("(无结果)")
            return

        # 打印表头
        headers = list(records[0].keys())
        col_widths = [max(len(h), max((len(str(r.get(h, ""))) for r in records), default=0)) for h in headers]
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print(header_line)
        print("-" * len(header_line))

        # 打印数据行
        for record in records:
            row = " | ".join(str(record.get(h, "")).ljust(col_widths[i]) for i, h in enumerate(headers))
            print(row)

        print(f"\n共 {len(records)} 行")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="ODPS 命令行辅助工具 (OpenClaw Skill 配套脚本)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-tables", action="store_true", help="列出所有表")
    group.add_argument("--describe", metavar="TABLE", help="获取表结构")
    group.add_argument("--query", metavar="SQL", help="执行 SQL 查询")

    parser.add_argument("--pattern", metavar="PATTERN", help="表名过滤关键词（配合 --list-tables）")
    parser.add_argument("--limit", type=int, default=100, help="查询结果行数限制，默认 100")

    args = parser.parse_args()

    odps = get_odps_client()

    if args.list_tables:
        cmd_list_tables(odps, pattern=args.pattern)
    elif args.describe:
        cmd_describe(odps, args.describe)
    elif args.query:
        cmd_query(odps, args.query, limit=args.limit)


if __name__ == "__main__":
    main()
