#!/usr/bin/env python3
"""
InvestmentTracker 持仓数据获取脚本
直接调用MCP API获取完整的投资数据
"""

import json
import time
import subprocess

# MCP API配置
BASE_URL = 'https://investmenttracker-ingest-production.up.railway.app/mcp'
AUTH_TOKEN = 'it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes'

def call_mcp_tool(tool_name, arguments=None):
    """调用MCP工具"""
    request_data = {
        'jsonrpc': '2.0',
        'method': 'tools/call',
        'params': {
            'name': tool_name,
            'arguments': arguments or {}
        },
        'id': int(time.time() * 1000)
    }
    
    json_data = json.dumps(request_data)
    curl_cmd = [
        'curl', '-s', '-X', 'POST', BASE_URL,
        '-H', 'Authorization: Bearer ' + AUTH_TOKEN,
        '-H', 'Accept: application/json, text/event-stream',
        '-H', 'Content-Type: application/json',
        '-d', json_data
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('data: '):
                    try:
                        event_data = json.loads(line[6:])
                        if 'result' in event_data and 'content' in event_data['result']:
                            for content in event_data['result']['content']:
                                if content['type'] == 'text':
                                    return json.loads(content['text'])
                    except json.JSONDecodeError:
                        continue
        return None
    except Exception as e:
        print(f'调用{tool_name}失败: {e}')
        return None

def main():
    print('📊 InvestmentTracker 持仓分析报告')
    print('=' * 60)
    
    # 1. 获取用户信息
    print('👤 用户信息')
    print('-' * 30)
    user_info = call_mcp_tool('whoami_v1')
    if user_info:
        print(f'用户ID: {user_info.get("openid", "N/A")}')
    else:
        print('用户信息: 获取失败')
    print()
    
    # 2. 获取投资方法论
    print('📈 投资方法论')
    print('-' * 30)
    methodology = call_mcp_tool('methodology_get_v1')
    if methodology:
        print(f'投资策略: {methodology.get("strategy", "N/A")}')
        print(f'风险承受能力: {methodology.get("risk_tolerance", "N/A")}')
        print(f'投资期限: {methodology.get("time_horizon", "N/A")}')
        print(f'分散化: {methodology.get("diversification", "N/A")}')
        print(f'再平衡频率: {methodology.get("rebalance_frequency", "N/A")}')
    else:
        print('投资方法论: 获取失败')
    print()
    
    # 3. 获取统计数据
    print('📊 投资统计数据')
    print('-' * 30)
    stats = call_mcp_tool('stats_quick_v1')
    if stats:
        total_value = stats.get("total_value", 0)
        total_gain = stats.get("total_gain", 0)
        return_rate = stats.get("return_rate", 0)
        
        print(f'投资组合总价值: ${total_value:,.2f}')
        print(f'总收益: ${total_gain:,.2f}')
        print(f'收益率: {return_rate:.2f}%')
        print(f'活跃持仓: {stats.get("active_positions", 0)}')
        print(f'已平仓持仓: {stats.get("closed_positions", 0)}')
        print(f'胜率: {stats.get("win_rate", 0):.2f}%')
    else:
        print('统计数据: 获取失败')
    print()
    
    # 4. 获取持仓数据
    print('📈 当前持仓')
    print('-' * 30)
    positions = call_mcp_tool('positions_list_v1', {'status': 'POSITION', 'limit': 20})
    if positions and 'items' in positions:
        print(f'持仓数量: {len(positions["items"])}')
        print()
        
        total_quantity = 0
        for i, position in enumerate(positions['items'], 1):
            print(f'{i}. {position["code"]} - {position["name"]}')
            print(f'   持仓状态: {position["status"]}')
            print(f'   货币: {position["currency"]}')
            print(f'   数量: {position["quantity"]:,}')
            print(f'   买入日期: {position["buy_date"]}')
            print(f'   投资组合: {position["portfolio"]}')
            print(f'   最后更新: {position["source_updated_at"][:19]}')
            print()
            total_quantity += position['quantity']
        
        print(f'总持仓数量: {total_quantity:,}')
    else:
        print('持仓数据: 获取失败')
    print()
    
    print('=' * 60)
    print('📅 报告生成时间: 2026-02-17 04:00 UTC')
    print('🔗 数据来源: InvestmentTracker MCP API')
    print('=' * 60)

if __name__ == '__main__':
    main()