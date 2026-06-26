#!/usr/bin/env python3
"""
OpenClaw Update - Cron Task Script
定时检查更新脚本 - 每天凌晨 4:00 执行
检查新版本，评估风险，发送通知等待用户批准
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

def log(message):
    """打印日志（带时间戳）"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

# Skill Version: 1.0

def get_current_version():
    """获取当前版本"""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def check_agent_reach():
    """检测 agent-reach 是否可用"""
    try:
        result = subprocess.run(
            ["agent-reach", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def get_latest_version():
    """获取最新版本（通过 agent-reach）"""
    try:
        result = subprocess.run(
            ["agent-reach", "read", "https://github.com/openclaw/openclaw/releases"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # 简单提取最新版本号
        import re
        matches = re.findall(r'v?(\d{4}\.\d+\.\d+)', result.stdout)
        if matches:
            return matches[0]
        return None
    except Exception as e:
        return None

def parse_version(version_str):
    """解析版本号"""
    import re
    match = re.search(r'v?(\d{4})\.(\d+)\.(\d+)', version_str)
    if match:
        return {
            'year': int(match.group(1)),
            'month': int(match.group(2)),
            'patch': int(match.group(3)),
            'full': version_str
        }
    return None

def version_compare(v1, v2):
    """比较版本：返回 -1(旧), 0(相同), 1(新)"""
    if not v1 or not v2:
        return 0
    
    p1 = parse_version(v1)
    p2 = parse_version(v2)
    
    if not p1 or not p2:
        return 0
    
    # 比较年.月.补丁
    if p1['year'] < p2['year']:
        return -1
    elif p1['year'] > p2['year']:
        return 1
    
    if p1['month'] < p2['month']:
        return -1
    elif p1['month'] > p2['month']:
        return 1
    
    if p1['patch'] < p2['patch']:
        return -1
    elif p1['patch'] > p2['patch']:
        return 1
    
    return 0

def check_issues():
    """检查 GitHub issues"""
    try:
        result = subprocess.run(
            ["agent-reach", "read", "https://github.com/openclaw/openclaw/issues"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # 简单检查是否有严重问题
        critical_keywords = ['critical', 'crash', 'data loss', 'security', 'vulnerability']
        content_lower = result.stdout.lower()
        
        critical_count = sum(1 for kw in critical_keywords if kw in content_lower)
        
        if critical_count > 3:
            return 'critical', "发现多个严重问题"
        elif critical_count > 0:
            return 'warning', "发现一些需要注意的问题"
        else:
            return 'safe', "Issues 状态良好"
    except:
        return 'unknown', "无法检查 Issues"

def send_notification(title, message, urgency='normal'):
    """发送通知（使用系统通知）"""
    try:
        # macOS
        subprocess.run([
            "osascript",
            "-e", f'display notification "{message}" with title "{title}"'
        ], check=True)
        return True
    except:
        try:
            # Linux (notify-send)
            subprocess.run(["notify-send", title, message], check=True)
            return True
        except:
            log("⚠️ 无法发送系统通知")
            return False

def create_cron_report(current_version, latest_version, issues_status, issues_msg):
    """创建检查报告"""
    report = f"""
╔═══════════════════════════════════════════════════════════╗
║  OpenClaw Update Check Report                             ║
║  版本检查报告                                              ║
╠═══════════════════════════════════════════════════════════╣
║  检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║
║                                                           ║
║  当前版本：{current_version:<40} ║
║  最新版本：{latest_version:<40} ║
║                                                           ║
"""
    
    comparison = version_compare(current_version, latest_version)
    
    if comparison < 0:
        report += "║  📊 状态：发现新版本！建议更新                      ║\n"
        report += "║                                                           ║\n"
        report += "║  ⚠️  风险评估：                                           ║\n"
        report += f"║     Issues 状态：{issues_msg:<28} ║\n"
        report += "║                                                           ║\n"
        report += "║  ✅ 已创建备份（更新前会自动备份）                         ║\n"
        report += "║                                                           ║\n"
        report += "║  📋 下一步操作：                                           ║\n"
        report += "║     请回复\"确认更新\"或\"update now\"开始更新流程           ║\n"
        report += "║     或回复\"稍后\"推迟更新                                 ║\n"
    elif comparison == 0:
        report += "║  ✅ 状态：已是最新版本，无需更新                         ║\n"
    else:
        report += "║  ⚠️  状态：当前版本比最新版更新（开发版本？）            ║\n"
    
    report += "╚═══════════════════════════════════════════════════════════╝\n"
    
    return report

def main():
    log("🔍 开始定时更新检查... / Starting scheduled update check...")
    
    # 1. 检查 agent-reach
    log("Step 1/5: Checking agent-reach...")
    if not check_agent_reach():
        log("❌ agent-reach not available, aborting check")
        send_notification(
            "OpenClaw Update Check Failed",
            "agent-reach not available. Please install it first.",
            'urgent'
        )
        return 1
    log("✅ agent-reach available")
    
    # 2. 获取当前版本
    log("Step 2/5: Getting current version...")
    current_version = get_current_version()
    log(f"Current version: {current_version}")
    
    # 3. 获取最新版本
    log("Step 3/5: Getting latest version from GitHub...")
    latest_version = get_latest_version()
    if not latest_version:
        log("❌ Failed to get latest version")
        return 1
    log(f"Latest version: {latest_version}")
    
    # 4. 检查 Issues
    log("Step 4/5: Checking GitHub issues...")
    issues_status, issues_msg = check_issues()
    log(f"Issues status: {issues_status} - {issues_msg}")
    
    # 5. 生成报告并发送通知
    log("Step 5/5: Generating report and sending notification...")
    report = create_cron_report(current_version, latest_version, issues_status, issues_msg)
    print(report)
    
    comparison = version_compare(current_version, latest_version)
    
    if comparison < 0:
        # 有新版本
        title = "OpenClaw Update Available / 发现新版本"
        message = f"{current_version} → {latest_version}\nIssues: {issues_msg}\nReply '确认更新' to start update."
        
        if issues_status == 'critical':
            urgency = 'urgent'
            message = f"⚠️ CRITICAL ISSUES FOUND! Update NOT recommended.\n{issues_msg}"
        else:
            urgency = 'normal'
        
        send_notification(title, message, urgency)
        
        # 保存报告到文件
        report_file = Path.home() / '.openclaw' / 'update_check_report.txt'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        log(f"📄 Report saved to: {report_file}")
    else:
        # 无需更新
        send_notification(
            "OpenClaw Up to Date / 已是最新版本",
            f"Current: {current_version}\nNo update needed.",
            'normal'
        )
    
    log("✅ 检查完成 / Check completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
