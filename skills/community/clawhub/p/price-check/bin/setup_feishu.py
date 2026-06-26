#!/usr/bin/env python3
"""price-check v0.3 飞书多维表格一次性配置脚本

用法：
    uv run bin/setup_feishu.py <feishu_base_url>
    例：
    uv run bin/setup_feishu.py 'https://your-tenant.feishu.cn/base/&lt;BASE_TOKEN&gt;...?from=...'

会做四件事：
1. 解析 URL 提取 base_token
2. 通过 lark-cli 列出 base 里的表，自动选第一张（默认表）作为 queries 表
3. 通过 lark-cli 自动建字段（已存在的字段会跳过）
4. 把 base_token / table_id / enabled=true 写到
   ~/.openclaw/data/price-check/config.json

要求：
- lark-cli 已安装并配置好飞书 Bot 应用（OpenClaw 默认 agent 名 "Molty"，自定义部署可用别的）
- 飞书表格已授予该 Bot 编辑权限（在表格"协作"里添加 Bot 为协作者）
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

CONFIG_PATH = Path.home() / ".openclaw" / "data" / "price-check" / "config.json"


# 字段定义：(name, type, options?)。
# 飞书 base 字段 type 可选：text / number / select / url / checkbox / datetime ...
# select 字段需要 options 列表（顶层放，不是 property 下）。
FIELDS_TO_CREATE: list[tuple[str, str, list[str] | None]] = [
    ("查询词",       "text",     None),
    ("Verdict",      "select",   ["强烈推荐", "可以买", "再等等", "别买",
                                  "数据噪音过多，无法判断", "数据质量不足，无法可信推荐", "无数据"]),
    ("Verdict依据",  "text",     None),
    ("best_deal价格", "number",  None),
    ("best_deal平台", "select",  ["全部", "淘宝/天猫", "京东", "拼多多", "苏宁",
                                  "唯品会", "考拉", "抖音", "快手", "1688", "未知"]),
    ("best_deal店铺", "text",    None),
    ("best_deal标题", "text",    None),
    ("best_deal搜索链接", "url", None),  # v0.6.0: 改名 + 改语义为原生搜索 URL
    ("Top2标签",        "text",  None),
    ("Top2搜索链接",    "url",   None),
    ("Top3标签",        "text",  None),
    ("Top3搜索链接",    "url",   None),
    ("匹配度",       "number",  None),
    ("Condition",    "select",  ["unknown", "trusted_domestic", "parallel_import",
                                  "refurbished", "bundle", "accessory", "activation_questionable"]),
    ("中位数",       "number",  None),
    ("最低价",       "number",  None),
    ("最高价",       "number",  None),
    ("原始条数",     "number",  None),
    ("剔除数",       "number",  None),
    ("过滤数",       "number",  None),
    ("不匹配数",     "number",  None),
    ("Trap提示",     "text",    None),
    # v0.4 历史价字段
    ("历史样本数",   "number",  None),
    ("历史最低",     "number",  None),
    ("历史最高",     "number",  None),
    ("历史均价",     "number",  None),
    ("当前位置",     "select",  ["low", "mid", "high"]),
    ("市场30日中位", "number",  None),
    ("当前/市场比",  "number",  None),
    ("标记已购",     "checkbox", None),
]


def parse_base_url(url: str) -> str:
    """提取 URL 里的 base_token。

    支持格式：
      https://your-tenant.feishu.cn/base/&lt;BASE_TOKEN&gt;...?...
      https://xxx.feishu.cn/wiki/wikcn... (wiki 子页) — 不支持，需要先转成 base URL
    """
    m = re.search(r"/base/([A-Za-z0-9]+)", url)
    if not m:
        sys.exit(f"❌ 无法从 URL 提取 base_token：{url}\n  期望形如 https://your-tenant.feishu.cn/base/&lt;BASE_TOKEN&gt;...")
    return m.group(1)


def lark(args: list[str], timeout: int = 30) -> dict[str, Any]:
    """跑 lark-cli 命令，返回解析后的 JSON。失败 sys.exit。"""
    cmd = ["lark-cli"] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError:
        sys.exit("❌ lark-cli 未安装或不在 PATH")
    if r.returncode != 0:
        sys.exit(f"❌ lark-cli 失败：\n  cmd: {' '.join(cmd)}\n  stderr: {r.stderr.strip()}")
    out = r.stdout.strip()
    if not out:
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"_raw": out}


def list_tables(base_token: str) -> list[dict[str, Any]]:
    res = lark(["base", "+table-list", "--base-token", base_token])
    data = res.get("data") or res
    return data.get("tables") or data.get("items") or []


def list_fields(base_token: str, table_id: str) -> list[dict[str, Any]]:
    res = lark(["base", "+field-list", "--base-token", base_token, "--table-id", table_id])
    data = res.get("data") or res
    return data.get("fields") or data.get("items") or []


def create_field(base_token: str, table_id: str, name: str, type_: str, options: list[str] | None) -> bool:
    """创建一个字段。返回 True=成功，False=失败（包括已存在）。"""
    body: dict[str, Any] = {"name": name, "type": type_}
    if type_ == "select" and options:
        body["options"] = [{"name": o} for o in options]
        body["multiple"] = False

    cmd = [
        "base", "+field-create",
        "--base-token", base_token,
        "--table-id", table_id,
        "--json", json.dumps(body, ensure_ascii=False),
    ]
    r = subprocess.run(["lark-cli"] + cmd, capture_output=True, text=True, timeout=20, check=False)
    if r.returncode == 0:
        return True
    err = (r.stderr or r.stdout).strip()
    # 字段已存在
    if "exist" in err.lower() or "duplicate" in err.lower() or "重复" in err or "Conflict" in err:
        return False
    print(f"  ⚠️ 字段 {name} ({type_}) 创建失败：{err[-200:]}", file=sys.stderr)
    return False


def main() -> None:
    p = argparse.ArgumentParser(description="price-check 飞书多维表格一次性配置")
    p.add_argument("base_url", help="飞书多维表格 URL")
    p.add_argument("--profile", default=None, help="lark-cli profile 名（可选）")
    args = p.parse_args()

    base_token = parse_base_url(args.base_url)
    print(f"📍 base_token = {base_token}")

    print("📋 列举表...")
    tables = list_tables(base_token)
    if not tables:
        sys.exit("❌ 该 base 下没有表。请先在飞书里手动创建空表，再跑本脚本。")
    table = tables[0]
    table_id = table.get("id") or table.get("table_id")
    table_name = table.get("name") or "(默认表)"
    print(f"📋 选用表：{table_name} (id={table_id})")

    print("📋 列举现有字段...")
    existing_fields = list_fields(base_token, table_id)
    existing_names = {f.get("name") or f.get("field_name") for f in existing_fields}
    print(f"   已有字段：{sorted(existing_names)}")

    print("➕ 增量创建字段...")
    created = 0
    skipped = 0
    failed = 0
    for name, type_, options in FIELDS_TO_CREATE:
        if name in existing_names:
            skipped += 1
            continue
        ok = create_field(base_token, table_id, name, type_, options)
        if ok:
            created += 1
            print(f"  ✓ 创建 {name} ({type_})")
        else:
            failed += 1
    print(f"   完成：创建 {created} / 跳过 {skipped} / 失败 {failed}")

    # 写回 config.json（只动 feishu_sync 段；version / storage / history_provider 由主程序维护，不在此覆盖）
    print("💾 写入 config.json...")
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    config: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            config = {}
    config["feishu_sync"] = {
        "enabled": True,
        "base_token": base_token,
        "table_id": table_id,
        "lark_cli_profile": args.profile,
    }
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   配置已写入 {CONFIG_PATH}")

    print()
    print("✅ 飞书同步已启用")
    print(f"   base: {base_token}")
    print(f"   table: {table_id}")
    print("   下次跑 price-check 会自动同步到飞书表格")
    print()
    print("如需关闭：编辑 config.json 把 feishu_sync.enabled 改成 false")


if __name__ == "__main__":
    main()
