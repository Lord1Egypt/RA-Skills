#!/usr/bin/env python3
"""CLI script to query Haier IoT API for SJTU laundry machine status."""

import argparse
import sys
import requests

API_URL = "https://yshz-user.haier-ioc.com/position/deviceDetailPage"

BUILDINGS = [
    {"id": "27131", "name": "西21楼"},
    {"id": "27136", "name": "西16楼"},
]
DEFAULT_BUILDING = "西21楼"

STATE_MAP = {1: "空闲", 2: "使用中", 3: "故障", 4: "离线"}
STATE_ORDER = {"空闲": 0, "使用中": 1, "故障": 2, "离线": 3, "未知": 4}
CATEGORY_MAP = {"00": "洗衣机", "02": "烘干机"}


def fetch_devices(position_id, category_code="00"):
    body = {
        "positionId": position_id,
        "categoryCode": category_code,
        "page": 1,
        "floorCode": "",
        "pageSize": 100,
    }
    try:
        resp = requests.post(API_URL, json=body, timeout=10)
        resp.raise_for_status()
    except requests.Timeout:
        print("错误：请求超时，请检查网络连接", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"错误：网络请求失败 — {e}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if data.get("code") != 0:
        print(f"错误：API 返回错误 — {data.get('message', '未知错误')}", file=sys.stderr)
        sys.exit(1)

    return data["data"]["items"]


def format_time(finish_time):
    if not finish_time:
        return ""
    parts = finish_time.split(" ")
    if len(parts) >= 2:
        return parts[1][:5]
    return finish_time[:5]


def format_building(building_id):
    washers = fetch_devices(building_id, "00")
    dryers = fetch_devices(building_id, "02")

    building_name = None
    for b in BUILDINGS:
        if b["id"] == building_id:
            building_name = b["name"]
            break
    if building_name is None:
        building_name = building_id

    lines = [f"{building_name}："]

    for category_code, devices in [("00", washers), ("02", dryers)]:
        label = CATEGORY_MAP.get(category_code, category_code)
        lines.append(f"  {label}:")

        groups = {}
        for d in devices:
            state = STATE_MAP.get(d.get("state"), "未知")
            groups.setdefault(state, []).append(d)

        if not devices:
            lines.append("    （无设备）")
            continue

        sorted_states = sorted(groups.keys(), key=lambda s: STATE_ORDER.get(s, 99))
        for state in sorted_states:
            items = groups[state]
            parts = []
            for d in items:
                name = d.get("name", "?")
                entry = name
                if state == "使用中" and d.get("finishTime"):
                    entry += f" [预计{format_time(d['finishTime'])}结束]"
                parts.append(entry)
            joined = "、".join(parts)
            lines.append(f"    {state}: {len(items)}台（{joined}）")

        lines.append("")

    return "\n".join(lines).rstrip()


def find_building(query):
    for b in BUILDINGS:
        if b["name"] == query or b["id"] == query:
            return b["id"]
    return None


def main():
    parser = argparse.ArgumentParser(description="查询上海交大闵行校区洗衣机/烘干机状态")
    parser.add_argument("--building", type=str, help="指定楼栋名称或ID")
    parser.add_argument("--all", action="store_true", help="查询所有楼栋")
    args = parser.parse_args()

    if args.all:
        for b in BUILDINGS:
            print(format_building(b["id"]))
            print()
    elif args.building:
        bid = find_building(args.building)
        if bid is None:
            names = "、".join(b["name"] for b in BUILDINGS)
            print(f"错误：未找到楼栋「{args.building}」，可选楼栋：{names}", file=sys.stderr)
            sys.exit(1)
        print(format_building(bid))
    else:
        bid = find_building(DEFAULT_BUILDING)
        if bid is None:
            print(f"错误：默认楼栋「{DEFAULT_BUILDING}」未在 BUILDINGS 中找到", file=sys.stderr)
            sys.exit(1)
        print(format_building(bid))


if __name__ == "__main__":
    main()
