#!/usr/bin/env python3
"""
检查 PaperMC 最新稳定版本
"""

import json
import subprocess
import sys
from datetime import datetime

def get_current_version():
    """获取当前服务器版本"""
    try:
        # 从服务器目录读取版本信息
        with open("/home/yan/projects/P_3.10.12/paperMC_RGFV_1.21.8/paper-version.txt", "r") as f:
            version_line = f.readline().strip()
            # 格式: Paper version git-Paper-1.21.10-117 (MC: 1.21.10)
            if "Paper-" in version_line:
                parts = version_line.split("Paper-")
                if len(parts) > 1:
                    version_part = parts[1].split(" ")[0]
                    return version_part
    except Exception as e:
        print(f"读取当前版本失败: {e}")
    
    # 备用方法：检查jar文件名
    import os
    for file in os.listdir("/home/yan/projects/P_3.10.12/paperMC_RGFV_1.21.8"):
        if file.startswith("paper-") and file.endswith(".jar"):
            version = file.replace("paper-", "").replace(".jar", "")
            return version
    
    return "1.21.10-117"  # 默认值

def get_all_versions():
    """获取所有可用版本"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'https://api.papermc.io/v2/projects/paper'],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        return data['versions']
    except Exception as e:
        print(f"获取版本列表失败: {e}")
        return []

def get_latest_stable_build(version):
    """获取指定版本的最新稳定版build"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://api.papermc.io/v2/projects/paper/versions/{version}/builds'],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        
        # 查找稳定版 (channel: "default")
        stable_builds = []
        for build in data['builds']:
            if build.get('channel') == 'default':
                stable_builds.append(build)
        
        if stable_builds:
            # 按build号排序，取最新
            stable_builds.sort(key=lambda x: x['build'], reverse=True)
            return stable_builds[0]
        else:
            return None
    except Exception as e:
        print(f"获取{version}的build信息失败: {e}")
        return None

def parse_version(version_str):
    """解析版本字符串，返回主版本和build号"""
    # 格式: 1.21.10-117
    if '-' in version_str:
        main_version, build = version_str.split('-')
        return main_version, int(build)
    else:
        return version_str, 0

def main():
    print("📋 PaperMC 最新稳定版本检查")
    print("=" * 50)
    
    # 获取当前版本
    current_full = get_current_version()
    current_main, current_build = parse_version(current_full)
    print(f"当前版本: {current_full}")
    print(f"解析结果: 版本={current_main}, build={current_build}")
    print()
    
    # 获取所有版本
    print("🔍 检查所有可用版本...")
    all_versions = get_all_versions()
    
    # 提取主版本号 (1.21.x)
    main_versions = []
    for v in all_versions:
        if v.startswith("1.21."):
            main_versions.append(v)
    
    # 按版本号排序（处理预发布版本）
    def version_key(v):
        # 移除预发布标识进行排序
        clean_v = v.split('-')[0]  # 移除 -preX, -rcX 等
        parts = clean_v.split('.')
        # 确保每个部分都是数字
        numeric_parts = []
        for part in parts:
            if part.isdigit():
                numeric_parts.append(int(part))
            else:
                numeric_parts.append(0)
        return numeric_parts
    
    main_versions.sort(key=version_key)
    
    print(f"找到 {len(main_versions)} 个 1.21.x 版本:")
    for v in main_versions[-5:]:  # 显示最后5个
        print(f"  • {v}")
    
    # 获取最新版本
    latest_version = main_versions[-1] if main_versions else current_main
    print(f"\n📊 最新版本: {latest_version}")
    
    # 检查当前版本是否最新
    if latest_version == current_main:
        print("✅ 当前使用最新主版本")
        
        # 检查build更新
        latest_build_info = get_latest_stable_build(current_main)
        if latest_build_info:
            latest_build = latest_build_info['build']
            latest_time = latest_build_info['time']
            
            print(f"最新稳定版build: {latest_build} ({latest_time})")
            
            if latest_build > current_build:
                print(f"⚠️ 有可用更新! 落后 {latest_build - current_build} 个build")
                
                # 显示更新内容摘要
                print("\n📝 更新内容摘要:")
                changes = latest_build_info.get('changes', [])
                security_fixes = 0
                for change in changes:
                    summary = change.get('summary', '')
                    if any(keyword in summary.lower() for keyword in ['fix', 'security', 'crash', 'prevent']):
                        security_fixes += 1
                        print(f"  • 🔒 {summary}")
                    else:
                        print(f"  • 📦 {summary}")
                
                if security_fixes > 0:
                    print(f"\n⚠️ 包含 {security_fixes} 个安全修复")
            else:
                print("✅ 已是最新稳定版")
        else:
            print("❌ 无法获取最新build信息")
    
    else:
        print(f"⚠️ 版本落后! 当前: {current_main}, 最新: {latest_version}")
        
        # 检查最新版本的稳定版
        latest_build_info = get_latest_stable_build(latest_version)
        if latest_build_info:
            latest_build = latest_build_info['build']
            latest_time = latest_build_info['time']
            
            print(f"最新版本稳定版: {latest_version}-{latest_build} ({latest_time})")
            
            # 建议
            print("\n🎯 建议:")
            print(f"1. 考虑升级到 {latest_version}")
            print(f"2. 先备份当前服务器")
            print(f"3. 使用 update_paper.py 脚本进行安全更新")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()