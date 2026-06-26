#!/usr/bin/env python3
"""
ClawHub技能发布脚本
基于API文档: https://github.com/openclaw/clawhub/blob/main/docs/http-api.md
"""

import requests
import json
import os
from pathlib import Path

# 配置
API_TOKEN = "clh_kZ-UWsDcsn7OiMG67RJxp3O1fdx43c41WgHMe01KWeY"
API_BASE = "https://clawhub.ai/api/v1"
SKILL_SLUG = "papermc-ai-ops"  # 现有技能slug
ZIP_FILE = "papermc-ai-ops-v2.0.0.zip"

def publish_skill():
    """发布技能到ClawHub"""
    print(f"发布技能: {SKILL_SLUG}")
    print(f"API端点: {API_BASE}/skills/{SKILL_SLUG}")
    
    # 检查文件是否存在
    if not os.path.exists(ZIP_FILE):
        print(f"错误: 文件 {ZIP_FILE} 不存在")
        return False
    
    # 准备multipart/form-data
    files = {
        'files': (ZIP_FILE, open(ZIP_FILE, 'rb'), 'application/zip')
    }
    
    # 准备payload
    payload = {
        'payload': json.dumps({
            'slug': SKILL_SLUG,
            'version': '2.0.0',
            'changelog': 'Release v2.0.0: Enhanced with Plugin Upgrade Framework\n\n- Added plugin_upgrade_framework.py based on ViaVersion 5.7.2→5.8.0 experience\n- Added upgrade_examples.py with 4 usage examples\n- Added viaversion_upgrade_report.json documenting the upgrade experience\n- Added Turret_Plugin_User_Manual.md complete plugin guide\n- Updated SKILL.md from v1.0.0 to v2.0.0\n- Enhanced risk assessment and batch upgrade planning\n- Validated by successful ViaVersion upgrade (2026-03-28)'
        })
    }
    
    # 设置headers
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    
    try:
        print("正在上传技能...")
        response = requests.post(
            f"{API_BASE}/skills/{SKILL_SLUG}",
            headers=headers,
            data=payload,
            files=files,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 技能发布成功!")
            result = response.json()
            print(f"版本: {result.get('version', 'unknown')}")
            print(f"创建时间: {result.get('createdAt', 'unknown')}")
            return True
        else:
            print(f"❌ 技能发布失败: {response.status_code}")
            if response.status_code == 401:
                print("错误: 认证失败，请检查API token")
            elif response.status_code == 403:
                print("错误: 权限不足，请确认你是技能所有者")
            elif response.status_code == 404:
                print("错误: 技能不存在，请确认slug正确")
            elif response.status_code == 429:
                print("错误: 请求过于频繁，请稍后重试")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_api_connection():
    """测试API连接"""
    print("测试API连接...")
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    
    try:
        response = requests.get(
            f"{API_BASE}/whoami",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ API连接成功")
            print(f"用户: {user_info.get('handle', 'unknown')}")
            print(f"显示名: {user_info.get('displayName', 'unknown')}")
            return True
        else:
            print(f"❌ API连接失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("ClawHub技能发布工具")
    print("=" * 60)
    
    # 测试连接
    if not test_api_connection():
        print("无法连接到ClawHub API，请检查网络和token")
        return
    
    print("\n" + "=" * 60)
    
    # 确认发布
    confirm = input(f"确认发布 {SKILL_SLUG} v2.0.0 到 ClawHub? (y/N): ")
    if confirm.lower() != 'y':
        print("发布取消")
        return
    
    # 执行发布
    print("\n开始发布...")
    success = publish_skill()
    
    if success:
        print("\n" + "=" * 60)
        print("发布完成!")
        print(f"技能地址: https://clawhub.ai/skills/{SKILL_SLUG}")
        print(f"GitHub地址: https://github.com/yanxi1024-git/PaperMC-Ai-Agent/tree/v2.0.0")
    else:
        print("\n发布失败，请检查错误信息")

if __name__ == "__main__":
    main()