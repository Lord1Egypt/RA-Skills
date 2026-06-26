#!/usr/bin/env python3
"""
Tushare Pro 配置测试脚本

验证 token 是否有效，检查可用接口
"""

import sys
import os

framework_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, framework_dir)
os.chdir(framework_dir)

from data_fetcher.providers.tushare import check_tushare_permissions, fetch_tushare_quote, fetch_tushare_financials
from data_fetcher.config import load_config


def main():
    print("🔍 Tushare Pro 配置测试")
    print("="*50)
    
    config = load_config()
    token = config['api_keys']['tushare']['token']
    
    # 检查权限（直接测试日线行情）
    print("\n1️⃣  检查 Token 有效性...")
    try:
        import tushare as ts
        ts.set_token(token)
        pro = ts.pro_api()
        df = pro.daily(ts_code='000001.SZ', start_date='20260319', end_date='20260319')
        if df is not None and len(df) > 0:
            print(f"✅ Token 有效（日线行情可用）")
            print(f"   测试数据：平安银行 {df.iloc[0]['close']}元")
        else:
            print(f"⚠️  Token 有效但无数据返回")
    except Exception as e:
        print(f"❌ Token 无效或积分不足")
        print(f"   {e}")
        print(f"\n💡 提示：")
        print(f"   1. 访问 https://tushare.pro/user/token 获取 token")
        print(f"   2. 注册送 100 积分，可使用基础接口")
        print(f"   3. 每日签到可获取更多积分")
        return 1
    
    # 测试行情接口
    print("\n2️⃣  测试行情接口...")
    test_symbols = ['000001.SZ', '600519.SH']
    
    for symbol in test_symbols:
        try:
            quote = fetch_tushare_quote(symbol, config=config)
            print(f"✅ {symbol}: ¥{quote.price} ({quote.change_percent}%) [PE: {quote.pe}]")
        except Exception as e:
            print(f"⚠️  {symbol}: {e}")
    
    # 测试财报接口
    print("\n3️⃣  测试财报接口...")
    symbol = '000001.SZ'
    try:
        financials = fetch_tushare_financials(symbol, config=config)
        print(f"✅ {symbol} 财报（{financials.report_date}）:")
        print(f"   ROE: {financials.roe}%")
        print(f"   EPS: {financials.eps}元")
        print(f"   毛利率：{financials.gross_margin}%")
    except Exception as e:
        print(f"⚠️  财报获取失败：{e}")
        print(f"   可能需要更高级别积分")
    
    print("\n" + "="*50)
    print("✅ Tushare 配置测试完成")
    print("\n📝 下一步：")
    print("   1. 如果接口可用，已自动集成到数据获取层")
    print("   2. 如果部分接口不可用，会自动降级到免费数据源")
    print("   3. 每日签到可获取更多积分，解锁更多接口")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
