#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据 IMO 或 MMSI 获取船舶档案（基本信息、尺度、舱容、建造、入级、动力、公司信息、互保协会等）。
接口支持 imo 与 mmsi 二选一；内贸船无 IMO 时仅传 mmsi 即可。船名不支持，需先通过 shipSearch 得到 MMSI/IMO。
需配置环境变量 `HIFLEET_API_KEY`。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_archive.py <IMO>   # 按 IMO 查档案（7 位）
  python get_archive.py <MMSI>  # 按 MMSI 查档案（9 位，支持内贸船无 IMO）

Security: 仅向 HIFLEET_API_BASE 下 shiparchive 路径发起 GET；标准库 only。
"""
import os
import sys
import urllib.request
import urllib.parse
import json


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def get_archive(api_key: str, imo: str = None, mmsi: str = None) -> dict:
    """根据 IMO 或 MMSI 获取船舶档案。imo 与 mmsi 二选一；内贸船无 IMO 时仅传 mmsi。"""
    if mmsi:
        params = {"mmsi": mmsi.strip(), "api_key": api_key}
    else:
        params = {"imo": (imo or "").strip(), "api_key": api_key}
    url = api_base() + "/shiparchive/getShipArchiveWithEnginAndCompany?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def _format_value(item: dict, indent: str) -> list:
    """递归格式化一条 value 项，返回要打印的行列表。"""
    lines = []
    val = item.get("value")
    label_zh = (item.get("labelZh") or "").strip()
    # 嵌套结构：value 是列表
    if isinstance(val, list) and len(val) > 0:
        if label_zh:
            lines.append(indent + label_zh + ":")
        next_indent = indent + "  "
        for sub in val:
            if isinstance(sub, dict):
                lines.extend(_format_value(sub, next_indent))
    else:
        # 键值行：用 valueZh，无则用 value
        disp = item.get("valueZh")
        if disp is None:
            disp = item.get("value")
        if disp is None:
            disp = ""
        if isinstance(disp, str) and disp.strip() == "" and not label_zh:
            return lines
        if label_zh:
            lines.append(indent + label_zh + ": " + str(disp))
    return lines


def print_archive(data: dict) -> None:
    """按 data 分块打印档案，使用 labelZh / valueZh。"""
    blocks = data.get("data") or []
    if not blocks:
        if data.get("status") != "1":
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for block in blocks:
        title = block.get("labelZh") or block.get("key") or ""
        vals = block.get("value")
        if not title and not vals:
            continue
        print("\n【" + title + "】")
        if isinstance(vals, list):
            for item in vals:
                if isinstance(item, dict):
                    for line in _format_value(item, "  "):
                        print(line)
    print()


def main():
    api_key = get_api_key()
    if not api_key:
        print("请先配置 HiFleet 授权 api_key（环境变量 HIFLEET_API_KEY）", file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) < 2:
        print("用法: python get_archive.py <IMO> 或 python get_archive.py <MMSI>", file=sys.stderr)
        sys.exit(1)
    raw_input = sys.argv[1].strip()
    # 支持 IMO 前缀
    if raw_input.upper().startswith("IMO"):
        raw_input = raw_input.upper().replace("IMO", "").strip()
    if not raw_input.isdigit():
        print("档案查询仅支持 IMO（7 位）或 MMSI（9 位）数字，不支持船名。请先通过船位/搜船得到 IMO 或 MMSI。", file=sys.stderr)
        sys.exit(1)
    # 9 位：MMSI，直接传 mmsi 查档案（支持内贸船无 IMO）；7 位：IMO，传 imo
    if len(raw_input) == 9:
        try:
            raw = get_archive(api_key, mmsi=raw_input)
        except Exception as e:
            print(f"档案请求失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if len(raw_input) < 6:
            print("IMO 应为数字（通常 7 位）", file=sys.stderr)
            sys.exit(1)
        try:
            raw = get_archive(api_key, imo=raw_input)
        except Exception as e:
            print(f"档案请求失败: {e}", file=sys.stderr)
            sys.exit(1)
    if raw.get("status") != "1":
        print(json.dumps(raw, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    print_archive(raw)


if __name__ == "__main__":
    main()
