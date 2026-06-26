#!/usr/bin/env python3
"""
企业微信 AI Bot 自动配置脚本
自动将企业微信通道配置添加到 OpenClaw 配置文件中
"""

import json
import os
import sys

def load_config():
    """加载 OpenClaw 配置文件"""
    config_paths = [
        os.path.expanduser('~/.openclaw/openclaw.json'),
        os.path.expanduser('~/.openclaw/config.json'),
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f), path
    
    raise FileNotFoundError("未找到 OpenClaw 配置文件")

def save_config(config, path):
    """保存配置文件"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def setup_wecom(bot_id=None, secret=None, dm_policy='open'):
    """配置企业微信通道"""
    print("🔧 开始配置企业微信 AI Bot...")
    
    # 加载配置
    config, config_path = load_config()
    print(f"✅ 配置文件：{config_path}")
    
    # 获取用户输入
    if not bot_id:
        bot_id = input("请输入企业微信 Bot ID: ").strip()
    if not secret:
        secret = input("请输入企业微信 Secret: ").strip()
    
    if not bot_id or not secret:
        print("❌ Bot ID 和 Secret 不能为空！")
        sys.exit(1)
    
    # 配置企业微信通道
    if 'channels' not in config:
        config['channels'] = {}
    
    config['channels']['wecom'] = {
        'enabled': True,
        'botId': bot_id,
        'secret': secret,
        'model': config.get('model', ''),
        'dmPolicy': dm_policy
    }
    
    # 保存配置
    save_config(config, config_path)
    print(f"✅ 配置已保存到：{config_path}")
    
    # 提示重启
    print("\n" + "="*50)
    print("📋 下一步操作：")
    print("1. 重启 Gateway: openclaw gateway restart")
    print("2. 测试连接：在企业微信中给 Bot 发消息")
    print("3. 查看日志：tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep wecom")
    print("="*50)
    
    return True

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='企业微信 AI Bot 自动配置脚本')
    parser.add_argument('--bot-id', help='企业微信 Bot ID')
    parser.add_argument('--secret', help='企业微信 Secret')
    parser.add_argument('--dm-policy', default='open', choices=['open', 'pairing', 'allowlist', 'disabled'],
                       help='直接消息策略（默认：open）')
    
    args = parser.parse_args()
    
    try:
        setup_wecom(args.bot_id, args.secret, args.dm_policy)
    except KeyboardInterrupt:
        print("\n❌ 配置已取消")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 配置失败：{e}")
        sys.exit(1)
