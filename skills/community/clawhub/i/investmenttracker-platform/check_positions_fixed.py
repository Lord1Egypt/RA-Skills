#!/usr/bin/env python3
"""
使用真实API密钥检查持仓数据 - 修复SSE响应处理
"""

import json
import os
import sys
import subprocess
import time
from typing import Dict, Any, List, Optional

def parse_sse_response(response_text: str) -> Optional[Dict[str, Any]]:
    """解析SSE响应"""
    lines = response_text.strip().split('\n')
    data_line = None
    
    for line in lines:
        if line.startswith('data: '):
            data_line = line[6:]  # 移除 'data: ' 前缀
            break
    
    if not data_line:
        print(f"未找到data行，响应: {response_text[:200]}...")
        return None
    
    try:
        data = json.loads(data_line)
        
        # 检查是否有嵌套的JSON字符串
        if "result" in data and "content" in data["result"]:
            content = data["result"]["content"]
            if content and len(content) > 0 and "text" in content[0]:
                text_content = content[0]["text"]
                try:
                    # 尝试解析嵌套的JSON
                    nested_data = json.loads(text_content)
                    return {"result": nested_data}
                except json.JSONDecodeError:
                    # 如果不是JSON，直接返回文本
                    return {"result": {"text": text_content}}
        
        return data
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始data行: {data_line[:200]}")
        return None

def send_mcp_request(api_url: str, headers: Dict[str, str], method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """发送MCP请求"""
    # 构建JSON-RPC请求
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": int(time.time() * 1000)
    }
    
    # 构建curl命令
    header_args = []
    for key, value in headers.items():
        header_args.append(f"-H")
        header_args.append(f"{key}: {value}")
    
    cmd = [
        "curl", "-s", "-N", "-X", "POST",
        api_url,
        *header_args,
        "-d", json.dumps(request)
    ]
    
    print(f"发送请求到: {api_url}")
    
    try:
        # 执行curl命令
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"请求失败: {result.stderr}")
            return None
        
        # 解析SSE响应
        return parse_sse_response(result.stdout)
        
    except subprocess.TimeoutExpired:
        print("请求超时")
        return None
    except Exception as e:
        print(f"请求异常: {e}")
        return None

def get_positions(api_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """获取持仓列表"""
    return send_mcp_request(api_url, headers, "tools/call", {
        "name": "positions_list_v1",
        "arguments": {
            "status": "POSITION",
            "limit": 20
        }
    })

def get_user_info(api_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """获取用户信息"""
    return send_mcp_request(api_url, headers, "tools/call", {
        "name": "whoami_v1",
        "arguments": {}
    })

def format_positions(positions_data: Dict[str, Any]) -> str:
    """格式化持仓数据"""
    if not positions_data or "result" not in positions_data:
        return "持仓数据: 获取失败或数据为空"
    
    result = positions_data["result"]
    
    # 检查是否有items字段
    if isinstance(result, dict) and "items" in result:
        positions = result["items"]
    elif isinstance(result, list):
        positions = result
    else:
        return f"持仓数据格式未知: {type(result)}"
    
    output = []
    output.append("📊 持仓列表 (真实数据)")
    output.append("=" * 60)
    
    if not positions:
        output.append("暂无持仓")
    else:
        output.append(f"持仓数量: {len(positions)}")
        output.append("=" * 60)
        
        for i, pos in enumerate(positions, 1):
            # 尝试不同的字段名
            symbol = pos.get('symbol') or pos.get('code') or 'N/A'
            name = pos.get('name') or 'N/A'
            asset_type = pos.get('asset_type') or pos.get('type') or 'N/A'
            quantity = pos.get('quantity') or pos.get('amount') or 0
            current_price = pos.get('current_price') or pos.get('price') or 0
            current_value = pos.get('current_value') or pos.get('value') or 0
            cost_basis = pos.get('cost_basis') or pos.get('cost') or 0
            unrealized_gain = pos.get('unrealized_gain') or pos.get('gain') or 0
            status = pos.get('status') or 'N/A'
            
            output.append(f"{i}. {symbol} - {name}")
            output.append(f"   类型: {asset_type}")
            output.append(f"   数量: {quantity:,.4f}")
            output.append(f"   当前价格: ${current_price:,.2f}")
            output.append(f"   当前价值: ${current_value:,.2f}")
            output.append(f"   成本基础: ${cost_basis:,.2f}")
            output.append(f"   未实现收益: ${unrealized_gain:,.2f}")
            output.append(f"   状态: {status}")
            if i < len(positions):
                output.append("-" * 40)
    
    return "\n".join(output)

def format_user_info(user_data: Dict[str, Any]) -> str:
    """格式化用户信息"""
    if not user_data or "result" not in user_data:
        return "用户信息: 获取失败"
    
    result = user_data["result"]
    
    output = []
    output.append("👤 用户信息")
    output.append("-" * 40)
    
    if isinstance(result, dict):
        output.append(f"ID: {result.get('id', 'N/A')}")
        output.append(f"名称: {result.get('name', 'N/A')}")
        output.append(f"邮箱: {result.get('email', 'N/A')}")
        output.append(f"加入日期: {result.get('joined_date', 'N/A')}")
        output.append(f"投资风格: {result.get('investment_style', 'N/A')}")
        output.append(f"OpenID: {result.get('openid', 'N/A')}")
    else:
        output.append(f"数据格式: {type(result)}")
        output.append(f"内容: {str(result)[:100]}...")
    
    return "\n".join(output)

def main():
    """主函数"""
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), "real_config.json")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"配置文件不存在: {config_path}")
        return
    
    mcp_config = config.get("mcpServers", {}).get("investmenttracker", {})
    api_url = mcp_config.get("url", "")
    headers = mcp_config.get("headers", {})
    
    print("=" * 60)
    print("InvestmentTracker 真实数据查询")
    print(f"API URL: {api_url}")
    print("=" * 60)
    print()
    
    # 获取用户信息
    print("获取用户信息...")
    user_info = get_user_info(api_url, headers)
    if user_info:
        print(format_user_info(user_info))
    else:
        print("用户信息获取失败")
    print()
    
    # 获取持仓数据
    print("获取持仓数据...")
    positions = get_positions(api_url, headers)
    if positions:
        print(format_positions(positions))
        
        # 计算总价值
        result = positions.get("result", {})
        if isinstance(result, dict) and "items" in result:
            positions_list = result["items"]
        elif isinstance(result, list):
            positions_list = result
        else:
            positions_list = []
        
        if positions_list:
            total_value = sum(pos.get("current_value") or pos.get("value") or 0 for pos in positions_list)
            total_gain = sum(pos.get("unrealized_gain") or pos.get("gain") or 0 for pos in positions_list)
            print()
            print("📈 持仓汇总")
            print("-" * 40)
            print(f"持仓总价值: ${total_value:,.2f}")
            print(f"总未实现收益: ${total_gain:,.2f}")
            print(f"持仓数量: {len(positions_list)}")
    else:
        print("持仓数据获取失败")
    
    print()
    print("=" * 60)
    print("查询完成")

if __name__ == "__main__":
    main()