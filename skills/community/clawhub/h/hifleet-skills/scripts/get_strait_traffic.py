#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海峡通航统计。咽喉航道通航船舶统计。支持曼德海峡、苏伊士运河、好望角、霍尔木兹海峡。
对于霍尔木兹海峡的方向：东是出湾，西是入湾。
接口：POST {base}/position/statisticzonetraffic，参数 oid、startdate、enddate、i18n（可选）、api_key（可选）。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。
无 `api_key` 仅可查最近 1 周；有 `api_key` 时间区间不限。

用法:
  python get_strait_traffic.py <海峡名或oid> [开始日期] [结束日期] [i18n]
  海峡: 曼德海峡|苏伊士运河|好望角|霍尔木兹海峡 或 oid(24480|132808|1062830|24471)
  日期: yyyy-MM-dd，不传则默认最近 7 天。无 `api_key` 时区间不得超过 7 天；有 `api_key` 不限。i18n 可选 zh 或 en。

Security: 仅向 HIFLEET_API_BASE 下 position/statisticzonetraffic 发起 POST；标准库 only。
"""
import os
import sys
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")

STRAITS = {
    "曼德海峡": "24480",
    "苏伊士运河": "132808",
    "好望角": "1062830",
    "霍尔木兹海峡": "24471",
    "24480": "24480",
    "132808": "132808",
    "1062830": "1062830",
    "24471": "24471",
}


def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def get_strait_traffic(oid: str, startdate: str, enddate: str, i18n: str = "zh", api_key: str = None) -> dict:
    """POST 请求咽喉航道通航统计。有 api_key 时传入可查任意时间区间。"""
    params = {"oid": oid, "startdate": startdate, "enddate": enddate, "i18n": i18n}
    if api_key:
        params["api_key"] = api_key
    url = api_base() + "/position/statisticzonetraffic?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="POST", data=b"")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():
    if len(sys.argv) < 2:
        print("用法: python get_strait_traffic.py <海峡名或oid> [开始日期] [结束日期] [i18n]", file=sys.stderr)
        print("海峡: 曼德海峡 苏伊士运河 好望角 霍尔木兹海峡 或 oid 24480 132808 1062830 24471", file=sys.stderr)
        print("日期: yyyy-MM-dd，不传默认最近 7 天。i18n 可选 zh 或 en。", file=sys.stderr)
        sys.exit(1)

    key = sys.argv[1].strip()
    oid = STRAITS.get(key) or (key if key.isdigit() else None)
    if not oid:
        print("未知海峡，支持: 曼德海峡、苏伊士运河、好望角、霍尔木兹海峡 或 oid 24480 132808 1062830 24471", file=sys.stderr)
        sys.exit(1)

    today = datetime.now().date()
    if len(sys.argv) >= 4:
        start_s = sys.argv[2].strip()
        end_s = sys.argv[3].strip()
        try:
            start_d = datetime.strptime(start_s, "%Y-%m-%d").date()
            end_d = datetime.strptime(end_s, "%Y-%m-%d").date()
        except ValueError:
            print("日期格式须为 yyyy-MM-dd", file=sys.stderr)
            sys.exit(1)
    else:
        end_d = today
        start_d = today - timedelta(days=6)

    if start_d > end_d:
        print("开始日期不得大于结束日期", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    delta = (end_d - start_d).days
    if delta > 6 and not api_key:
        print("无 api_key 时仅可查询最近 1 周（7 天），当前区间为 %d 天。请配置 HIFLEET_API_KEY 或缩短区间。" % (delta + 1), file=sys.stderr)
        sys.exit(1)

    i18n = (sys.argv[4].strip() if len(sys.argv) > 4 else "zh").lower()
    if i18n not in ("zh", "en"):
        i18n = "zh"

    start_str = start_d.strftime("%Y-%m-%d")
    end_str = end_d.strftime("%Y-%m-%d")

    try:
        data = get_strait_traffic(oid, start_str, end_str, i18n, api_key)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
