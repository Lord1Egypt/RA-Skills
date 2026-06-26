# -*- coding: utf-8 -*-
"""
配置管理器测试 - Linux版本
对应: scripts/config_manager.py
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from config_manager import ConfigManager, ConfigNotSetError

def test_config():
    """测试配置管理功能"""
    
    print("\n[测试1] 初始化配置管理器")
    config_mgr = ConfigManager()
    print(f"[OK] Skill路径: {config_mgr.skill_path}")
    
    print("\n[测试2] 加载配置")
    config = config_mgr.load_config()
    print(f"[OK] 配置版本: {config['metadata']['version']}")
    print(f"[OK] 配置描述: 快导(KD) Skill - 平台参数配置")
    
    print("\n[测试3] 获取平台配置 - 小红书")
    xhs_config = config_mgr.get_platform_config("xiaohongshu")
    print(f"[OK] 平台名称: {xhs_config['name']}")
    print(f"[OK] 用户画像: {xhs_config['user_profile']}")
    print(f"[OK] 内容风格: {xhs_config['content_style']}")
    print(f"[OK] 总时长: {xhs_config['duration']['total']}")
    print(f"[OK] 分镜时长: {xhs_config['duration']['segment']}")
    print(f"[OK] 分镜数量: {xhs_config['duration']['segments_count']}")
    
    print("\n[测试4] 计算分镜数量")
    segments = config_mgr.calculate_segments("xiaohongshu", "2-3min")
    print(f"[OK] 2-3分钟计算分镜数: {segments}")
    
    print("\n[测试5] 验证配置")
    validation = config_mgr.validate_config()
    print("[OK] 配置验证结果:")
    for key, value in validation.items():
        status = "[OK] 已设置" if value else "[X] 未设置"
        print(f"  - {key}: {status}")
    
    print("\n[测试6] 获取Excel路径（预期报错）")
    try:
        path = config_mgr.get_excel_path("xiaohongshu")
        print(f"[OK] Excel路径: {path}")
    except ConfigNotSetError as e:
        print(f"[OK] 正确捕获错误: 配置项未设置")
    
    print("\n[完成] 配置管理测试通过")

if __name__ == "__main__":
    test_config()
