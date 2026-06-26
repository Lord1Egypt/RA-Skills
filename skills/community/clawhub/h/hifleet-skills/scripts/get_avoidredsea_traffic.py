#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集装箱饶航船舶每日统计。、支持查询下饶航红海的集装箱船舶。
对于饶航饶航的方向：东是向东，西是向西。
接口：POST {base}/routerisk/getAvoidRedSeaDetail/token，参数 starttime、endtime、api_key（可选）。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。
无 `api_key` 仅可查最近 1 周；有 `api_key` 时间区间不限。

用法:
  python get_avoidredsea_traffic.py  [开始日期] [结束日期] [i18n]

  日期: yyyy-MM-dd，不传则默认最近 1 天。无 `api_key` 时区间不得超过 7 天；有 `api_key` 不限。i18n 可选 zh 或 en。

Security: 仅向 HIFLEET_API_BASE 下 routerisk/getAvoidRedSeaDetail/token 发起 POST；标准库 only。
"""
import os
import sys
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")




def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def get_strait_traffic(starttime: str, endtime: str, i18n: str = "zh", api_key: str = None) -> dict:
    """POST 请求红海绕航统计。有 api_key 时传入可查任意时间区间。"""
    params = {"starttime": starttime, "endtime": endtime, "i18n": i18n}
    if api_key:
        params["api_key"] = api_key
    url = api_base() + "/routerisk/getAvoidRedSeaDetail/token?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="POST", data=b"")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():



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
        start_d = today - timedelta(days=1)

    if start_d > end_d:
        print("开始日期不得大于结束日期", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    delta = (end_d - start_d).days
    if delta > 6 and not api_key:
        print("无 api_key 时仅可查询最近 1 天（1 天），当前区间为 %d 天。请配置 HIFLEET_API_KEY 或缩短区间。" % (delta + 1), file=sys.stderr)
        sys.exit(1)

    i18n = (sys.argv[4].strip() if len(sys.argv) > 4 else "zh").lower()
    if i18n not in ("zh", "en"):
        i18n = "zh"

    start_str = start_d.strftime("%Y-%m-%d")
    end_str = end_d.strftime("%Y-%m-%d")

    try:
        data = get_strait_traffic(start_str, end_str, i18n, api_key)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
