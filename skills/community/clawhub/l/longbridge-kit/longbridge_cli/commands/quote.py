"""行情命令模块"""
import click
from longbridge.openapi import QuoteContext, Period, AdjustType

from longbridge_cli.config import get_config
from longbridge_cli.formatters import print_table, print_json, print_error

PERIOD_MAP = {
    "1m": Period.Min_1,
    "5m": Period.Min_5,
    "15m": Period.Min_15,
    "30m": Period.Min_30,
    "60m": Period.Min_60,
    "day": Period.Day,
    "week": Period.Week,
    "month": Period.Month,
    "quarter": Period.Quarter,
    "year": Period.Year,
}


@click.command("quote")
@click.argument("symbols", nargs=-1, required=True)
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def quote_cmd(ctx, symbols, output_json):
    """获取实时报价（支持多个标的）

    示例：longbridge quote AAPL.US 700.HK
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.quote(list(symbols))
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = [
            {
                "symbol": q.symbol,
                "last_done": float(q.last_done),
                "open": float(q.open),
                "high": float(q.high),
                "low": float(q.low),
                "volume": q.volume,
                "turnover": float(q.turnover),
                "change_rate": round(float(q.last_done / q.prev_close - 1) * 100, 2) if q.prev_close else None,
                "prev_close": float(q.prev_close),
            }
            for q in resp
        ]
        print_json(data)
    else:
        headers = ["标的", "最新价", "涨跌幅", "开盘", "最高", "最低", "成交量", "成交额"]
        rows = []
        for q in resp:
            change_rate = round(float(q.last_done / q.prev_close - 1) * 100, 2) if q.prev_close else "-"
            change_str = f"{change_rate:+.2f}%" if isinstance(change_rate, float) else change_rate
            rows.append([
                q.symbol,
                f"{float(q.last_done):.3f}",
                change_str,
                f"{float(q.open):.3f}",
                f"{float(q.high):.3f}",
                f"{float(q.low):.3f}",
                f"{q.volume:,}",
                f"{float(q.turnover):,.0f}",
            ])
        print_table(headers, rows, title="实时报价")


@click.command("depth")
@click.argument("symbol")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def depth_cmd(ctx, symbol, output_json):
    """查看盘口（买5卖5）

    示例：longbridge depth 700.HK
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.depth(symbol)
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = {
            "symbol": symbol,
            "asks": [{"position": a.position, "price": float(a.price), "volume": a.volume} for a in resp.asks],
            "bids": [{"position": b.position, "price": float(b.price), "volume": b.volume} for b in resp.bids],
        }
        print_json(data)
    else:
        headers = ["方向", "档位", "价格", "数量"]
        rows = []
        for a in reversed(resp.asks):
            rows.append(["卖", str(a.position), f"{float(a.price):.3f}", f"{a.volume:,}"])
        for b in resp.bids:
            rows.append(["买", str(b.position), f"{float(b.price):.3f}", f"{b.volume:,}"])
        print_table(headers, rows, title=f"盘口 - {symbol}")


@click.command("trades")
@click.argument("symbol")
@click.option("--count", default=20, show_default=True, help="返回条数（最多 1000）")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def trades_cmd(ctx, symbol, count, output_json):
    """查看最近逐笔成交

    示例：longbridge trades 700.HK --count 20
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.trades(symbol, count)
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = [
            {
                "price": float(t.price),
                "volume": t.volume,
                "timestamp": t.timestamp.isoformat() if t.timestamp else None,
                "direction": str(t.trade_type),
            }
            for t in resp
        ]
        print_json(data)
    else:
        headers = ["时间", "价格", "数量", "类型"]
        rows = [
            [
                t.timestamp.strftime("%H:%M:%S") if t.timestamp else "-",
                f"{float(t.price):.3f}",
                f"{t.volume:,}",
                str(t.trade_type),
            ]
            for t in resp
        ]
        print_table(headers, rows, title=f"逐笔成交 - {symbol}")


@click.command("candlesticks")
@click.argument("symbol")
@click.argument("period", type=click.Choice(list(PERIOD_MAP.keys())))
@click.option("--count", default=30, show_default=True, help="返回K线条数（最多 1000）")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def candlesticks_cmd(ctx, symbol, period, count, output_json):
    """查看 K 线数据

    PERIOD 可选：1m 5m 15m 30m 60m day week month quarter year

    示例：longbridge candlesticks AAPL.US day --count 30
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.candlesticks(symbol, PERIOD_MAP[period], count, AdjustType.NoAdjust)
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = [
            {
                "timestamp": c.timestamp.isoformat() if c.timestamp else None,
                "open": float(c.open),
                "high": float(c.high),
                "low": float(c.low),
                "close": float(c.close),
                "volume": c.volume,
                "turnover": float(c.turnover),
            }
            for c in resp
        ]
        print_json(data)
    else:
        headers = ["时间", "开盘", "最高", "最低", "收盘", "成交量"]
        rows = [
            [
                c.timestamp.strftime("%Y-%m-%d %H:%M") if c.timestamp else "-",
                f"{float(c.open):.3f}",
                f"{float(c.high):.3f}",
                f"{float(c.low):.3f}",
                f"{float(c.close):.3f}",
                f"{c.volume:,}",
            ]
            for c in resp
        ]
        print_table(headers, rows, title=f"K线 - {symbol} ({period})")


@click.command("info")
@click.argument("symbols", nargs=-1, required=True)
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def info_cmd(ctx, symbols, output_json):
    """查看标的静态基本信息（名称、交易所、类型等）

    示例：longbridge info 700.HK AAPL.US
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.static_info(list(symbols))
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = [
            {
                "symbol": s.symbol,
                "name_cn": s.name_cn,
                "name_en": s.name_en,
                "exchange": s.exchange,
                "currency": s.currency,
                "lot_size": s.lot_size,
                "total_shares": s.total_shares,
                "circulating_shares": s.circulating_shares,
                "board": str(s.board),
            }
            for s in resp
        ]
        print_json(data)
    else:
        headers = ["标的", "中文名", "英文名", "交易所", "币种", "手数", "板块"]
        rows = [
            [
                s.symbol,
                s.name_cn,
                s.name_en,
                s.exchange,
                s.currency,
                str(s.lot_size),
                str(s.board),
            ]
            for s in resp
        ]
        print_table(headers, rows, title="标的信息")
