#!/usr/bin/env python3
"""
柳比歇夫时间记录 - 一键初始化脚本

自动完成以下操作：
1. 检查 lark-cli 是否已安装并登录
2. 创建飞书多维表格（记录表 + 日报表）
3. 创建所有字段（含正确的类型和选项）
4. 输出配置信息，供 SKILL.md 或自动化使用

用法：
  python3 setup.py [--base-token EXISTING_BASE_TOKEN]

如果不传 --base-token，脚本会自动创建新的多维表格。
如果传入已有的 base-token，则在现有表格中创建新表。

前置条件：
  1. pip install lark-cli
  2. lark-cli auth login
"""

import subprocess
import sys
import json
import argparse
import time


def run_lark_cli(args, check=True):
    """执行 lark-cli 命令并返回解析后的 JSON"""
    cmd = ["lark-cli"] + args
    print(f"  → {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0 and check:
        print(f"  ✗ 命令失败 (exit {result.returncode})")
        print(f"    stdout: {result.stdout[:200]}")
        print(f"    stderr: {result.stderr[:200]}")
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        if check:
            print(f"  ✗ JSON 解析失败: {result.stdout[:200]}")
            sys.exit(1)
        return None


def check_lark_cli():
    """检查 lark-cli 是否可用"""
    print("\n📋 步骤 1/4：检查 lark-cli")
    try:
        result = subprocess.run(["lark-cli", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("  ✓ lark-cli 已安装")
        else:
            print("  ✗ lark-cli 未正确安装")
            print("    请运行: pip install lark-cli")
            sys.exit(1)
    except FileNotFoundError:
        print("  ✗ lark-cli 未找到")
        print("    请运行: pip install lark-cli")
        sys.exit(1)

    # 检查是否已登录
    result = subprocess.run(["lark-cli", "auth", "whoami"], capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and result.stdout.strip():
        print(f"  ✓ 已登录: {result.stdout.strip()}")
    else:
        print("  ✗ 未登录飞书")
        print("    请运行: lark-cli auth login")
        sys.exit(1)


def create_base():
    """创建新的多维表格"""
    print("\n📋 步骤 2/4：创建飞书多维表格")
    result = run_lark_cli([
        "base", "+create",
        "--name", "柳比歇夫时间记录",
        "--i-have-read-guide"
    ])
    base_token = result.get("data", {}).get("app", {}).get("appToken", "")
    if not base_token:
        print("  ✗ 创建多维表格失败")
        sys.exit(1)
    print(f"  ✓ 多维表格已创建: {base_token}")
    return base_token


def get_existing_tables(base_token):
    """获取现有的表列表"""
    result = run_lark_cli([
        "base", "+table-list",
        "--base-token", base_token,
        "--i-have-read-guide"
    ])
    tables = result.get("data", {}).get("items", [])
    return tables


def create_records_table(base_token):
    """创建记录表及所有字段"""
    print("\n📋 步骤 3/4：创建记录表")

    # 创建表
    result = run_lark_cli([
        "base", "+table-create",
        "--base-token", base_token,
        "--name", "时间记录",
        "--i-have-read-guide"
    ])
    table_id = result.get("data", {}).get("table_id", "")
    if not table_id:
        print("  ✗ 创建记录表失败")
        sys.exit(1)
    print(f"  ✓ 记录表已创建: {table_id}")

    # 获取默认字段 ID（自动创建的）
    result = run_lark_cli([
        "base", "+field-list",
        "--base-token", base_token,
        "--table-id", table_id,
        "--i-have-read-guide"
    ])
    existing_fields = {f["field_name"]: f["field_id"] for f in result.get("data", {}).get("fields", [])}

    # 删除默认的多行文本字段
    for fname, fid in existing_fields.items():
        run_lark_cli([
            "base", "+field-delete",
            "--base-token", base_token,
            "--table-id", table_id,
            "--field-id", fid,
            "--yes"
        ], check=False)
        print(f"    删除默认字段: {fname}")

    # 记录表字段定义
    fields = [
        {"name": "记录日期", "type": "date"},
        {"name": "开始时间", "type": "text"},
        {"name": "结束时间", "type": "text"},
        {"name": "时长（分钟）", "type": "number", "style": {"type": "plain", "precision": 0, "percentage": False, "thousands_separator": False}},
        {"name": "主活动描述", "type": "text"},
        {"name": "主类别", "type": "single_select", "options": ["睡觉", "日常", "输入", "输出", "关系", "回血"]},
        {"name": "主Tag", "type": "text"},
        {"name": "附带活动描述", "type": "text"},
        {"name": "附带类别", "type": "single_select", "options": ["睡觉", "日常", "输入", "输出", "关系", "回血"]},
        {"name": "附带Tag", "type": "text"},
        {"name": "附带时长（分钟）", "type": "number", "style": {"type": "plain", "precision": 0, "percentage": False, "thousands_separator": False}},
        {"name": "能量状态", "type": "single_select", "options": ["高能", "平稳", "消耗"]},
        {"name": "记录人", "type": "user"},
    ]

    for i, field in enumerate(fields):
        cmd_args = [
            "base", "+field-create",
            "--base-token", base_token,
            "--table-id", table_id,
            "--json", json.dumps(field, ensure_ascii=False),
            "--i-have-read-guide"
        ]
        run_lark_cli(cmd_args)
        print(f"    ✓ [{i+1}/13] {field['name']}")

    print(f"  ✓ 记录表 13 个字段全部创建完成")
    return table_id


def create_daily_table(base_token):
    """创建日报表及所有字段"""
    print("\n📋 步骤 4/4：创建日报表")

    # 创建表
    result = run_lark_cli([
        "base", "+table-create",
        "--base-token", base_token,
        "--name", "日报",
        "--i-have-read-guide"
    ])
    table_id = result.get("data", {}).get("table_id", "")
    if not table_id:
        print("  ✗ 创建日报表失败")
        sys.exit(1)
    print(f"  ✓ 日报表已创建: {table_id}")

    # 获取默认字段 ID
    result = run_lark_cli([
        "base", "+field-list",
        "--base-token", base_token,
        "--table-id", table_id,
        "--i-have-read-guide"
    ])
    existing_fields = {f["field_name"]: f["field_id"] for f in result.get("data", {}).get("fields", [])}

    # 删除默认字段
    for fname, fid in existing_fields.items():
        run_lark_cli([
            "base", "+field-delete",
            "--base-token", base_token,
            "--table-id", table_id,
            "--field-id", fid,
            "--yes"
        ], check=False)

    # 日报表字段定义（24个）
    fields = [
        {"name": "日期", "type": "date"},
        {"name": "追踪总时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "黑洞时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "黑洞占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "睡觉时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "睡觉占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "日常时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "日常占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "输入时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "输入占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "输出时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "输出占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "关系时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "关系占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "回血时长", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "回血占比", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "Top1资产", "type": "text"},
        {"name": "Top2资产", "type": "text"},
        {"name": "Top3资产", "type": "text"},
        {"name": "增量复利", "type": "number", "style": {"type": "plain", "precision": 1, "percentage": False, "thousands_separator": False}},
        {"name": "增量复利明细", "type": "text"},
        {"name": "能量洞察", "type": "text"},
        {"name": "日报全文", "type": "text"},
        {"name": "记录人", "type": "user"},
    ]

    for i, field in enumerate(fields):
        cmd_args = [
            "base", "+field-create",
            "--base-token", base_token,
            "--table-id", table_id,
            "--json", json.dumps(field, ensure_ascii=False),
            "--i-have-read-guide"
        ]
        run_lark_cli(cmd_args)
        print(f"    ✓ [{i+1}/24] {field['name']}")

    print(f"  ✓ 日报表 24 个字段全部创建完成")
    return table_id


def main():
    parser = argparse.ArgumentParser(description="柳比歇夫时间记录 - 一键初始化")
    parser.add_argument("--base-token", help="已有的多维表格 token（不传则自动创建）")
    args = parser.parse_args()

    print("=" * 50)
    print("⏱️  柳比歇夫时间记录 - 一键初始化")
    print("=" * 50)

    # 步骤1: 检查环境
    check_lark_cli()

    # 步骤2: 创建/使用多维表格
    if args.base_token:
        base_token = args.base_token
        print(f"\n📋 步骤 2/4：使用已有表格 {base_token}")
    else:
        base_token = create_base()

    # 步骤3: 创建记录表
    records_table_id = create_records_table(base_token)

    # 步骤4: 创建日报表
    daily_table_id = create_daily_table(base_token)

    # 输出配置信息
    print("\n" + "=" * 50)
    print("✅ 初始化完成！")
    print("=" * 50)
    print(f"""
📌 请保存以下配置信息：

  Base Token:      {base_token}
  记录表 Table ID: {records_table_id}
  日报表 Table ID: {daily_table_id}

📎 飞书表格链接：
  https://feishu.cn/base/{base_token}

🔧 日报脚本用法：
  python3 scripts/daily_report.py --date YYYY-MM-DD \\
    --base-token {base_token} \\
    --records-table {records_table_id} \\
    --daily-table {daily_table_id} \\
    --recorder YOUR_NAME \\
    --recorder-id YOUR_OPEN_ID

💡 获取你的 open_id：
  lark-cli contact +search --keyword "你的名字"
""")


if __name__ == "__main__":
    main()
