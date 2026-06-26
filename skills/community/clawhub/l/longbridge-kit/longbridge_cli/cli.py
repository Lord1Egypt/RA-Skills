"""longbridge-cli 根命令组"""
import click

from longbridge_cli.commands.quote import (
    quote_cmd,
    depth_cmd,
    trades_cmd,
    candlesticks_cmd,
    info_cmd,
)
from longbridge_cli.commands.account import balance_cmd, positions_cmd, funds_cmd
from longbridge_cli.commands.order import (
    orders_cmd,
    history_orders_cmd,
    buy_cmd,
    sell_cmd,
    cancel_cmd,
)
from longbridge_cli.commands.market import (
    temperature_cmd,
    capital_flow_cmd,
    capital_dist_cmd,
    option_chain_cmd,
)


@click.group()
@click.version_option("1.0.0", prog_name="longbridge")
@click.option("--profile", default=None, help="账户 profile（如 paper），加载 .{profile}.env 凭证文件")
@click.pass_context
def cli(ctx, profile):
    """长桥 LongPort OpenAPI CLI 工具

    \b
    行情：  quote depth trades candlesticks info
    账户：  balance positions funds
    订单：  orders history-orders buy sell cancel
    市场：  temperature capital-flow capital-dist option-chain

    所有命令支持 --json 输出 JSON 格式。
    """
    ctx.ensure_object(dict)
    ctx.obj["profile"] = profile


# 行情
cli.add_command(quote_cmd, name="quote")
cli.add_command(depth_cmd, name="depth")
cli.add_command(trades_cmd, name="trades")
cli.add_command(candlesticks_cmd, name="candlesticks")
cli.add_command(info_cmd, name="info")

# 账户
cli.add_command(balance_cmd, name="balance")
cli.add_command(positions_cmd, name="positions")
cli.add_command(funds_cmd, name="funds")

# 订单
cli.add_command(orders_cmd, name="orders")
cli.add_command(history_orders_cmd, name="history-orders")
cli.add_command(buy_cmd, name="buy")
cli.add_command(sell_cmd, name="sell")
cli.add_command(cancel_cmd, name="cancel")

# 市场
cli.add_command(temperature_cmd, name="temperature")
cli.add_command(capital_flow_cmd, name="capital-flow")
cli.add_command(capital_dist_cmd, name="capital-dist")
cli.add_command(option_chain_cmd, name="option-chain")
