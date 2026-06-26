"""
掘金量化 v2.1.0 新增 API 测试
- fut_get_continuous_contracts: 查询连续合约对应真实合约
- last_tick: 查询已订阅的最新 Tick（多标的）
- current_price: 查询当前最新价
"""

import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ⚠️ 请先在掘金终端中复制你的 Token，替换下面这行
TOKEN = os.environ.get('GM_TOKEN', '') or ''
if not TOKEN:
    print('❌ 请先设置环境变量 GM_TOKEN 或直接修改脚本中的 TOKEN 变量')
    sys.exit(1)

set_token(TOKEN)
print(f'✅ Token 已设置')
print()


def test_fut_get_continuous_contracts():
    """测试 fut_get_continuous_contracts"""
    print('=' * 60)
    print('1️⃣ 测试 fut_get_continuous_contracts')
    print('=' * 60)

    test_cases = [
        ('CFFEX.IM', '中证1000主力连续', '2025-01-01', '2025-03-31'),
        ('CFFEX.IM99', '中证1000加权指数', '2025-01-01', '2025-03-31'),
    ]

    for csymbol, desc, start, end in test_cases:
        try:
            df = fut_get_continuous_contracts(csymbol, start_date=start, end_date=end)
            if df is not None and len(df) > 0:
                print(f'  ✅ [{desc}] {csymbol}')
                print(f'     返回 {len(df)} 条记录')
                print(f'     字段: {list(df.columns)[:6]}')
                print(f'     最新: {df.iloc[-1].to_dict()}')
            else:
                print(f'  ⚠️  [{desc}] {csymbol} → 返回空数据')
        except Exception as e:
            print(f'  ❌ [{desc}] {csymbol} → {e}')

    print()


def test_last_tick_and_current_price():
    """测试 last_tick 和 current_price"""
    print('=' * 60)
    print('2️⃣ 测试 last_tick 和 current_price')
    print('=' * 60)

    symbols = 'SHSE.600519,SZSE.000001'

    # 先订阅 tick（last_tick 需要）
    try:
        subscribe(symbols=symbols, frequency='tick')
        print(f'  ✅ subscribe tick 成功')
    except Exception as e:
        print(f'  ⚠️  subscribe tick 异常（非策略环境可忽略）: {e}')

    # --- last_tick ---
    try:
        data = last_tick(symbols=symbols, fields='symbol,price,open,high,low,volume,created_at')
        print(f'  ✅ last_tick 返回 {len(data)} 条')
        if data:
            for item in data:
                print(f'     {item["symbol"]}  price={item.get("price")}  created_at={item.get("created_at")}')
    except Exception as e:
        print(f'  ❌ last_tick → {e}')

    # --- current_price ---
    try:
        data = current_price(symbols=symbols)
        print(f'  ✅ current_price 返回 {len(data)} 条')
        if data:
            for item in data:
                print(f'     {item["symbol"]}  price={item.get("price")}  created_at={item.get("created_at")}')
    except Exception as e:
        print(f'  ❌ current_price → {e}')

    print()


def test_current_rate_limit_info():
    """验证 current() 调用（确认兼容性）"""
    print('=' * 60)
    print('3️⃣ current() 兼容性测试（验证调用正常）')
    print('=' * 60)

    try:
        data = current(symbols='SHSE.600519')
        if data:
            print(f'  ✅ current() 正常返回')
            print(f'     symbol={data[0].get("symbol")}  price={data[0].get("price")}')
    except Exception as e:
        print(f'  ❌ current() → {e}')

    print()


if __name__ == '__main__':
    test_fut_get_continuous_contracts()
    test_last_tick_and_current_price()
    test_current_rate_limit_info()
    print('=' * 60)
    print('🏁 全部测试完成')
