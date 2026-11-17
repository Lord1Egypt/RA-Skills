# -*- coding: utf-8 -*-
"""
fetch_history.py — 抓取中国福彩 / 体彩历史开奖数据

用法:
  python fetch_history.py --game ssq --count 100 --out ssq.json
  python fetch_history.py --game dlt --count 50 --source opencai --out dlt.json
  python fetch_history.py --local existing.json --out copy.json   # 仅做格式校验/复制

说明:
  - 默认按顺序尝试多个公开数据源, 任一成功即采用, 失败则自动尝试下一个。
  - 公开彩票接口经常变动, 若全部失败会提示改用 --local 导入已有数据文件。
  - 输出为归一化 JSON (见 lottery_core.load_normalized 的格式说明), 供 analyze/generate 使用。

依赖: 仅标准库。
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lottery_core as core

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# opencai 接口使用的彩种名
OPENCAI_NAME = {
    "ssq": "ssq", "dlt": "dlt", "qlc": "qlc", "kl8": "kl8",
    "fc3d": "fc3d", "pl3": "pl3", "pl5": "pl5", "qxc": "qxc",
}


def _http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Referer": "https://www.baidu.com/"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "ignore")


def _parse_opencode(game, opencode):
    """解析 opencai 风格开奖号 '01,02,03,04,05,06+07' -> pools dict。"""
    cfg = core.GAME_CONFIG[game]
    pools = {}
    if "+" in opencode:
        main_part, extra = opencode.split("+", 1)
    else:
        main_part, extra = opencode, ""
    nums = [int(x) for x in main_part.split(",") if x.strip() != ""]
    if game in ("ssq",):
        pools["red"] = nums
        pools["blue"] = [int(x) for x in extra.split(",") if x.strip() != ""]
    elif game in ("dlt",):
        pools["front"] = nums
        pools["back"] = [int(x) for x in extra.split(",") if x.strip() != ""]
    elif game in ("qlc",):
        pools["main"] = nums[:7]
        pools["special"] = [int(x) for x in extra.split(",") if x.strip() != ""][:1]
    else:  # single pool
        pools["main"] = nums
    return pools


def fetch_opencai(game, count):
    """开彩网 (opencai.net) JSON 接口。结构可能调整, 失败返回 None。"""
    name = OPENCAI_NAME.get(game, game)
    url = "https://www.opencai.net/api/lottery/?name=%s&num=%d" % (name, count)
    try:
        txt = _http_get(url)
        data = json.loads(txt)
        rows = data.get("data") or data.get("result") or []
        records = []
        for r in rows:
            oc = r.get("opencode") or r.get("openCode") or ""
            issue = str(r.get("expect") or r.get("issue") or "")
            date = (r.get("opentime") or r.get("openTime") or "")[:10]
            if not oc:
                continue
            records.append({"issue": issue, "date": date,
                            "pools": _parse_opencode(game, oc)})
        if records:
            return records
    except Exception as e:
        sys.stderr.write("[opencai] 失败: %s\n" % e)
    return None


def fetch_500(game, count):
    """500彩票 (datachart.500.com) HTML 抓取。脆弱, 失败返回 None。"""
    # 仅对 ssq/dlt/qlc/kl8 等 datachart 支持的彩种
    try:
        url = "https://datachart.500.com/%s/history/newinc/history.php?start=00001&end=99999" % game
        txt = _http_get(url)
        # 简单正则提取期号与开奖号(需根据实际 HTML 调整)
        import re
        # 500 的 history 页面为表格, 这里仅做占位解析演示
        rows = re.findall(r"<td>(\d{6,7})</td>.*?openCode.*?>([\d,\+\s]+)<", txt, re.S)
        records = []
        for issue, oc in rows[:count]:
            oc = oc.replace(" ", "").replace("\n", "")
            records.append({"issue": issue, "date": "",
                            "pools": _parse_opencode(game, oc)})
        if records:
            return records
    except Exception as e:
        sys.stderr.write("[500] 失败: %s\n" % e)
    return None


SOURCES = {
    "opencai": fetch_opencai,
    "500": fetch_500,
}


def fetch(game, count, source=None):
    if source and source != "auto":
        fn = SOURCES.get(source)
        if not fn:
            raise ValueError("未知数据源: %s (可选: %s)" % (source, ", ".join(SOURCES)))
        recs = fn(game, count)
        if not recs:
            raise RuntimeError("数据源 %s 未返回数据, 请改用 --local 导入。" % source)
        return recs
    # auto: 依次尝试
    for name, fn in SOURCES.items():
        recs = fn(game, count)
        if recs:
            sys.stderr.write("[OK] 数据源生效: %s (%d 期)\n" % (name, len(recs)))
            return recs
    raise RuntimeError("所有在线数据源均失败(接口可能变动/网络受限)。"
                       "请改用 --local 导入已有数据文件。")


def main():
    ap = argparse.ArgumentParser(description="抓取福彩/体彩历史开奖数据")
    ap.add_argument("--game", default="ssq", help="彩种: ssq/dlt/qlc/kl8/fc3d/pl3/pl5/qxc")
    ap.add_argument("--count", type=int, default=100, help="抓取期数")
    ap.add_argument("--source", default="auto", help="数据源: auto/opencai/500/local")
    ap.add_argument("--local", default=None, help="直接读取本地数据文件(JSON/CSV)")
    ap.add_argument("--out", default=None, help="输出 JSON 路径")
    args = ap.parse_args()

    game = core.resolve_game(args.game)

    if args.local:
        data = core.load_normalized(args.local)
        records = data["records"]
        if data.get("game") and data["game"] != game:
            sys.stderr.write("注意: 文件彩种(%s)与 --game(%s) 不一致, 以 --game 为准。\n"
                             % (data.get("game"), game))
    else:
        records = fetch(game, args.count, args.source)

    out = args.out or ("%s_history.json" % game)
    out_data = {"game": game, "source": args.source if not args.local else "local",
                "records": records}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print("已写出 %d 期 %s 数据 -> %s" % (len(records), core.GAME_CONFIG[game]["name"], out))


if __name__ == "__main__":
    main()
