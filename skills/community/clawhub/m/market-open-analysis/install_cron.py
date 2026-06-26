#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_cron.py - 安装每日开盘分析定时任务

运行此脚本自动配置 cron 定时任务：
- 交易日 5:00 收集价格数据
- 交易日 5:30 分析并推送

包含交互式配置向导，引导用户配置 API Key 和推送渠道
"""

import os
import subprocess
import sys
import re

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SKILL_DIR, "main.py")
CONFIG_FILE = os.path.join(SKILL_DIR, "config.py")
COMMODITY_FILE = os.path.join(SKILL_DIR, "commodity_price.py")
PYTHON_BIN = "/usr/bin/python3"


def get_current_crontab():
    """获取当前 crontab 内容"""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return ""
    except Exception:
        return ""


def install_cron():
    """安装定时任务"""
    # 检查脚本是否存在
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ 脚本不存在：{MAIN_SCRIPT}")
        return False
    
    # 获取当前 crontab
    current_cron = get_current_crontab()
    
    # 检查是否已安装
    if "market-open-analysis" in current_cron or "market_open" in current_cron:
        print("⚠️ 检测到已有相关定时任务")
        print("是否覆盖？(y/n): ", end="")
        response = input().strip().lower()
        if response != "y":
            print("取消安装")
            return False
    
    # 构建新的 cron 条目
    cron_header = """# 每日开盘分析定时任务 (market-open-analysis)
# 交易日 5:00 收集价格数据，5:30 分析推送
"""
    
    cron_jobs = f"""
# 交易日早上 5:00 执行 - 收集价格数据
0 5 * * 1-5 {PYTHON_BIN} {MAIN_SCRIPT} --stage collect >> ~/openclaw/workspace/logs/market_open.log 2>&1

