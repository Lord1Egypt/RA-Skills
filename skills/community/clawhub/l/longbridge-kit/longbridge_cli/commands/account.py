"""账户与持仓命令模块"""
import click
from longbridge.openapi import TradeContext

from longbridge_cli.config import get_config
from longbridge_cli.formatters import print_table, print_json, print_error


@click.command("balance")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def balance_cmd(ctx, output_json):
    """查看账户余额与净资产

    示例：longbridge balance
    """
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.account_balance()
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = [
            {
                "currency": b.currency,
                "total_cash": float(b.total_cash),
                "max_finance_amount": float(b.max_finance_amount),
                "remaining_finance_amount": float(b.remaining_finance_amount),
                "risk_level": b.risk_level,
                "margin_call": float(b.margin_call),
                "net_assets": float(b.net_assets),
                "init_margin": float(b.init_margin),
                "maintenance_margin": float(b.maintenance_margin),
            }
            for b in resp
        ]
        print_json(data)
    else:
        headers = ["币种", "现金余额", "净资产", "最大融资额", "剩余融资额", "风险等级"]
        rows = [
            [
                b.currency,
                f"{float(b.total_cash):,.2f}",
                f"{float(b.net_assets):,.2f}",
                f"{float(b.max_finance_amount):,.2f}",
                f"{float(b.remaining_finance_amount):,.2f}",
                str(b.risk_level),
            ]
            for b in resp
        ]
        print_table(headers, rows, title="账户余额")


@click.command("positions")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def positions_cmd(ctx, output_json):
    """查看股票持仓

    示例：longbridge positions
    """
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.stock_positions()
    except Exception as e:
        print_error(str(e))

    channels = resp.channels if resp else []

    if output_json:
        data = []
        for ch in channels:
            for p in ch.positions:
                data.append({
                    "symbol": p.symbol,
                    "symbol_name": p.symbol_name,
                    "quantity": p.quantity,
                    "available_quantity": p.available_quantity,
                    "currency": p.currency,
                    "cost_price": float(p.cost_price),
                    "init_quantity": p.init_quantity,
                    "market": str(p.market),
                })
        print_json(data)
    else:
        headers = ["标的", "名称", "持仓", "可卖", "成本价", "初始持仓", "市场", "币种"]
        rows = []
        for ch in channels:
            for p in ch.positions:
                rows.append([
                    p.symbol,
                    p.symbol_name,
                    str(p.quantity),
                    str(p.available_quantity),
                    f"{float(p.cost_price):.3f}",
                    str(p.init_quantity),
                    str(p.market),
                    p.currency,
                ])
        print_table(headers, rows, title="股票持仓")


@click.command("funds")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def funds_cmd(ctx, output_json):
    """查看基金持仓

    示例：longbridge funds
    """
    try:
        trade_ctx = TradeContext(get_config(ctx.obj.get("profile")))
        resp = trade_ctx.fund_positions()
    except Exception as e:
        print_error(str(e))

    channels = resp.channels if resp else []

    if output_json:
        data = []
        for ch in channels:
            for f in ch.positions:
                data.append({
                    "symbol": f.symbol,
                    "symbol_name": f.symbol_name,
                    "holding_units": float(f.holding_units),
                    "current_net_asset_value": float(f.current_net_asset_value),
                    "cost_net_asset_value": float(f.cost_net_asset_value),
                    "net_asset_value_day": f.net_asset_value_day.isoformat() if f.net_asset_value_day else None,
                    "market_value": float(f.market_value) if hasattr(f, "market_value") else None,
                })
        print_json(data)
    else:
        headers = ["基金代码", "名称", "持有份额", "当前净值", "成本净值", "净值日期"]
        rows = []
        for ch in channels:
            for f in ch.positions:
                rows.append([
                    f.symbol,
                    f.symbol_name,
                    f"{float(f.holding_units):.4f}",
                    f"{float(f.current_net_asset_value):.4f}",
                    f"{float(f.cost_net_asset_value):.4f}",
                    f.net_asset_value_day.strftime("%Y-%m-%d") if f.net_asset_value_day else "-",
                ])
        print_table(headers, rows, title="基金持仓")
