#!/usr/bin/env python3
"""
Longbridge 账户余额查询

使用长桥证券 API 获取账户资金和资产信息
"""

import os
import sys

# 导入共享配置模块
try:
    from longbridge_config import find_config_file, load_config, show_config_help
except ImportError:
    # 如果作为独立脚本运行，从同目录导入
    sys.path.insert(0, os.path.dirname(__file__))
    from longbridge_config import find_config_file, load_config, show_config_help

try:
    from longport.openapi import Config, TradeContext
except ImportError:
    print("❌ 错误: 未安装 longport-openapi SDK")
    print("   请运行: pip3 install longport")
    sys.exit(1)


class LongBridgeAccount:
    """长桥证券账户查询"""

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

        # 创建 TradeContext
        try:
            ctx_config = Config(
                app_key=self.config.get('LONGPORT_APP_KEY'),
                app_secret=self.config.get('LONGPORT_APP_SECRET'),
                access_token=self.config.get('LONGPORT_ACCESS_TOKEN'),
                http_url=self.config.get('LONGPORT_HTTP_URL', 'https://openapi.longportapp.cn'),
                trade_ws_url=self.config.get('LONGPORT_TRADE_WS_URL', 'wss://openapi-trade.longportapp.cn')
            )
            self.trade_ctx = TradeContext(ctx_config)
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            sys.exit(1)

    def get_balance(self):
        """
        获取账户余额

        Returns:
            余额数据列表
        """
        try:
            balances = self.trade_ctx.account_balance()
            return balances
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return []

    def format_balance(self, balance):
        """格式化余额输出（Markdown 格式）"""
        lines = [
            f"## 💰 {balance.currency} 账户余额",
            f"",
            f"| 指标 | 金额 |",
            f"|------|------|",
            f"| **总现金** | `{balance.total_cash:,.2f}` |",
            f"| **购买力** | `{balance.buy_power:,.2f}` |",
            f"| **净资产** | `{balance.net_assets:,.2f}` |",
            f"| 风险等级 | `{balance.risk_level}` |",
            f"| 初始保证金 | `{balance.init_margin:,.2f}` |",
            f"| 维持保证金 | `{balance.maintenance_margin:,.2f}` |",
        ]
        return '\n'.join(lines)


def main():
    """命令行入口"""
    print("正在初始化 Longbridge API...")
    account = LongBridgeAccount()

    # 查询
    print("\n正在查询账户余额...")
    balances = account.get_balance()

    if not balances:
        print("\n❌ 未获取到余额信息")
        sys.exit(1)

    # 输出
    for balance in balances:
        print('\n' + account.format_balance(balance))

    print('\n✅ 查询完成')


if __name__ == "__main__":
    main()
