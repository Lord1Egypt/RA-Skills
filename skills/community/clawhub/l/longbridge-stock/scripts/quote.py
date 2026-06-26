#!/usr/bin/env python3
"""
Longbridge 股票实时行情查询

使用长桥证券 API 获取股票实时价格
"""

import os
import sys
from datetime import datetime

# 导入共享配置模块
try:
    from longbridge_config import find_config_file, load_config, show_config_help
except ImportError:
    # 如果作为独立脚本运行，从同目录导入
    sys.path.insert(0, os.path.dirname(__file__))
    from longbridge_config import find_config_file, load_config, show_config_help

try:
    from longport.openapi import Config, QuoteContext
except ImportError:
    print("❌ 错误: 未安装 longport-openapi SDK")
    print("   请运行: pip3 install longport")
    sys.exit(1)


class LongBridgeStock:
    """长桥证券股票查询"""

    def __init__(self, config_path=None):
        """
        初始化

        Args:
            config_path: 配置文件路径（可选）
        """
        # 确定配置文件路径
        if config_path is None:
            config_path = find_config_file()

        if not config_path or not os.path.exists(config_path):
            show_config_help(config_path)
            sys.exit(1)

        # 加载配置
        self.config = load_config(config_path)

        if not self.config:
            sys.exit(1)

        # 创建 QuoteContext
        try:
            ctx_config = Config(
                app_key=self.config.get('LONGPORT_APP_KEY'),
                app_secret=self.config.get('LONGPORT_APP_SECRET'),
                access_token=self.config.get('LONGPORT_ACCESS_TOKEN'),
                http_url=self.config.get('LONGPORT_HTTP_URL', 'https://openapi.longportapp.cn'),
                quote_ws_url=self.config.get('LONGPORT_QUOTE_WS_URL', 'wss://openapi-quote.longportapp.cn')
            )
            self.quote_ctx = QuoteContext(ctx_config)
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            sys.exit(1)

    def get_quote(self, symbols):
        """
        获取实时行情

        Args:
            symbols: 股票代码列表，如 ['AAPL.US', '700.HK', 'GOOGL.US']

        Returns:
            行情数据字典
        """
        try:
            quotes = self.quote_ctx.quote(symbols)

            result = {}
            for quote in quotes:
                quote_data = {
                    'symbol': quote.symbol,
                    'last_price': quote.last_done,
                    'open': quote.open,
                    'high': quote.high,
                    'low': quote.low,
                    'prev_close': quote.prev_close,
                    'volume': quote.volume,
                    'turnover': quote.turnover,
                    'change': quote.last_done - quote.prev_close if quote.prev_close else 0,
                    'change_percent': ((quote.last_done - quote.prev_close) / quote.prev_close * 100) if quote.prev_close else 0,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                # 盘前价格
                if hasattr(quote, 'pre_market_quote'):
                    quote_data['pre_market_quote'] = quote.pre_market_quote.last_done if quote.pre_market_quote else None
                else:
                    quote_data['pre_market_quote'] = None

                # 盘后价格
                if hasattr(quote, 'post_market_quote'):
                    quote_data['post_market_quote'] = quote.post_market_quote.last_done if quote.post_market_quote else None
                else:
                    quote_data['post_market_quote'] = None

                # 交易状态
                if hasattr(quote, 'trade_status'):
                    quote_data['trade_status'] = quote.trade_status
                else:
                    quote_data['trade_status'] = None

                result[quote.symbol] = quote_data

            return result
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return {}

    def format_quote(self, quote):
        """格式化行情输出"""
        change = quote['change']
        change_pct = quote['change_percent']
        symbol_emoji = "📈" if change >= 0 else "📉"

        # 判断市场类型和货币符号
        symbol = quote['symbol']
        if symbol.endswith('.HK'):
            market = '港股'
            currency_symbol = 'HK$'
            show_us_time = False
        elif symbol.endswith('.SH') or symbol.endswith('.SZ'):
            market = 'A股'
            currency_symbol = '¥'
            show_us_time = False
        elif symbol.endswith('.US'):
            market = '美股'
            currency_symbol = '$'
            show_us_time = True
        else:
            market = '未知'
            currency_symbol = '$'
            show_us_time = False

        lines = [
            f"{symbol_emoji} {quote['symbol']} [{market}]",
            "",
        ]

        # 只为美股显示交易时间
        if show_us_time:
            lines.extend([
                f"美股交易时间（北京时间）：",
                f"  盘前：17:00 - 22:30",
                f"  正盘：22:30 - 次日05:00",
                f"  盘后：05:00 - 09:00",
                "",
            ])

        # 价格信息
        lines.extend([
            f"【基本信息】",
            f"  当前价格：{currency_symbol}{quote['last_price']:.2f}",
            f"  开盘价：{currency_symbol}{quote['open']:.2f}",
            f"  最高价：{currency_symbol}{quote['high']:.2f}",
            f"  最低价：{currency_symbol}{quote['low']:.2f}",
            f"  昨收价：{currency_symbol}{quote['prev_close']:.2f}",
            "",
        ])

        # 涨跌信息
        if change >= 0:
            lines.append(f"  涨跌额：{currency_symbol}+{change:+.2f}")
        else:
            lines.append(f"  涨跌额：{currency_symbol}{change:+.2f}")

        lines.append(f"  涨跌幅：{change_pct:+.2f}%")
        lines.append("")

        # 盘前/盘后
        if quote.get('pre_market_quote'):
            lines.append(f"  盘前价：{currency_symbol}{quote['pre_market_quote']:.2f}")
        else:
            lines.append("  盘前价：无")
        lines.append("")

        if quote.get('post_market_quote'):
            lines.append(f"  盘后价：{currency_symbol}{quote['post_market_quote']:.2f}")
        else:
            lines.append("  盘后价：无")
        lines.append("")

        # 成交量数据
        lines.extend([
            f"【成交数据】",
            f"  成交量：{quote['volume']:,}",
            f"  成交额：{currency_symbol}{quote['turnover']:,.0f}",
        ])

        # 交易状态
        if quote.get('trade_status'):
            lines.append(f"交易状态：{quote['trade_status']}")
        else:
            lines.append("交易状态：未知")

        lines.append(f"更新时间：{quote['timestamp']}")

        return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python3 quote.py <股票代码1> [股票代码2] ...")
        print("示例: python3 quote.py AAPL.US GOOGL.US")
        sys.exit(1)

    # 解析股票代码
    symbols = sys.argv[1:]

    # 初始化
    print(f"正在初始化 Longbridge API...")
    stock = LongBridgeStock()

    # 查询
    print(f"\n正在查询: {', '.join(symbols)}")
    quotes = stock.get_quote(symbols)

    # 输出
    for symbol in symbols:
        if symbol in quotes:
            print('\n' + stock.format_quote(quotes[symbol]))
        else:
            print(f'\n❌ 未找到股票: {symbol}')


if __name__ == "__main__":
    main()
