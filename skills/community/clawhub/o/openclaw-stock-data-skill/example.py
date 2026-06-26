"""
股票数据 API Skill 使用示例

运行前请确保：
1. 已设置环境变量 STOCK_API_KEY
2. 已安装依赖: pip install requests
"""

import os
from stock_api import (
    get_stock_list,
    get_daily_data,
    get_history_data,
    get_finance_data,
    get_stock_valuation,
    get_call_auction,
    get_closing_snapshot,
    get_trade_calendar,
    search_stock_by_name,
    get_stock_info
)


def example_get_stock_list():
    """示例：获取股票列表"""
    print("=" * 50)
    print("示例 1: 获取股票列表")
    print("=" * 50)
    
    try:
        result = get_stock_list(page_size=5)
        print(f"共有 {result['total']} 只股票")
        print("\n前5只股票:")
        for stock in result['list']:
            print(f"  {stock['stock_code']}: {stock['name']} - {stock.get('industry', 'N/A')}")
    except Exception as e:
        print(f"错误: {e}")


def example_search_stock():
    """示例：搜索股票"""
    print("\n" + "=" * 50)
    print("示例 2: 搜索股票（按名称）")
    print("=" * 50)
    
    try:
        results = search_stock_by_name("平安")
        print(f"找到 {len(results)} 只相关股票:")
        for stock in results[:5]:
            print(f"  {stock['stock_code']}: {stock['name']}")
    except Exception as e:
        print(f"错误: {e}")


def example_get_daily_data():
    """示例：获取日K线数据"""
    print("\n" + "=" * 50)
    print("示例 3: 获取日K线数据")
    print("=" * 50)
    
    try:
        # 获取平安银行最近30天的日K线数据
        result = get_daily_data(
            stock_code="000001.SZ",
            start_time="2024-01-01",
            end_time="2024-01-31"
        )
        print(f"共 {result['total']} 条数据")
        print("\n前5条数据:")
        for record in result['list'][:5]:
            print(f"  {record['trade_date']}: "
                  f"开盘={record['open']}, "
                  f"收盘={record['close']}, "
                  f"涨跌幅={record['pct_chg']}%")
    except Exception as e:
        print(f"错误: {e}")


def example_get_finance_data():
    """示例：获取财务数据"""
    print("\n" + "=" * 50)
    print("示例 4: 获取财务数据")
    print("=" * 50)
    
    try:
        result = get_finance_data(
            stock_code="600000.SH",
            start_time="2024-01-01",
            end_time="2024-01-31"
        )
        print(f"共 {result['total']} 条数据")
        if result['list']:
            record = result['list'][0]
            print(f"\n最新财务数据 ({record['trade_date']}):")
            print(f"  收盘价: {record['close']}")
            print(f"  PE(TTM): {record.get('pe_ttm', 'N/A')}")
            print(f"  PB: {record.get('pb', 'N/A')}")
            print(f"  总市值: {record.get('total_mv', 'N/A')}")
    except Exception as e:
        print(f"错误: {e}")


def example_get_stock_valuation():
    """示例：获取股票估值"""
    print("\n" + "=" * 50)
    print("示例 5: 获取股票估值（按PE百分位排序）")
    print("=" * 50)
    
    try:
        results = get_stock_valuation(
            sort_by="pe_percentile",
            sort_order="asc",
            limit=5
        )
        print("PE百分位最低的5只股票:")
        for stock in results:
            print(f"  {stock['stock_code']} - {stock['stock_name']}")
            print(f"    PE(TTM): {stock.get('pe_ttm', 'N/A')}")
            print(f"    PE百分位: {stock.get('pe_percentile', 'N/A')}%")
    except Exception as e:
        print(f"错误: {e}")


def example_get_trade_calendar():
    """示例：获取交易日历"""
    print("\n" + "=" * 50)
    print("示例 6: 获取交易日历")
    print("=" * 50)
    
    try:
        calendar = get_trade_calendar(
            start_time="2024-01-01",
            end_time="2024-01-31"
        )
        print(f"共 {len(calendar)} 天")
        trading_days = [d for d in calendar if d['is_open'] == 1]
        print(f"其中交易日: {len(trading_days)} 天")
        print("\n前10天:")
        for day in calendar[:10]:
            status = "交易" if day['is_open'] == 1 else "休市"
            print(f"  {day['date']}: {status}")
    except Exception as e:
        print(f"错误: {e}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("股票数据 API Skill 使用示例")
    print("=" * 50)
    print("\n提示: 请确保已设置环境变量 STOCK_API_KEY")
    print("获取 API Key: https://data.diemeng.chat/\n")
    
    # 检查 API Key
    if not os.getenv("STOCK_API_KEY"):
        print("❌ 错误: 未设置环境变量 STOCK_API_KEY")
        print("\n请执行以下命令设置 API Key:")
        print("  Linux/macOS: export STOCK_API_KEY='your_api_key'")
        print("  Windows PowerShell: $env:STOCK_API_KEY='your_api_key'")
        print("  Windows CMD: set STOCK_API_KEY=your_api_key")
        print("\n获取 API Key: https://data.diemeng.chat/")
        return
    
    # 运行示例
    example_get_stock_list()
    example_search_stock()
    example_get_daily_data()
    example_get_finance_data()
    example_get_stock_valuation()
    example_get_trade_calendar()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
