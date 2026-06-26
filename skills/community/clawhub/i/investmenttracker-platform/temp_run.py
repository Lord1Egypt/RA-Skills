#!/usr/bin/env python3
"""
临时运行InvestmentTracker技能使用真实API密钥
"""

import json
import os
import sys

# 首先备份原始config.json
original_config = None
config_path = os.path.join(os.path.dirname(__file__), "config.json")
backup_path = os.path.join(os.path.dirname(__file__), "config.json.backup")

try:
    # 备份原始配置
    with open(config_path, 'r') as f:
        original_config = f.read()
    
    # 创建新配置
    new_config = {
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
        },
        "features": {
            "portfolio_management": True,
            "transaction_history": True,
            "performance_analytics": True,
            "market_data": True,
            "price_alerts": False,
            "tax_reporting": False
        },
        "display": {
            "currency": "USD",
            "date_format": "YYYY-MM-DD",
            "number_format": "en-US",
            "theme": "light"
        },
        "notifications": {
            "daily_summary": False,
            "price_change_alerts": False,
            "portfolio_rebalancing": False,
            "market_news": False
        },
        "integrations": {
            "feishu": {
                "enabled": False,
                "webhook_url": ""
            },
            "telegram": {
                "enabled": False,
                "bot_token": "",
                "chat_id": ""
            }
        }
    }
    
    # 写入新配置
    with open(config_path, 'w') as f:
        json.dump(new_config, f, indent=2)
    
    print("✅ 配置文件已更新为使用真实API密钥")
    print(f"🔑 API密钥: it_live_IGWL2ZjlCHmxHCHMV_AFU87xz0CszLrJTCvfzs5gAjo")
    print(f"🌐 MCP URL: https://claw.investtracker.ai/mcp")
    print()
    
    # 运行技能
    print("=" * 60)
    print("运行InvestmentTracker技能...")
    print("=" * 60)
    
    import subprocess
    result = subprocess.run([sys.executable, "InvestmentTracker_skill.py", "all", "--mode", "api"], 
                          capture_output=True, text=True, timeout=30)
    
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
finally:
    # 恢复原始配置
    if original_config:
        with open(config_path, 'w') as f:
            f.write(original_config)
        print()
        print("✅ 配置文件已恢复为原始状态")