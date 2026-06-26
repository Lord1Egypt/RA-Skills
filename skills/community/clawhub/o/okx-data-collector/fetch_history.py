#!/usr/bin/env python3
"""
OKX 历史 K 线数据采集脚本
用于补全历史数据到本地或 COS

使用方法:
    python3 fetch_history.py --symbol BTC-USDT-SWAP --bar 1H --days 365
"""

import argparse
import requests
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

# OKX API 配置
BASE_URL = 'https://www.okx.com/api/v5/market/candles'
RATE_LIMIT_DELAY = 0.05  # 50ms 避免限流

# 周期对应的秒数
BAR_SECONDS = {
    '1m': 60,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1H': 3600,
    '2H': 7200,
    '4H': 14400,
    '6H': 21600,
    '12H': 43200,
    '1D': 86400,
    '1W': 604800,
    '1M': 2592000,
}


def get_candles(inst_id, bar, before=None, after=None, limit=100):
    """获取单批 K 线数据"""
    params = {
        'instId': inst_id,
        'bar': bar,
        'limit': str(limit),
    }
    
    if before:
        params['before'] = str(before)
    if after:
        params['after'] = str(after)
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == '0':
            return data.get('data', [])
        else:
            print(f"API 错误：{data.get('msg')}")
            return []
    except Exception as e:
        print(f"请求失败：{e}")
        return []


def fetch_history(inst_id, bar, days, output_dir=None):
    """
    获取指定天数的历史 K 线数据
    
    Args:
        inst_id: 品种 ID (如 BTC-USDT-SWAP)
        bar: 周期 (1m, 5m, 1H, 4H, 1D 等)
        days: 采集天数
        output_dir: 输出目录（可选）
    
    Returns:
        list: K 线数据列表
    """
    print(f"\n{'='*60}")
    print(f"开始采集：{inst_id} - {bar} - {days}天")
    print(f"{'='*60}")
    
    # 计算时间范围
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    
    print(f"时间范围：{start_time.strftime('%Y-%m-%d')} 至 {end_time.strftime('%Y-%m-%d')}")
    
    # 理论条数
    bar_seconds = BAR_SECONDS.get(bar, 60)
    theoretical_bars = days * 86400 // bar_seconds
    print(f"理论条数：约 {theoretical_bars:,} 条")
    
    # 开始采集
    all_candles = []
    current_before = None
    iterations = 0
    max_iterations = theoretical_bars // 100 + 10
    
    while iterations < max_iterations:
        iterations += 1
        
        # 获取数据
        candles = get_candles(inst_id, bar, before=current_before)
        
        if not candles:
            print("无更多数据")
            break
        
        all_candles.extend(candles)
        
        # 检查是否到达最早时间
        earliest_ts = int(candles[-1][0])
        earliest_date = datetime.fromtimestamp(earliest_ts / 1000)
        
        if earliest_date < start_time:
            # 过滤掉早于开始时间的数据
            all_candles = [c for c in all_candles if int(c[0]) >= start_time.timestamp() * 1000]
            print(f"已到达目标时间范围")
            break
        
        # 更新 before 参数
        current_before = earliest_ts - 1000
        
        # 进度显示
        if iterations % 10 == 0:
            progress = len(all_candles) / theoretical_bars * 100
            print(f"进度：{len(all_candles):,} / {theoretical_bars:,} 条 ({progress:.1f}%), 最早：{earliest_date.strftime('%Y-%m-%d')}")
        
        # 速率限制
        time.sleep(RATE_LIMIT_DELAY)
    
    # 结果统计
    print(f"\n{'='*60}")
    print(f"采集完成!")
    print(f"实际获取：{len(all_candles):,} 条")
    print(f"耗时：{iterations * RATE_LIMIT_DELAY:.1f} 秒")
    print(f"{'='*60}")
    
    # 保存数据
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存为 JSON
        output_file = output_path / f"{inst_id}_{bar}_{days}d.json"
        with open(output_file, 'w') as f:
            json.dump(all_candles, f, indent=2)
        print(f"已保存：{output_file}")
        
        # 保存为 CSV
        csv_file = output_path / f"{inst_id}_{bar}_{days}d.csv"
        with open(csv_file, 'w') as f:
            f.write("timestamp,open,high,low,close,volume\n")
            for c in reversed(all_candles):  # 按时间正序
                ts = datetime.fromtimestamp(int(c[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{ts},{c[1]},{c[2]},{c[3]},{c[4]},{c[5]}\n")
        print(f"已保存：{csv_file}")
    
    return all_candles


def parse_candle(candle):
    """解析单根 K 线"""
    return {
        'timestamp': datetime.fromtimestamp(int(candle[0]) / 1000),
        'open': float(candle[1]),
        'high': float(candle[2]),
        'low': float(candle[3]),
        'close': float(candle[4]),
        'volume': float(candle[5]),
    }


def main():
    parser = argparse.ArgumentParser(description='OKX 历史 K 线数据采集')
    parser.add_argument('--symbol', '-s', required=True, help='品种 ID (如 BTC-USDT-SWAP)')
    parser.add_argument('--bar', '-b', required=True, help='周期 (1m, 5m, 1H, 4H, 1D 等)')
    parser.add_argument('--days', '-d', type=int, default=365, help='采集天数')
    parser.add_argument('--output', '-o', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    fetch_history(args.symbol, args.bar, args.days, args.output)


if __name__ == '__main__':
    main()
