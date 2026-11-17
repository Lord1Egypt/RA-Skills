#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金模拟大赛：账户、行情、交易、记录查询。

通过 cf-gold-ai BFF 调用 ic-community-sim-client 服务。

子命令：
  account           查询/初始化模拟账户
  time-sharing      查询分时行情
  kline             查询K线行情
  buy               模拟买入
  sell              模拟卖出
  overview          查询交易总览
  records           查询交易记录（分页）

所有子命令均需先完成 OAuth 登录（通过 jos.py login）。
"""
import argparse
import json
import sys
import urllib.error

import bff_client
import jos


# ── 底层接口调用 ───────────────────────────────────────────────────

def _call_sim_account(access_token: str, account_type: int = 1) -> dict:
    """查询/初始化模拟账户。"""
    return bff_client.post_json(bff_client.PATH_SIM_ACCOUNT, {
        "accessToken": access_token,
        "accountType": account_type,
    })


def _call_sim_time_sharing(access_token: str, unique_code: str,
                           type_: str = "m1", from_: str = None,
                           to: str = None, nums: int = None) -> dict:
    """查询分时行情数据。"""
    body = {
        "accessToken": access_token,
        "uniqueCode": unique_code,
        "type": type_,
    }
    if from_:
        body["from"] = from_
    if to:
        body["to"] = to
    if nums is not None:
        body["nums"] = nums
    return bff_client.post_json(bff_client.PATH_SIM_QUOTE_TIME_SHARING, body)


def _call_sim_kline(access_token: str, unique_code: str,
                    k_type: str = "day", af_type: str = "bfq",
                    from_: str = None, nums: int = None) -> dict:
    """查询K线行情数据。"""
    body = {
        "accessToken": access_token,
        "uniqueCode": unique_code,
        "kType": k_type,
        "afType": af_type,
    }
    if from_:
        body["from"] = from_
    if nums is not None:
        body["nums"] = nums
    return bff_client.post_json(bff_client.PATH_SIM_QUOTE_KLINE, body)


def _call_sim_buy(access_token: str, trade_unit: int, bus_id: str,
                  trade_amount=None, trade_gram=None,
                  account_type: int = 1) -> dict:
    """模拟买入交易。"""
    body = {
        "accessToken": access_token,
        "accountType": account_type,
        "tradeUnit": trade_unit,
        "busId": bus_id,
    }
    if trade_amount is not None:
        body["tradeAmount"] = str(trade_amount)
    if trade_gram is not None:
        body["tradeGram"] = str(trade_gram)
    return bff_client.post_json(bff_client.PATH_SIM_BUY, body)


def _call_sim_sell(access_token: str, trade_unit: int, bus_id: str,
                   trade_gram=None, trade_ratio=None,
                   account_type: int = 1) -> dict:
    """模拟卖出交易。"""
    body = {
        "accessToken": access_token,
        "accountType": account_type,
        "tradeUnit": trade_unit,
        "busId": bus_id,
    }
    if trade_gram is not None:
        body["tradeGram"] = str(trade_gram)
    if trade_ratio is not None:
        body["tradeRatio"] = str(trade_ratio)
    return bff_client.post_json(bff_client.PATH_SIM_SELL, body)


def _call_sim_trade_overview(access_token: str, account_type: int = 1) -> dict:
    """查询交易总览。"""
    return bff_client.post_json(bff_client.PATH_SIM_TRADE_OVERVIEW, {
        "accessToken": access_token,
        "accountType": account_type,
    })


def _call_sim_trade_records(access_token: str, last_id: str = None,
                            page_size: int = 8, account_type: int = 1) -> dict:
    """查询交易记录（分页）。"""
    body = {
        "accessToken": access_token,
        "accountType": account_type,
        "pageSize": page_size,
    }
    if last_id:
        body["lastId"] = last_id
    return bff_client.post_json(bff_client.PATH_SIM_TRADE_RECORDS, body)


# ── 格式化输出 ────────────────────────────────────────────────────

def _fmt_num(v, digits=2):
    if v is None:
        return "—"
    try:
        n = float(v)
        return f"{n:,.{digits}f}"
    except (TypeError, ValueError):
        return str(v)


def _fmt_amount(v):
    """金叶子金额格式化。"""
    return _fmt_num(v, 2)


def render_account(data: dict) -> str:
    """渲染模拟账户信息。"""
    if not data:
        return "> ⚠️ 未获取到模拟账户信息。"
    lines = ["## 🎮 黄金模拟大赛账户", ""]
    lines.append("| 项目 | 数值 |")
    lines.append("| --- | ---: |")
    lines.append(f"| 🆔 账户ID | {data.get('accountId', '—')} |")
    lines.append(f"| 💰 可用额度(金叶子) | {_fmt_amount(data.get('availableAmount'))} |")
    lines.append(f"| ⚖️ 当前持仓(克) | {_fmt_num(data.get('currentHoldingGram'), 4)} |")
    lines.append(f"| 💵 成本均价(金叶子/克) | {_fmt_amount(data.get('costAvgPerGram'))} |")
    lines.append(f"| 💎 总资产(金叶子) | {_fmt_amount(data.get('totalAsset'))} |")
    lines.append(f"| 📈 累计收益(金叶子) | {_fmt_amount(data.get('totalProfit'))} |")
    lines.append(f"| 📊 持仓盈亏(金叶子) | {_fmt_amount(data.get('holdingProfit'))} |")
    lines.append(f"| 🛒 累计买入 | {data.get('totalBuyCount', 0)}笔 / {_fmt_amount(data.get('totalBuyAmount'))}金叶子 |")
    lines.append(f"| 🏷️ 累计卖出 | {data.get('totalSellCount', 0)}笔 / {_fmt_amount(data.get('totalSellAmount'))}金叶子 |")
    return "\n".join(lines)


def render_trade_overview(data: dict) -> str:
    """渲染交易总览。"""
    if not data:
        return "> ⚠️ 未获取到交易总览数据。"
    lines = ["## 📊 模拟交易总览", ""]
    buy_info = data.get("buyInfo") or {}
    sell_info = data.get("sellInfo") or {}
    lines.append("| 类型 | 交易次数 | 总金额(金叶子) |")
    lines.append("| --- | ---: | ---: |")
    lines.append(f"| 🛒 买入 | {buy_info.get('count', 0)} | {_fmt_amount(buy_info.get('totalAmount'))} |")
    lines.append(f"| 🏷️ 卖出 | {sell_info.get('count', 0)} | {_fmt_amount(sell_info.get('totalAmount'))} |")
    return "\n".join(lines)


def render_trade_records(data: dict) -> str:
    """渲染交易记录。"""
    if not data:
        return "> ⚠️ 未获取到交易记录。"
    records = data.get("records") or []
    has_more = data.get("hasMore", False)
    last_id = data.get("lastId")
    if not records:
        return "> ℹ️ 暂无交易记录。"
    lines = ["## 📋 模拟交易记录", ""]
    lines.append("| 日期 | 时间 | 类型 | 克数 | 金价 | 金额 | 手续费 |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: |")
    for r in records:
        lines.append(
            f"| {r.get('tradeDate', '—')} "
            f"| {r.get('tradeTime', '—')} "
            f"| {r.get('tradeTypeDesc', '—')} "
            f"| {r.get('tradeGramDesc', '—')} "
            f"| {r.get('tradePriceDesc', '—')} "
            f"| {r.get('tradeAmountDesc', '—')} "
            f"| {r.get('feeAmount', '—')} |"
        )
    if has_more and last_id:
        lines.append("")
        lines.append(f"> 📄 还有更多记录，翻页游标：`{last_id}`")
    return "\n".join(lines)


def render_buy_result(data: dict) -> str:
    """渲染买入结果。"""
    if not data:
        return "> ⚠️ 买入失败，未获取到结果。"
    lines = ["## ✅ 模拟买入成功", ""]
    lines.append(f"- **流水号**：{data.get('tradeNo', '—')}")
    lines.append(f"- **成交描述**：{data.get('tradeAmountAndGramDesc', '—')}")
    lines.append(f"- **成交金价**：{data.get('tradePriceDesc', '—')}")
    lines.append(f"- **成交时间**：{data.get('tradeTime', '—')}")
    return "\n".join(lines)


def render_sell_result(data: dict) -> str:
    """渲染卖出结果。"""
    if not data:
        return "> ⚠️ 卖出失败，未获取到结果。"
    lines = ["## ✅ 模拟卖出成功", ""]
    lines.append(f"- **流水号**：{data.get('tradeNo', '—')}")
    lines.append(f"- **成交描述**：{data.get('tradeAmountAndGramDesc', '—')}")
    lines.append(f"- **成交金价**：{data.get('tradePriceDesc', '—')}")
    lines.append(f"- **手续费**：{data.get('feeAmountDesc', '—')}")
    lines.append(f"- **成交时间**：{data.get('tradeTime', '—')}")
    return "\n".join(lines)


# ── 子命令入口 ────────────────────────────────────────────────────

def cmd_account(args):
    access_token = jos._valid_access_token()
    data = _call_sim_account(access_token, args.account_type)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_account(data))
    return 0


def cmd_time_sharing(args):
    access_token = jos._valid_access_token()
    data = _call_sim_time_sharing(
        access_token, args.unique_code, args.type,
        args.from_, args.to, args.nums,
    )
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        items = data.get("items") or data if isinstance(data, list) else []
        if isinstance(data, dict):
            items = data.get("items") or []
        print(f"## 📈 分时行情 ({args.unique_code})")
        print(f"\n共 {len(items)} 条数据")
        if items:
            print("\n| 时间 | 最新价 | 涨跌幅 | 成交量 |")
            print("| --- | ---: | ---: | ---: |")
            for item in items[:20]:  # 最多展示20条
                print(
                    f"| {item.get('showTime') or item.get('tradeTime', '—')} "
                    f"| {_fmt_num(item.get('lastPrice'))} "
                    f"| {_fmt_num(item.get('changePercent'))}% "
                    f"| {item.get('tradeVolume', '—')} |"
                )
            if len(items) > 20:
                print(f"\n> ...共 {len(items)} 条，仅展示前 20 条")
    return 0


def cmd_kline(args):
    access_token = jos._valid_access_token()
    data = _call_sim_kline(
        access_token, args.unique_code, args.k_type,
        args.af_type, args.from_, args.nums,
    )
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        items = data.get("items") or data if isinstance(data, list) else []
        if isinstance(data, dict):
            items = data.get("items") or []
        print(f"## 📊 K线行情 ({args.unique_code}, {args.k_type})")
        print(f"\n共 {len(items)} 条数据")
        if items:
            print("\n| 日期 | 开盘 | 收盘 | 最高 | 最低 | 涨跌幅 |")
            print("| --- | ---: | ---: | ---: | ---: | ---: |")
            for item in items[:20]:
                print(
                    f"| {item.get('tradeDate') or item.get('tradeTime', '—')} "
                    f"| {_fmt_num(item.get('openPrice'))} "
                    f"| {_fmt_num(item.get('closePrice'))} "
                    f"| {_fmt_num(item.get('highPrice'))} "
                    f"| {_fmt_num(item.get('lowPrice'))} "
                    f"| {_fmt_num(item.get('changePercent'))}% |"
                )
            if len(items) > 20:
                print(f"\n> ...共 {len(items)} 条，仅展示前 20 条")
    return 0


def cmd_buy(args):
    access_token = jos._valid_access_token()
    data = _call_sim_buy(
        access_token, args.trade_unit, args.bus_id,
        trade_amount=args.trade_amount, trade_gram=args.trade_gram,
        account_type=args.account_type,
    )
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_buy_result(data))
    return 0


def cmd_sell(args):
    access_token = jos._valid_access_token()
    data = _call_sim_sell(
        access_token, args.trade_unit, args.bus_id,
        trade_gram=args.trade_gram, trade_ratio=args.trade_ratio,
        account_type=args.account_type,
    )
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_sell_result(data))
    return 0


def cmd_overview(args):
    access_token = jos._valid_access_token()
    data = _call_sim_trade_overview(access_token, args.account_type)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_trade_overview(data))
    return 0


def cmd_records(args):
    access_token = jos._valid_access_token()
    data = _call_sim_trade_records(
        access_token, args.last_id, args.page_size, args.account_type,
    )
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_trade_records(data))
    return 0


# ── CLI 主入口 ─────────────────────────────────────────────────────

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="黄金模拟大赛：账户、行情、交易、记录查询",
    )
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")

    sub = parser.add_subparsers(dest="command")

    # account
    p_acc = sub.add_parser("account", help="查询/初始化模拟账户")
    p_acc.add_argument("--account-type", type=int, default=1)

    # time-sharing
    p_ts = sub.add_parser("time-sharing", help="查询分时行情")
    p_ts.add_argument("--unique-code", required=True, help="证券唯一编码，如 SH-000001")
    p_ts.add_argument("--type", default="m1", help="分时类型：m1/m5")
    p_ts.add_argument("--from", dest="from_", help="开始时间 yyyy-MM-dd HH:mm:ss")
    p_ts.add_argument("--to", help="结束时间 yyyy-MM-dd HH:mm:ss")
    p_ts.add_argument("--nums", type=int, help="数据条数")

    # kline
    p_kl = sub.add_parser("kline", help="查询K线行情")
    p_kl.add_argument("--unique-code", required=True, help="证券唯一编码")
    p_kl.add_argument("--k-type", default="day", help="K线类型：day/week/month/m1/m5/m15/m30/m60")
    p_kl.add_argument("--af-type", default="bfq", help="复权类型：bfq/qfq/hfq")
    p_kl.add_argument("--from", dest="from_", help="开始时间 yyyy-MM-dd HH:mm:ss")
    p_kl.add_argument("--nums", type=int, help="K线数量")

    # buy
    p_buy = sub.add_parser("buy", help="模拟买入")
    p_buy.add_argument("--trade-unit", type=int, required=True, help="1:按金额 2:按克重")
    p_buy.add_argument("--bus-id", required=True, help="业务ID（幂等）")
    p_buy.add_argument("--trade-amount", type=float, help="交易金额（按金额时必传）")
    p_buy.add_argument("--trade-gram", type=float, help="交易克数（按克重时必传）")
    p_buy.add_argument("--account-type", type=int, default=1)

    # sell
    p_sell = sub.add_parser("sell", help="模拟卖出")
    p_sell.add_argument("--trade-unit", type=int, required=True, help="2:按克重 3:按比例")
    p_sell.add_argument("--bus-id", required=True, help="业务ID（幂等）")
    p_sell.add_argument("--trade-gram", type=float, help="交易克数（按克数时必传）")
    p_sell.add_argument("--trade-ratio", type=float, help="交易比例 0.01-1.00（按比例时必传）")
    p_sell.add_argument("--account-type", type=int, default=1)

    # overview
    p_ov = sub.add_parser("overview", help="查询交易总览")
    p_ov.add_argument("--account-type", type=int, default=1)

    # records
    p_rec = sub.add_parser("records", help="查询交易记录")
    p_rec.add_argument("--last-id", help="翻页游标")
    p_rec.add_argument("--page-size", type=int, default=8, help="每页条数(默认8,最大50)")
    p_rec.add_argument("--account-type", type=int, default=1)

    args = parser.parse_args(argv)
    bff_client.set_claw(args.claw)

    if not args.command:
        parser.print_help()
        return 1

    try:
        dispatch = {
            "account": cmd_account,
            "time-sharing": cmd_time_sharing,
            "kline": cmd_kline,
            "buy": cmd_buy,
            "sell": cmd_sell,
            "overview": cmd_overview,
            "records": cmd_records,
        }
        return dispatch[args.command](args)
    except bff_client.BffError as e:
        print(f"❌ 接口错误：{e.message} (code={e.code})", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ 异常：{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
