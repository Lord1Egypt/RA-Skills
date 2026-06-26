#!/usr/bin/env python3
"""
Longbridge 持仓查询

使用长桥证券 API 获取账户持仓信息
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


class LongBridgePositions:
    """长桥证券持仓查询"""

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

    def get_positions(self):
        """
        获取持仓信息

        Returns:
            持仓数据列表
        """
        try:
            # 调用 stock_positions
            positions_resp = self.trade_ctx.stock_positions()

            # 获取 channels 字段中的持仓
            if hasattr(positions_resp, 'channels'):
                channels = positions_resp.channels

                result = []

                # 从每个 channel 获取 positions
                for channel in channels:
                    if hasattr(channel, 'positions'):
                        positions = channel.positions

                        for pos in positions:
                            # 转换为字典
                            pos_dict = {}
                            for attr in dir(pos):
                                if not attr.startswith('_'):
                                    pos_dict[attr] = getattr(pos, attr)

                            # 检查是否有 symbol
                            if pos_dict.get('symbol'):
                                pos_dict['source'] = 'channels'
                                result.append(pos_dict)

                return result
            else:
                print("❌ 返回对象没有 channels 字段")
                return []

        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return []

    def format_positions(self, positions):
        """格式化持仓输出（Markdown 格式）"""
        if not positions:
            return "❌ 没有持仓数据"

        lines = [
            f"## 📊 持仓总数: {len(positions)}",
            f"",
            f"| 股票代码 | 股票名称 | 持仓 | 可用 | 成本价 | 当前市值 | 币种 | 市场",
            f"|--------|--------|------|------|------|------|------|",
        ]

        for pos in positions:
            symbol = pos.get('symbol', 'N/A')
            symbol_name = pos.get('symbol_name', 'N/A')
            quantity = pos.get('quantity', 0)
            available = pos.get('available_quantity', 0)
            cost = pos.get('cost_price', 0)
            market_val = pos.get('market_val', 0)
            currency = pos.get('currency', 'N/A')
            market = pos.get('market', 'N/A')

            lines.extend([
                f"| {symbol} | {symbol_name} | {quantity} | {available} | ${cost:.2f} | ${market_val:.2f} | {currency} | {market}",
            ])

        # 统计数据
        total_quantity = sum(pos.get('quantity', 0) for pos in positions)
        total_cost = sum(pos.get('cost_price', 0) * pos.get('quantity', 0) for pos in positions)
        total_market = sum(pos.get('market_val', 0) for pos in positions)

        lines.extend([
            f"|--------|--------|------|------|------|------|------|",
            f"| **总计** | | **{total_quantity}** | | **${total_cost:,.2f}** | **${total_market:,.2f}** | |",
        ])

        return '\n'.join(lines)


def main():
    """命令行入口"""
    print("正在初始化 Longbridge API...")
    account = LongBridgePositions()

    # 查询
    print("\n正在查询账户持仓...")
    positions = account.get_positions()

    if not positions:
        print("\n❌ 未找到持仓信息")
        sys.exit(1)

    # 输出
    print('\n' + account.format_positions(positions))

    print("\n✅ 查询完成")


if __name__ == "__main__":
    main()
