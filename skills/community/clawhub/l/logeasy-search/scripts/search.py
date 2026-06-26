#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志易日志搜索工具
用于 OpenClaw 集成
"""
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse

# 配置
LOGEASE_URL = os.environ.get('LOGEASE_URL', 'http://10.20.51.16')
LOGEASE_USERNAME = os.environ.get('LOGEASE_USERNAME', 'admin')
LOGEASE_PASSWORD = os.environ.get('LOGEASE_PASSWORD', 'MIma@sec2025')


def search_logs(query='*', time_range='-1h,now', limit=10):
    """搜索日志"""
    params = {
        'query': query,
        'time_range': time_range,
        'limit': limit
    }
    
    try:
        r = requests.get(
            LOGEASE_URL + '/api/v3/search/sheets/',
            params=params,
            auth=HTTPBasicAuth(LOGEASE_USERNAME, LOGEASE_PASSWORD),
            timeout=30
        )
        
        data = r.json()
        
        if data.get('rc') == 0:
            results = data.get('results', {})
            total_hits = results.get('total_hits', 0)
            rows = results.get('sheets', {}).get('rows', [])
            
            return {
                'success': True,
                'total_hits': total_hits,
                'count': len(rows),
                'rows': rows
            }
        else:
            return {
                'success': False,
                'error': data.get('error', 'Unknown error')
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def format_results(results):
    """格式化输出"""
    if not results['success']:
        return f"搜索失败: {results['error']}"
    
    output = []
    output.append(f"总命中: {results['total_hits']}")
    output.append(f"返回: {results['count']} 条")
    output.append("")
    
    for i, row in enumerate(results['rows'][:10], 1):
        # 提取关键字段
        timestamp = row.get('agent_send_timestamp', '')
        raw_msg = row.get('raw_message', '')
        
        # 格式化时间
        if timestamp:
            try:
                import datetime
                dt = datetime.datetime.fromtimestamp(timestamp/1000)
                timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp_str = str(timestamp)
        else:
            timestamp_str = ''
        
        # 截断消息
        if raw_msg and len(raw_msg) > 150:
            raw_msg = raw_msg[:150] + '...'
        
        output.append(f"{i}. [{timestamp_str}] {raw_msg}")
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='日志易日志搜索')
    parser.add_argument('query', nargs='?', default='*', help='搜索语句')
    parser.add_argument('time_range', nargs='?', default='-1h,now', help='时间范围')
    parser.add_argument('limit', nargs='?', type=int, default=10, help='返回数量')
    
    args = parser.parse_args()
    
    results = search_logs(args.query, args.time_range, args.limit)
    print(format_results(results))


if __name__ == '__main__':
    main()
