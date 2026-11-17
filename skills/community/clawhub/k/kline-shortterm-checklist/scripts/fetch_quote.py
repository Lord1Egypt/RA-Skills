#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_quote.py — 腾讯财经实时行情抓取与短线选股客观指标初筛

用法:
    python fetch_quote.py <股票代码> [--screen]
    股票代码支持: 603045 / sh603045 / 600158 / sz000001 / 8xxxxx(北交所 bj)

说明:
    - 数据源: 腾讯财经接口 https://qt.gtimg.cn/q=<code> (返回 GBK 编码, ~88 字段管道分隔)
    - 本脚本仅做「客观指标」抓取与初筛, 主观项(K线形态/趋势/分时/题材)需人工或看图判断
    - 字段索引已实测确认(2026-08 福达合金 603045), 不同市场字段一致

客观指标映射(索引基于 v_<code>="..." 按 ~ 切分):
    [1] 名称  [2] 代码  [3] 现价  [4] 昨收  [5] 今开
    [32] 涨跌幅%  [33] 最高  [34] 最低  [36] 成交量(手)  [37] 成交额(万)
    [38] 换手率%  [39] 市盈率TTM  [43] 振幅%  [44] 流通市值(亿)
    [45] 总市值(亿)  [46] 市净率  [47] 涨停价  [48] 跌停价  [49] 量比  [51] 均价
"""

import sys
import json
import urllib.request
import urllib.parse

API = "https://qt.gtimg.cn/q="


def normalize_code(code: str) -> str:
    """把纯数字或带前缀的代码规范成 Tencent 接口可用的代码。"""
    code = code.strip().lower()
    if code.startswith(("sh", "sz", "bj")):
        return code
    if len(code) == 6 and code.isdigit():
        if code[0] == "6":
            return "sh" + code
        if code[0] in ("0", "3"):
            return "sz" + code
        if code[0] in ("4", "8"):
            return "bj" + code
    return code  # 兜底, 原样传


def fetch_raw(code: str) -> str:
    url = API + urllib.parse.quote(code)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.qq.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("gbk", "ignore")


def parse(raw: str) -> dict:
    # 形如 v_sh603045="1~名称~代码~..."
    inner = raw.split('"', 1)[1].rsplit('"', 1)[0]
    f = inner.split("~")

    def g(i):
        try:
            return f[i]
        except IndexError:
            return ""

    def num(i):
        v = g(i)
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    return {
        "name": g(1),
        "code": g(2),
        "price": num(3),
        "prev_close": num(4),
        "open": num(5),
        "change_pct": num(32),
        "high": num(33),
        "low": num(34),
        "volume_hand": num(36),
        "amount_wan": num(37),
        "turnover_pct": num(38),
        "pe_ttm": num(39),
        "amplitude_pct": num(43),
        "float_mv_yi": num(44),
        "total_mv_yi": num(45),
        "pb": num(46),
        "limit_up": num(47),
        "limit_down": num(48),
        "volume_ratio": num(49),
        "avg_price": num(51),
        "time": g(30),
    }


# ---------- 客观初筛阈值(来自「下午2:30选股法」与「96原则」) ----------
def screen(d: dict) -> list:
    """返回逐条核查结果 [(项目, 数值, 阈值, 结论), ...]。"""
    rows = []

    cp = d.get("change_pct")
    if cp is None:
        rows.append(("涨幅%", "N/A", "3%~5%", "无数据"))
    elif 3 <= cp <= 5:
        rows.append(("涨幅%", f"{cp:.2f}", "3%~5%", "达标"))
    elif cp < 3:
        rows.append(("涨幅%", f"{cp:.2f}", "3%~5%", "偏弱(低于3%)"))
    else:
        rows.append(("涨幅%", f"{cp:.2f}", "3%~5%", "偏高(高于5%,追高风险)"))

    vr = d.get("volume_ratio")
    if vr is None:
        rows.append(("量比", "N/A", ">=1", "无数据"))
    elif vr >= 1:
        rows.append(("量比", f"{vr:.2f}", ">=1", "达标"))
    else:
        rows.append(("量比", f"{vr:.2f}", ">=1", "剔除(缺成交活性)"))

    to = d.get("turnover_pct")
    if to is None:
        rows.append(("换手率%", "N/A", "5%~10%", "无数据"))
    elif 5 <= to <= 10:
        rows.append(("换手率%", f"{to:.2f}", "5%~10%", "达标"))
    elif to < 5:
        rows.append(("换手率%", f"{to:.2f}", "5%~10%", "剔除(没人气)"))
    else:
        rows.append(("换手率%", f"{to:.2f}", "5%~10%", "警惕(>10%有出货嫌疑)"))

    fm = d.get("float_mv_yi")
    if fm is None:
        rows.append(("流通市值(亿)", "N/A", "50~200亿", "无数据"))
    elif 50 <= fm <= 200:
        rows.append(("流通市值(亿)", f"{fm:.2f}", "50~200亿", "达标"))
    elif fm < 50:
        rows.append(("流通市值(亿)", f"{fm:.2f}", "50~200亿", "剔除(可能庄股)"))
    else:
        rows.append(("流通市值(亿)", f"{fm:.2f}", "50~200亿", "剔除(盘子过大难拉)"))

    # 96原则中可直接量化的风险项
    if vr is not None and vr > 10:
        rows.append(("高位量比", f"{vr:.2f}", "<=10", "警示(高位量比>10规避)"))
    if to is not None and to > 25:
        rows.append(("换手率", f"{to:.2f}", "<=25%", "不买(>25%坚决不买)"))

    return rows


def render(d: dict, do_screen: bool):
    print(f"标的: {d['name']}({d['code']})  时间: {d['time']}")
    print("-" * 52)
    labels = [
        ("现价", "price"), ("昨收", "prev_close"), ("今开", "open"),
        ("涨跌幅%", "change_pct"), ("最高", "high"), ("最低", "low"),
        ("振幅%", "amplitude_pct"), ("成交量(手)", "volume_hand"),
        ("成交额(万)", "amount_wan"), ("换手率%", "turnover_pct"),
        ("量比", "volume_ratio"), ("流通市值(亿)", "float_mv_yi"),
        ("总市值(亿)", "total_mv_yi"), ("市盈率TTM", "pe_ttm"),
        ("市净率", "pb"), ("均价", "avg_price"),
        ("涨停价", "limit_up"), ("跌停价", "limit_down"),
    ]
    for zh, key in labels:
        v = d.get(key)
        print(f"  {zh:<10}: {v}")

    if do_screen:
        print("-" * 52)
        print("客观初筛(下午2:30选股法 / 96原则可量化项):")
        print(f"  {'项目':<14}{'数值':<10}{'阈值':<14}{'结论'}")
        for item, val, thr, verdict in screen(d):
            print(f"  {item:<14}{val:<10}{thr:<14}{verdict}")

    # 同时输出 JSON 便于程序化消费
    print("-" * 52)
    out = {"quote": d}
    if do_screen:
        out["screen"] = [
            {"item": i, "value": v, "threshold": t, "verdict": vd}
            for i, v, t, vd in screen(d)
        ]
    print("JSON>>> " + json.dumps(out, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    code = args[0]
    do_screen = "--screen" in args
    norm = normalize_code(code)
    try:
        raw = fetch_raw(norm)
    except Exception as e:
        print(f"抓取失败: {e}")
        sys.exit(1)
    d = parse(raw)
    if not d.get("name"):
        print(f"未解析到行情数据(代码={norm}), 请检查代码是否正确。")
        sys.exit(1)
    render(d, do_screen)


if __name__ == "__main__":
    main()
