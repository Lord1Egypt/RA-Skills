"""
南向资金（沪深港通港股通）净流入
需要 akshare: pip install akshare
"""
try:
    import akshare as ak
    import pandas as pd
except ImportError as e:
    print(f"需要安装akshare: pip install akshare ({e})")
    exit(1)

def get_southbound():
    print("\n=== 南向资金（港股通）===")
    try:
        # 沪深港通南向资金历史
        df = ak.stock_hsgt_north_net_flow_em()
        print(df.tail(5).to_string(index=False))
    except Exception as e:
        print(f"南向资金获取失败: {e}")
        print("\n尝试替代方案...")
        try:
            # 替代：东方财富南向资金
            url = "https://push2.eastmoney.com/api/qt/kamt.rtmin/get"
            params = {"fields1": "f1,f2,f3,f4", "fields2": "f51,f52,f53,f54,f55,f56"}
            r = requests.get(url, params=params, timeout=10)
            print(r.json())
        except Exception as e2:
            print(f"替代方案也失败: {e2}")

if __name__ == "__main__":
    get_southbound()
