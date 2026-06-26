"""订单管理命令模块"""
from datetime import datetime
from decimal import Decimal

import click
from longbridge.openapi import (
    TradeContext,
    OrderType,
    OrderSide,
    TimeInForceType,
)

from longbridge_cli.config import get_config, require_trade_enabled
from longbridge_cli.formatters import print_table, print_json, print_error


@click.command("orders")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def orders_cmd(ctx, output_json):
    """查看今日订单

    示例：longbridge orders
    """
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.today_orders()
    except Exception as e:
        print_error(str(e))

    _print_orders(resp, output_json, "今日订单")


@click.command("history-orders")
@click.option("--start", required=True, help="开始日期 (YYYY-MM-DD)")
@click.option("--end", required=True, help="结束日期 (YYYY-MM-DD)")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def history_orders_cmd(ctx, start, end, output_json):
    """查看历史订单

    示例：longbridge history-orders --start 2026-01-01 --end 2026-03-14
    """
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.history_orders(start_at=start_dt, end_at=end_dt)
    except ValueError:
        print_error("日期格式错误，请使用 YYYY-MM-DD")
        return
    except Exception as e:
        print_error(str(e))

    _print_orders(resp, output_json, f"历史订单 ({start} ~ {end})")


@click.command("buy")
@click.argument("symbol")
@click.option("--qty", required=True, type=int, help="买入数量")
@click.option("--price", required=True, type=float, help="限价价格")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.option("--yes", "-y", is_flag=True, help="跳过交互确认（程序化调用时使用）")
@click.pass_context
def buy_cmd(ctx, symbol, qty, price, output_json, yes):
    """限价买入

    示例：longbridge buy AAPL.US --qty 100 --price 180.0
    """
    require_trade_enabled()
    if not yes:
        click.confirm(f"确认买入 {symbol}  数量 {qty}  限价 {price}？", abort=True)
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.submit_order(
            symbol,
            OrderType.LO,
            OrderSide.Buy,
            qty,
            TimeInForceType.Day,
            submitted_price=Decimal(str(price)),
        )
    except Exception as e:
        print_error(str(e))
        return

    if output_json:
        print_json({"order_id": resp.order_id})
    else:
        click.echo(f"下单成功，订单号：{resp.order_id}")


@click.command("sell")
@click.argument("symbol")
@click.option("--qty", required=True, type=int, help="卖出数量")
@click.option("--price", required=True, type=float, help="限价价格")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.option("--yes", "-y", is_flag=True, help="跳过交互确认（程序化调用时使用）")
@click.pass_context
def sell_cmd(ctx, symbol, qty, price, output_json, yes):
    """限价卖出

    示例：longbridge sell 700.HK --qty 500 --price 320.0
    """
    require_trade_enabled()
    if not yes:
        click.confirm(f"确认卖出 {symbol}  数量 {qty}  限价 {price}？", abort=True)
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.submit_order(
            symbol,
            OrderType.LO,
            OrderSide.Sell,
            qty,
            TimeInForceType.Day,
            submitted_price=Decimal(str(price)),
        )
    except Exception as e:
        print_error(str(e))
        return

    if output_json:
        print_json({"order_id": resp.order_id})
    else:
        click.echo(f"下单成功，订单号：{resp.order_id}")


@click.command("cancel")
@click.argument("order_id")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def cancel_cmd(ctx, order_id, output_json):
    """撤销订单

    示例：longbridge cancel 701234567890
    """
    require_trade_enabled()
    click.confirm(f"确认撤销订单 {order_id}？", abort=True)
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        trade_ctx.cancel_order(order_id)
    except Exception as e:
        print_error(str(e))

    if output_json:
        print_json({"order_id": order_id, "status": "cancelled"})
    else:
        click.echo(f"订单 {order_id} 已撤销")


def _print_orders(orders, output_json: bool, title: str) -> None:
    """内部辅助：统一输出订单列表"""
    if output_json:
        data = [
            {
                "order_id": o.order_id,
                "symbol": o.symbol,
                "side": str(o.side),
                "order_type": str(o.order_type),
                "quantity": o.quantity,
                "executed_quantity": o.executed_quantity,
                "price": float(o.price) if o.price else None,
                "executed_price": float(o.executed_price) if o.executed_price else None,
                "status": str(o.status),
                "submitted_at": o.submitted_at.isoformat() if o.submitted_at else None,
                "updated_at": o.updated_at.isoformat() if o.updated_at else None,
            }
            for o in orders
        ]
        print_json(data)
    else:
        headers = ["订单号", "标的", "方向", "类型", "数量", "已成交", "委托价", "成交价", "状态", "提交时间"]
        rows = [
            [
                o.order_id,
                o.symbol,
                str(o.side),
                str(o.order_type),
                str(o.quantity),
                str(o.executed_quantity),
                f"{float(o.price):.3f}" if o.price else "-",
                f"{float(o.executed_price):.3f}" if o.executed_price else "-",
                str(o.status),
                o.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if o.submitted_at else "-",
            ]
            for o in orders
        ]
        print_table(headers, rows, title=title)
