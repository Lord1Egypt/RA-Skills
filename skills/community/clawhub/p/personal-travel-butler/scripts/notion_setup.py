#!/usr/bin/env python3
"""Create the Notion Travel Entries database and required properties."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

from notion_common import (
    DEFAULT_NOTION_VERSION,
    PROPERTY_CREATE_SCHEMA,
    check_notion_properties,
    load_local_env,
    normalize_notion_id,
    notion_request,
    save_local_env_value,
    travel_entries_database_payload,
)


def extract_data_source_id(response: dict[str, Any]) -> str | None:
    data_sources = response.get("data_sources")
    if isinstance(data_sources, list) and data_sources:
        first = data_sources[0]
        if isinstance(first, dict) and first.get("id"):
            return str(first["id"])
    if response.get("id"):
        return str(response["id"])
    return None


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-page-id", default=os.environ.get("NOTION_PARENT_PAGE_ID"), help="Parent Notion page ID or copied Notion page URL.")
    parser.add_argument("--title", default="Travel Entries", help="Database/data source title to create.")
    parser.add_argument("--apply", action="store_true", help="Actually create the database. Without this flag, only print the planned payload.")
    parser.add_argument("--force-create", action="store_true", help="Create a new Notion database even if NOTION_TRAVEL_DATA_SOURCE_ID is already configured.")
    args = parser.parse_args()

    existing_data_source_id = os.environ.get("NOTION_TRAVEL_DATA_SOURCE_ID")
    if existing_data_source_id and not args.force_create:
        print("Notion 数据源已经配置好了。")
        print(f"数据源编号: {existing_data_source_id}")
        print("")
        print("不用再运行建库命令，下一步请运行:")
        print("personal-travel-butler/scripts/notion_check.py --db travel-db")
        print("")
        print("如果你真的想再创建一个全新的 Notion 数据库，请加上 --force-create。")
        return 0

    parent_page_id = normalize_notion_id(args.parent_page_id)
    if not parent_page_id:
        print("缺少 Notion 页面编号。请传 --parent-page-id，或先设置 NOTION_PARENT_PAGE_ID。")
        return 1

    payload = travel_entries_database_payload(parent_page_id, args.title)
    if not args.apply:
        print("预演：将会在这个 Notion 页面下创建数据库和列。")
        print(f"页面编号: {parent_page_id}")
        print(f"数据库名称: {args.title}")
        print("将创建这些列:")
        for name in PROPERTY_CREATE_SCHEMA:
            print(f"- {name}")
        print("")
        print("如果确认无误，再运行同一条命令并加上 --apply。")
        return 0

    token = os.environ.get("NOTION_TOKEN")
    version = os.environ.get("NOTION_VERSION", DEFAULT_NOTION_VERSION)
    if not token:
        print("缺少 Notion 令牌。请先在本机设置 NOTION_TOKEN，不要把令牌写进文件或聊天。")
        return 1

    response = notion_request("POST", "/databases", token, version, payload)
    data_source_id = extract_data_source_id(response)
    errors: list[str] = []
    if data_source_id:
        data_source = notion_request("GET", f"/data_sources/{data_source_id}", token, version)
        errors = check_notion_properties((data_source.get("properties") or {}))

    print("Notion 数据库已创建。")
    print(f"数据库编号: {response.get('id')}")
    if data_source_id:
        print(f"数据源编号: {data_source_id}")
        save_local_env_value("NOTION_TRAVEL_DATA_SOURCE_ID", data_source_id)
        print("已写入本地 .env：NOTION_TRAVEL_DATA_SOURCE_ID")
    else:
        print("没有从返回结果中找到数据源编号，请在 Notion 页面链接或返回结果中确认。")

    if errors:
        print("")
        print("提醒：创建后返回的属性结构和预期不完全一致:")
        for error in errors:
            print(f"- {error}")
        print("可以继续运行 notion_check.py 做一次正式检查。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
