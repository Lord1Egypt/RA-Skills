#!/usr/bin/env python3
"""
测试修复后的InvestmentTracker技能
"""

import json
import os
import sys
import tempfile

# 创建临时配置文件
temp_config = {
    "mcpServers": {
        "investmenttracker": {
            "url": "https://claw.investtracker.ai/mcp",
            "headers": {
                "Authorization": "Bearer it_live_IGWL2ZjlCHmxHCHMV_AFU87xz0CszLrJTCvfzs5gAjo",
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json"
            },
            "timeout": 30,
            "retry_attempts": 3,
            "cache_enabled": True,
            "cache_ttl": 300
        }
    }
}

# 创建临时文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(temp_config, f, indent=2)
    temp_config_path = f.name

print(f"临时配置文件: {temp_config_path}")
print("=" * 60)

try:
    # 导入技能
    sys.path.insert(0, os.path.dirname(__file__))
    
    # 动态修改技能以使用临时配置
    import InvestmentTracker_skill as skill_module
    
    # 保存原始配置路径逻辑
    original_load_config = skill_module.InvestmentTrackerSkill._load_config
    
    def patched_load_config(self):
        """使用临时配置文件的补丁方法"""
        print(f"使用临时配置文件: {temp_config_path}")
        try:
            with open(temp_config_path, 'r') as f:
                config = json.load(f)
                print(f"临时配置文件加载成功")
                return config
        except FileNotFoundError:
            print(f"临时配置文件不存在，使用原始方法")
            return original_load_config(self)
    
    # 应用补丁
    skill_module.InvestmentTrackerSkill._load_config = patched_load_config
    
    # 创建技能实例
    print("创建InvestmentTrackerSkill实例...")
    from InvestmentTracker_skill import InvestmentTrackerSkill, ConnectionMode
    
    skill = InvestmentTrackerSkill(mode=ConnectionMode.API)
    
    print("=" * 60)
    print("测试用户信息获取...")
    print("=" * 60)
    
    user_info = skill.get_user_info()
    print(f"用户信息结果: {user_info.get('source', 'unknown')}")
    
    if user_info.get("source") == "api" and user_info.get("data"):
        data = user_info["data"]
        print(f"👤 用户信息:")
        print(f"  ID: {data.get('id', 'N/A')}")
        print(f"  名称: {data.get('name', 'N/A')}")
        print(f"  邮箱: {data.get('email', 'N/A')}")
        print(f"  OpenID: {data.get('openid', 'N/A')}")
    elif user_info.get("source") == "api_error":
        print("❌ API错误: 无法获取用户信息")
    else:
        print(f"⚠️ 使用模拟数据或未知状态")
    
    print()
    print("=" * 60)
    print("测试持仓数据获取...")
    print("=" * 60)
    
    positions = skill.list_positions(status="POSITION", limit=10)
    print(f"持仓结果: {positions.get('source', 'unknown')}")
    
    if positions.get("source") == "api" and positions.get("data"):
        data = positions["data"]
        items = data.get("items", []) if isinstance(data, dict) else data
        
        if items:
            print(f"📊 找到 {len(items)} 个持仓:")
            print("-" * 60)
            
            for i, pos in enumerate(items, 1):
                # 尝试不同的字段名
                symbol = pos.get('symbol') or pos.get('code') or 'N/A'
                name = pos.get('name') or 'N/A'
                quantity = pos.get('quantity') or pos.get('amount') or 0
                current_value = pos.get('current_value') or pos.get('value') or 0
                
                print(f"{i}. {symbol} - {name}")
                print(f"   数量: {quantity:,.4f}")
                print(f"   当前价值: ${current_value:,.2f}")
                
                if i < len(items):
                    print()
        else:
            print("📭 暂无持仓")
    elif positions.get("source") == "api_error":
        print("❌ API错误: 无法获取持仓数据")
    else:
        print(f"⚠️ 使用模拟数据或未知状态")
    
    print()
    print("=" * 60)
    print("测试完成")
    
finally:
    # 清理临时文件
    if os.path.exists(temp_config_path):
        os.remove(temp_config_path)
        print(f"已清理临时配置文件")