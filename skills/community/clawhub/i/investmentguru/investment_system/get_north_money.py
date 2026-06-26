#!/usr/bin/env python3
"""
北向资金数据获取脚本
Agent调用此脚本获取今日北向资金数据
"""
import tushare as ak
import sys
import json

TOKEN = 'b8ef516ff4abecadc1cdb55956458c3fed0378f8f85c30460f0d4500'

def get_north_money(date=None):
    """获取北向资金流向"""
    if date is None:
        date = sys.argv[1] if len(sys.argv) > 1 else '20250417'
    
    try:
        ak.set_token(TOKEN)
        pro = ak.pro_api()
        
        df = pro.moneyflow_hsgt(trade_date=date)
        if df is None or df.empty:
            return None
        
        row = df.iloc[0]
        data = {
            'date': str(row['trade_date']),
            'ggt_ss': round(float(row['ggt_ss']) / 1e4, 2),
            'ggt_sz': round(float(row['ggt_sz']) / 1e4, 2),
            'hgt': round(float(row['hgt']) / 1e4, 2),
            'sgt': round(float(row['sgt']) / 1e4, 2),
            'north_money': round(float(row['north_money']) / 1e4, 2),
            'south_money': round(float(row['south_money']) / 1e4, 2),
        }
        
        # 信号判断
        if data['north_money'] > 100:
            data['signal'] = '🔴 红色警报'
            data['signal_desc'] = '大幅流入'
        elif data['north_money'] > 50:
            data['signal'] = '🟠 橙色警报'
            data['signal_desc'] = '大量流入'
        elif data['north_money'] > 30:
            data['signal'] = '🟡 黄色警报'
            data['signal_desc'] = '流入'
        else:
            data['signal'] = '🟢 正常'
            data['signal_desc'] = '温和流入'
        
        return data
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    result = get_north_money()
    print(json.dumps(result, ensure_ascii=False, indent=2))