# 交易日早上 5:30 执行 - 分析并推送
30 5 * * 1-5 {PYTHON_BIN} {MAIN_SCRIPT} --stage analyze >> ~/openclaw/workspace/logs/market_open.log 2>&1
"""
    
    # 合并 crontab
    new_cron = current_cron.strip() + "\n" + cron_header + cron_jobs
    
    # 写入 crontab
    try:
        # 写入临时文件
        temp_file = "/tmp/cron_temp.txt"
        with open(temp_file, "w") as f:
            f.write(new_cron)
        
        # 安装 crontab
        result = subprocess.run(["crontab", temp_file], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 定时任务安装成功！")
            print("\n已添加的任务：")
            print("  - 交易日 5:00 收集价格数据")
            print("  - 交易日 5:30 分析并推送")
            print("\n查看任务：crontab -l")
            print("删除任务：crontab -r")
            
            # 清理临时文件
            os.remove(temp_file)
            return True
        else:
            print(f"❌ 安装失败：{result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ 安装异常：{e}")
        return False


def uninstall_cron():
    """卸载定时任务"""
    current_cron = get_current_crontab()
    
    if not current_cron:
        print("⚠️ 当前没有 crontab")
        return False
    
    # 过滤掉相关任务
    lines = current_cron.split("\n")
    new_lines = []
    skip_next = False
    
    for line in lines:
        if "market-open-analysis" in line or "market_open" in line:
            skip_next = True
            continue
        if skip_next and (line.startswith("#") or line.strip() == ""):
            skip_next = False
            continue
        if "收集价格数据" in line or "分析并推送" in line:
            continue
        new_lines.append(line)
    
    # 写入新的 crontab
    try:
        temp_file = "/tmp/cron_temp.txt"
        with open(temp_file, "w") as f:
            f.write("\n".join(new_lines))
        
        result = subprocess.run(["crontab", temp_file], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 定时任务已卸载")
            os.remove(temp_file)
            return True
        else:
            print(f"❌ 卸载失败：{result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ 卸载异常：{e}")
        return False


def show_status():
    """显示当前状态"""
    print("=" * 60)
    print("📋 每日开盘分析 - 定时任务状态")
    print("=" * 60)
    
    # 检查 cron 服务
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "cron"],
            capture_output=True, text=True
        )
        status = result.stdout.strip()
        if status == "active":
            print("✅ cron 服务：运行中")
        else:
            print(f"⚠️ cron 服务：{status}")
    except Exception:
        print("⚠️ 无法检查 cron 服务状态")
    
    # 显示当前任务
    print("\n当前定时任务：")
    current_cron = get_current_crontab()
    if current_cron:
        related = [line for line in current_cron.split("\n") 
                   if "market" in line.lower() or "收集" in line or "分析" in line]
        if related:
            for line in related:
                print(f"  {line}")
        else:
            print("  (无相关任务)")
    else:
        print("  (无 crontab)")
    
    print("\n" + "=" * 60)


def guide_config():
    """引导用户配置文件"""
    print("\n" + "=" * 60)
    print("🔑 API Key 配置向导")
    print("=" * 60)
    
    # 1. 配置商品价格 API
    print("\n【1/4】CommodityPriceAPI 配置")
    print("-" * 60)
    print("获取方式：访问 https://commoditypriceapi.com 注册并获取 API Key")
    print("免费套餐：每月 100 次调用（足够每日使用）")
    
    while True:
        api_key = input("\n请输入 CommodityPriceAPI Key: ").strip()
        if api_key and api_key != "YOUR_COMMODITY_PRICE_API_KEY_HERE":
            break
        print("❌ API Key 不能为空！")
    
    # 更新 commodity_price.py
    try:
        with open(COMMODITY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'API_KEY = "[^"]*"',
            f'API_KEY = "{api_key}"',
            content
        )
        with open(COMMODITY_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ CommodityPriceAPI Key 已保存")
    except Exception as e:
        print(f"❌ 保存失败：{e}")
        return False
    
    # 2. 配置新闻 API
    print("\n【2/4】东方财富妙想 API 配置")
    print("-" * 60)
    print("获取方式：联系东方财富妙想官方申请 API 访问权限")
    print("如暂无 Key，可先填写占位符，后续再配置")
    
    mx_key = input("请输入东方财富妙想 API Key (或按回车跳过): ").strip()
    if not mx_key:
        mx_key = "YOUR_MX_API_KEY_HERE"
        print("⚠️ 已设置占位符，请后续手动配置 config.py")
    
    # 3. 配置推送用户
    print("\n【3/4】推送用户配置")
    print("-" * 60)
    print("支持平台：飞书、Telegram、Discord、Slack、WhatsApp 等")
    print("\n用户 ID 格式示例：")
    print("  - 飞书：ou_xxxxxxxxxxxx")
    print("  - Telegram: username 或 user_id")
    print("  - Discord: user_id 或 channel_id")
    
    while True:
        target = input("\n请输入推送用户 ID: ").strip()
        if target and target != "YOUR_USER_ID_HERE":
            break
        print("❌ 用户 ID 不能为空！")
    
    # 4. 配置推送渠道
    print("\n【4/4】推送渠道配置")
    print("-" * 60)
    print("可用渠道：feishu, telegram, discord, slack, whatsapp")
    print("留空则使用 OpenClaw 默认渠道")
    
    channel = input("请输入推送渠道 (直接回车使用默认): ").strip().lower()
    if channel and channel not in ["feishu", "telegram", "discord", "slack", "whatsapp"]:
        print(f"⚠️ 未知渠道 '{channel}'，将使用默认渠道")
        channel = ""
    
    # 更新 config.py
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新 MX_API_KEY
        content = re.sub(
            r'MX_API_KEY = "[^"]*"',
            f'MX_API_KEY = "{mx_key}"',
            content
        )
        
        # 更新 DEFAULT_TARGET
        content = re.sub(
            r'DEFAULT_TARGET = "[^"]*"',
            f'DEFAULT_TARGET = "{target}"',
            content
        )
        
        # 更新 DEFAULT_CHANNEL
        if channel:
            content = re.sub(
                r'DEFAULT_CHANNEL = "[^"]*"',
                f'DEFAULT_CHANNEL = "{channel}"',
                content
            )
        else:
            content = re.sub(
                r'DEFAULT_CHANNEL = "[^"]*"',
                'DEFAULT_CHANNEL = ""',
                content
            )
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ 配置已保存到 config.py")
        
    except Exception as e:
        print(f"❌ 保存失败：{e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ API Key 配置完成！")
    print("=" * 60)
    print(f"\n配置摘要：")
    print(f"  - CommodityPriceAPI: {'✓ 已配置' if api_key != 'YOUR_COMMODITY_PRICE_API_KEY_HERE' else '✗ 未配置'}")
    print(f"  - 东方财富妙想：{'✓ 已配置' if mx_key != 'YOUR_MX_API_KEY_HERE' else '✗ 未配置 (使用占位符)'}")
    print(f"  - 推送用户：{target}")
    print(f"  - 推送渠道：{channel or '默认'}")
    
    return True


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "install":
            # 先引导配置
            if guide_config():
                install_cron()
        elif command == "uninstall":
            uninstall_cron()
        elif command == "status":
            show_status()
        elif command == "config":
            guide_config()
        else:
            print("用法：python3 install_cron.py [install|uninstall|status|config]")
    else:
        # 默认安装（带配置向导）
        print("=" * 60)
        print("🌅 每日开盘分析 - 安装向导")
        print("=" * 60)
        print("\n本向导将帮助您完成：")
        print("  1. 配置 API Key（商品价格 + 新闻资讯）")
        print("  2. 配置推送渠道和用户")
        print("  3. 安装定时任务（5:00 收集，5:30 推送）")
        print("\n预计耗时：2-3 分钟")
        print("\n是否继续？(y/n): ", end="")
        response = input().strip().lower()
        
        if response == "y":
            if guide_config():
                print("\n" + "=" * 60)
                print("📅 现在安装定时任务...")
                print("=" * 60)
                install_cron()
            else:
                print("\n❌ 配置失败，安装中止")
        else:
            print("取消安装")


if __name__ == "__main__":
    main()
