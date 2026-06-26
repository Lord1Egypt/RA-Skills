#!/usr/bin/env python3
"""
简化版数据获取脚本

直接使用 requests 获取数据，绕过 data_fetcher 模块

用法：
    python3 workflows/scripts/simple-data-fetcher.py
"""

import requests
import re
from datetime import datetime


def get_tencent_quote(symbol):
    """
    直接从腾讯 API 获取个股行情
    
    Args:
        symbol: 股票代码（如：600519.SH）
    
    Returns:
        dict: 行情数据
    """
    # 转换股票代码
    if '.SH' in symbol:
        code = symbol.replace('.SH', '')
        tencent_code = f'sh{code}'
    elif '.SZ' in symbol:
        code = symbol.replace('.SZ', '')
        tencent_code = f'sz{code}'
    else:
        tencent_code = symbol
    
    url = f"http://qt.gtimg.cn/q={tencent_code}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # 解析数据
        text = response.content.decode('gbk')
        pattern = r'v_(.*?)="(.*?)"'
        matches = re.findall(pattern, text)
        
        if not matches:
            return None
        
        for code, data in matches:
            fields = data.split('~')
            
            if len(fields) < 12:
                continue
            
            # 修复涨跌幅解析（腾讯格式：字段 4=涨跌额，字段 5=涨跌幅%，但可能是百分比格式）
            price = float(fields[3]) if fields[3] else 0.0
            prev_close = float(fields[11]) if fields[11] else 0.0
            change = float(fields[4]) if fields[4] else 0.0
            
            # 重新计算涨跌幅（避免解析错误）
            if prev_close > 0:
                change_percent = (change / prev_close) * 100
            else:
                change_percent = 0.0
            
            return {
                'symbol': symbol,
                'name': fields[1],
                'price': price,
                'change': change,
                'change_percent': round(change_percent, 2),
                'volume': int(float(fields[6])) if fields[6] else 0,
                'turnover': float(fields[7]) if fields[7] else 0.0,
                'high': float(fields[8]) if fields[8] else 0.0,
                'low': float(fields[9]) if fields[9] else 0.0,
                'open': float(fields[10]) if fields[10] else 0.0,
                'prev_close': float(fields[11]) if fields[11] else 0.0,
                'source': 'tencent',
                'timestamp': datetime.now().isoformat(),
            }
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None


def get_sina_index(symbol):
    """
    从新浪 API 获取大盘指数
    
    Args:
        symbol: 指数代码（如：sh000001）
    
    Returns:
        dict: 指数数据
    """
    url = f"http://hq.sinajs.cn/list={symbol}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        text = response.content.decode('gbk')
        
        # 解析：var hq_str_sh000001="上证指数，4006.55，..."
        if ',' in text:
            parts = text.split(',')
            if len(parts) >= 3:
                name = parts[0].split('=')[1].strip('"')
                price = float(parts[1].strip('"'))
                prev_close = float(parts[2].strip('"'))
                
                # 获取其他数据
                open_price = float(parts[3]) if len(parts) > 3 else 0.0
                high = float(parts[4]) if len(parts) > 4 else 0.0
                low = float(parts[5]) if len(parts) > 5 else 0.0
                
                change = price - prev_close
                change_percent = (change / prev_close * 100) if prev_close else 0.0
                
                return {
                    'symbol': symbol,
                    'name': name,
                    'price': price,
                    'change': change,
                    'change_percent': round(change_percent, 2),
                    'open': open_price,
                    'high': high,
                    'low': low,
                    'prev_close': prev_close,
                    'source': 'sina',
                    'timestamp': datetime.now().isoformat(),
                }
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None


def main():
    """主函数"""
    print("📊 简化版数据获取测试")
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试个股
    print("测试个股数据（腾讯 API）：")
    print("-" * 50)
    
    test_stocks = ['600519.SH', '000001.SZ', '300750.SZ']
    
    for symbol in test_stocks:
        data = get_tencent_quote(symbol)
        if data:
            print(f"✅ {symbol} {data.get('name', '')}: ¥{data['price']} ({data['change_percent']}%)")
        else:
            print(f"❌ {symbol}: 获取失败")
    
    print()
    
    # 测试指数
    print("测试大盘指数（新浪 API）：")
    print("-" * 50)
    
    test_indices = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
    ]
    
    for symbol, name in test_indices:
        data = get_sina_index(symbol)
        if data:
            print(f"✅ {name}: {data['price']} ({data['change_percent']}%)")
        else:
            print(f"❌ {name}: 获取失败")
    
    print()
    print("=" * 50)
    print("✅ 测试完成！")


if __name__ == '__main__':
    main()
