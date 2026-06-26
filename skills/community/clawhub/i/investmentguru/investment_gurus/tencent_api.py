#!/usr/bin/env python3
"""
腾讯财经API - 获取实时股票数据 V2
使用实时行情接口
"""
import requests
import json
from typing import Dict, Optional


# 股票代码映射 (腾讯财经格式)
STOCK_CODE_MAP = {
    "腾讯": "hk00700",
    "阿里": "hk09988",
    "阿里巴巴": "hk09988",
    "美团": "hk03690",
    "京东": "hk09618",
    "小米": "hk01810",
    "网易": "hk09999",
    "百度": "hk09888",
    "快手": "hk01024",
    "携程": "hk09961",
    "海底捞": "hk06862",
    "泡泡玛特": "hk09992",
    "中芯国际": "hk00981",
    "金山云": "hk03896",
}


def get_stock_realtime(code: str) -> Optional[Dict]:
    """
    获取实时股票数据
    
    Args:
        code: 腾讯财经格式的代码 (如 hk00700)
    
    Returns:
        dict: 股票数据
    """
    # 尝试使用实时接口
    url = "https://web.ifzq.gtimg.cn/appstock/app/getquote_redis"
    params = {'_var': 'quote', 'param': code}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        text = response.text
        
        if '=' in text:
            data = json.loads(text.split('=')[1])
            
            if code in data.get('data', {}):
                quote = data['data'][code]
                if 'qt' in quote:
                    qt = quote['qt'][code]
                    
                    # 解析数据
                    # [0] = 名称, [1] = 代码, [2] = 当前价, [3] = 涨跌, [4] = 涨跌%
                    # [5] = 成交量, [6] = 成交额, [7] = 振幅, [8] = 最高
                    # [9] = 最低, [10] = 今开, [11] = 昨收
                    
                    return {
                        'code': code,
                        'name': qt[0],
                        'price': float(qt[2]) if qt[2] not in ('0', '-', '') else None,
                        'change': float(qt[3]) if qt[3] not in ('0', '-', '') else 0,
                        'change_pct': float(qt[4]) if qt[4] not in ('0', '-', '') else 0,
                        'volume': float(qt[5]) if qt[5] not in ('0', '-', '') else 0,
                        'amount': float(qt[6]) if qt[6] not in ('0', '-', '') else 0,
                        'amplitude': float(qt[7]) if len(qt) > 7 and qt[7] not in ('0', '-', '') else 0,
                        'high': float(qt[8]) if len(qt) > 8 and qt[8] not in ('0', '-', '') else None,
                        'low': float(qt[9]) if len(qt) > 9 and qt[9] not in ('0', '-', '') else None,
                        'open': float(qt[10]) if len(qt) > 10 and qt[10] not in ('0', '-', '') else None,
                        'prev_close': float(qt[11]) if len(qt) > 11 and qt[11] not in ('0', '-', '') else None,
                    }
    
    except Exception as e:
        print(f"实时接口失败: {e}")
    
    # 备用：使用K线接口
    return get_stock_from_kline(code)


def get_stock_from_kline(code: str) -> Optional[Dict]:
    """从K线数据获取"""
    url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    params = {'_var': 'kline_dayqfq', 'param': f'{code},day,,,1,qfq'}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        text = response.text
        
        if '=' in text:
            data = json.loads(text.split('=')[1])
            
            if code in data.get('data', {}):
                stock_data = data['data'][code]
                qt = stock_data.get('qt', {}).get(code, [])
                
                if len(qt) > 10:
                    return {
                        'code': code,
                        'name': qt[1] if len(qt) > 1 else code,
                        'prev_close': float(qt[3]) if qt[3] not in ('0', '') else None,
                        'high': float(qt[4]) if len(qt) > 4 and qt[4] not in ('0', '') else None,
                        'low': float(qt[5]) if len(qt) > 5 and qt[5] not in ('0', '') else None,
                        'price': float(qt[9]) if len(qt) > 9 and qt[9] not in ('0', '') else None,
                        'change': float(qt[31]) if len(qt) > 31 and qt[31] not in ('0', '') else 0,
                        'change_pct': float(qt[32]) if len(qt) > 32 and qt[32] not in ('0', '') else 0,
                        'amount': float(qt[37]) if len(qt) > 37 and qt[37] not in ('0', '') else 0,
                        'volume': float(qt[6]) if len(qt) > 6 and qt[6] not in ('0', '') else 0,
                    }
    
    except Exception as e:
        print(f"K线接口失败: {e}")
    
    return None


def get_stock_quote(stock_name: str) -> Optional[Dict]:
    """根据股票名称获取实时报价"""
    code = STOCK_CODE_MAP.get(stock_name)
    if not code:
        return None
    
    return get_stock_realtime(code)


# 测试
if __name__ == "__main__":
    print("测试腾讯财经实时API...")
    
    stocks = ["腾讯", "阿里", "中芯国际", "小米"]
    
    for name in stocks:
        data = get_stock_quote(name)
        if data:
            print(f"\n{name}:")
            print(f"  价格: {data.get('price')} 港元")
            print(f"  涨跌: {data.get('change')} ({data.get('change_pct')}%)")
            print(f"  昨收: {data.get('prev_close')}")
            print(f"  最高: {data.get('high')}, 最低: {data.get('low')}")
        else:
            print(f"\n{name}: 获取失败")