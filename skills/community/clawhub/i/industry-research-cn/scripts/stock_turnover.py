"""
stock_turnover.py - 获取A股个股最近30个交易日换手率数据

用法：
  python stock_turnover.py <股票代码> [天数]
  python stock_turnover.py 603799 30

输出：
  - 每日收盘价 + 换手率
  - 30日累计换手率
  - 超过5%换手天数（主力活跃度指标）

数据源：东方财富历史K线接口
"""

import sys
import requests


def get_turnover(stock_code: str, days: int = 30) -> dict:
    """
    从东方财富获取个股历史换手率数据
    返回字段: 日期,开,收,高,低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
    """
    market = '1' if stock_code.startswith('6') else '0'
    url = (
        f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
        f"?secid={market}.{stock_code}"
        f"&fields1=f1,f2,f3,f4,f5,f6"
        f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
        f"&lmt={days}&klt=101&fqt=1&end=20260415"
    )
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://quote.eastmoney.com/'
    }
    r = requests.get(url, timeout=10, headers=headers)
    data = r.json()
    klines = data.get('data', {}).get('klines', [])

    total = 0.0
    high_days = 0
    daily = []
    for k in klines:
        f = k.split(',')
        try:
            turnover = float(f[10]) if len(f) > 10 and f[10] else 0.0
        except Exception:
            turnover = 0.0
        total += turnover
        if turnover > 5:
            high_days += 1
        daily.append({'date': f[0], 'close': f[2], 'turnover': turnover})

    # 活跃度判断
    if total > 100:
        activity = 'HIGHLY ACTIVE'
    elif total > 50:
        activity = 'Normal Activity'
    else:
        activity = 'Relatively Quiet'

    return {
        'code': stock_code,
        'days': len(klines),
        'total': round(total, 1),
        'high_days': high_days,
        'activity': activity,
        'daily': daily
    }


def print_report(result: dict):
    print(f"\n{'='*55}")
    print(f"  股票代码: {result['code']}  |  统计天数: {result['days']}")
    print(f"{'='*55}")
    print(f"  {'日期':<12} {'收盘价':>8}  {'换手率':>8}")
    print(f"  {'-'*12} {'-'*8}  {'-'*8}")
    for d in result['daily']:
        marker = ' ★' if d['turnover'] > 5 else ''
        print(f"  {d['date']:<12} {d['close']:>8}  {d['turnover']:>7.2f}%{marker}")
    print(f"{'='*55}")
    print(f"  30日累计换手率: {result['total']}%  |  {result['activity']}")
    print(f"  超5%换手天数:   {result['high_days']}天")
    print(f"{'='*55}\n")


if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else '603799'
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    result = get_turnover(code, days)
    print_report(result)
