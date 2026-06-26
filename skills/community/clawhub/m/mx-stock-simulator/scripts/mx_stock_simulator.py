#!/usr/bin/env python3
# mx_stock_simulator - 妙想模拟组合管理技能

import os
import sys
import json
import requests
from typing import Dict, Any

# 加载环境变量
MX_APIKEY = os.environ.get('MX_APIKEY')
MX_API_URL = os.environ.get('MX_API_URL', 'https://mkapi2.dfcfs.com/finskillshub')
OUTPUT_DIR = '/root/.openclaw/workspace/mx_data/output'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_request(endpoint: str, body: Dict[str, Any], output_prefix: str) -> None:
    """发送POST请求并保存结果"""
    full_url = f"{MX_API_URL}{endpoint}"
    headers = {
        'apikey': MX_APIKEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(full_url, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        
        output_path = os.path.join(OUTPUT_DIR, f"{output_prefix}_raw.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"请求完成，结果保存在 {output_path}")
    except Exception as e:
        print(f"网络请求失败: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("请提供查询意图，例如：python mx_stock_simulator.py 我的持仓")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    output_prefix = f"mx_stock_simulator_{query.replace(' ', '_')}"
    
    # 根据意图识别调用不同接口
    if any(word in query for word in ['持仓', '我的持仓', '持仓情况']):
        make_request('/api/claw/mockTrading/positions', {'moneyUnit': 1}, output_prefix)
    elif any(word in query for word in ['资金', '我的资金', '账户余额', '资金情况']):
        make_request('/api/claw/mockTrading/balance', {'moneyUnit': 1}, output_prefix)
    elif any(word in query for word in ['委托', '我的委托', '订单', '委托记录']):
        make_request('/api/claw/mockTrading/orders', {'fltOrderDrt': 0, 'fltOrderStatus': 0}, output_prefix)
    else:
        print("无法识别意图，请明确说明：持仓查询/资金查询/委托查询等")
        sys.exit(1)

if __name__ == '__main__':
    main()
