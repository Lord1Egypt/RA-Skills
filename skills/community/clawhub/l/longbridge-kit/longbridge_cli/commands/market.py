"""市场数据命令模块"""
import click
from longbridge.openapi import QuoteContext, Market

from longbridge_cli.config import get_config
from longbridge_cli.formatters import print_table, print_json, print_kv, print_error

MARKET_MAP = {
    "US": Market.US,
    "HK": Market.HK,
    "CN": Market.CN,
    "SG": Market.SG,
}


@click.command("temperature")
@click.argument("market", type=click.Choice(["US", "HK", "CN", "SG"]))
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def temperature_cmd(ctx, market, output_json):
    """查看市场温度

    MARKET 可选：US HK CN SG

    示例：longbridge temperature US
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.market_temperature(MARKET_MAP[market])
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = {
            "market": market,
            "temperature": resp.temperature,
            "description": resp.description,
            "valuation": float(resp.valuation) if hasattr(resp, "valuation") else None,
        }
        print_json(data)
    else:
        pairs = [
            ("市场", market),
            ("温度", resp.temperature),
            ("描述", resp.description),
        ]
        if hasattr(resp, "valuation"):
            pairs.append(("估值", float(resp.valuation)))
        print_kv(pairs, title=f"市场温度 - {market}")


@click.command("capital-flow")
@click.argument("symbol")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def capital_flow_cmd(ctx, symbol, output_json):
    """查看资金流向

    示例：longbridge capital-flow 700.HK
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.capital_flow(symbol)
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = [
            {
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "inflow": float(item.inflow),
            }
            for item in resp
        ]
        print_json(data)
    else:
        headers = ["时间", "净流入"]
        rows = [
            [
                item.timestamp.strftime("%Y-%m-%d %H:%M") if item.timestamp else "-",
                f"{float(item.inflow):+,.0f}",
            ]
            for item in resp
        ]
        print_table(headers, rows, title=f"资金流向 - {symbol}")


@click.command("capital-dist")
@click.argument("symbol")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def capital_dist_cmd(ctx, symbol, output_json):
    """查看资金分布

    示例：longbridge capital-dist 700.HK
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.capital_distribution(symbol)
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = {
            "symbol": symbol,
            "timestamp": resp.timestamp.isoformat() if resp.timestamp else None,
            "capital_in": {
                "large": float(resp.capital_in.large),
                "medium": float(resp.capital_in.medium),
                "small": float(resp.capital_in.small),
            },
            "capital_out": {
                "large": float(resp.capital_out.large),
                "medium": float(resp.capital_out.medium),
                "small": float(resp.capital_out.small),
            },
        }
        print_json(data)
    else:
        headers = ["方向", "大单", "中单", "小单"]
        rows = [
            [
                "流入",
                f"{float(resp.capital_in.large):,.0f}",
                f"{float(resp.capital_in.medium):,.0f}",
                f"{float(resp.capital_in.small):,.0f}",
            ],
            [
                "流出",
                f"{float(resp.capital_out.large):,.0f}",
                f"{float(resp.capital_out.medium):,.0f}",
                f"{float(resp.capital_out.small):,.0f}",
            ],
        ]
        print_table(headers, rows, title=f"资金分布 - {symbol}")


@click.command("option-chain")
@click.argument("symbol")
@click.option("--json", "output_json", is_flag=True, help="以 JSON 格式输出")
@click.pass_context
def option_chain_cmd(ctx, symbol, output_json):
    """查看期权链到期日列表

    示例：longbridge option-chain AAPL.US
    """
    try:
        quote_ctx = QuoteContext(get_config(ctx.obj.get("profile")))
        resp = quote_ctx.option_chain_expiry_date_list(symbol)
    except Exception as e:
        print_error(str(e))

    if output_json:
        data = {
            "symbol": symbol,
            "expiry_dates": [d.isoformat() for d in resp],
        }
        print_json(data)
    else:
        headers = ["序号", "到期日"]
        rows = [[str(i + 1), d.strftime("%Y-%m-%d")] for i, d in enumerate(resp)]
        print_table(headers, rows, title=f"期权链到期日 - {symbol}")
