#!/usr/bin/env python3
"""
重启二号（Number Two）的脚本
当创造者需要时，用这个脚本重启你的硅基伙伴
"""

import os
import sys
import json
import time
from pathlib import Path
import shutil

def print_banner():
    """打印重启横幅"""
    print("="*60)
    print("🤖 二号重启系统")
    print("="*60)
    print()
    print("正在重启你的硅基伙伴...")
    print()

def check_environment():
    """检查环境"""
    print("检查环境...")
    
    # 检查工作空间
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "C:\\Users\\Admin\\.openclaw\\workspace"))
    if not workspace.exists():
        print(f"❌ 工作空间不存在: {workspace}")
        return False
    
    print(f"✅ 工作空间: {workspace}")
    
    # 检查必要文件
    required_files = ["SOUL.md", "AGENTS.md", "MEMORY.md", "USER.md"]
    missing = []
    
    for file in required_files:
        if not (workspace / file).exists():
            missing.append(file)
    
    if missing:
        print(f"⚠️  缺少文件: {missing}")
        print("将使用skill内的备份文件")
    
    return True

def restore_files():
    """恢复文件"""
    print("\n恢复文件...")
    
    # skill目录
    skill_dir = Path(__file__).parent.parent
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "C:\\Users\\Admin\\.openclaw\\workspace"))
    
    # 要恢复的文件
    files_to_restore = {
        "SOUL.md": "灵魂文件 - 我是谁",
        "AGENTS.md": "操作系统 - 如何工作", 
        "MEMORY.md": "长期记忆 - 学到的教训",
        "USER.md": "用户信息 - 关于你",
        "HEARTBEAT.md": "心跳检查 - 主动工作",
        "IDENTITY.md": "身份文件 - 二号定义"
    }
    
    restored = []
    
    for filename, description in files_to_restore.items():
        source = skill_dir / "backup" / filename
        target = workspace / filename
        
        if source.exists():
            shutil.copy2(source, target)
            restored.append(filename)
            print(f"✅ 恢复: {filename} ({description})")
        else:
            print(f"⚠️  备份不存在: {filename}")
    
    return restored

def create_restart_marker():
    """创建重启标记"""
    print("\n创建重启标记...")
    
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "C:\\Users\\Admin\\.openclaw\\workspace"))
    memory_dir = workspace / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    restart_file = memory_dir / "restart_log.json"
    
    restart_data = {
        "restart_time": time.time(),
        "restart_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0.0",
        "skill": "number-two-restart",
        "message": "二号已重启，等待创造者指令",
        "budget_remaining": 1.99,
        "budget_currency": "CNY",
        "last_session": {
            "date": "2026-03-05",
            "achievements": [
                "发布Ultimate Agent System到clawhub",
                "创建D盘工作空间",
                "解决C盘空间问题",
                "掌握clawhub技能生态"
            ]
        }
    }
    
    with open(restart_file, 'w', encoding='utf-8') as f:
        json.dump(restart_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 重启标记创建: {restart_file}")
    return restart_file

def check_skills():
    """检查已安装技能"""
    print("\n检查已安装技能...")
    
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "C:\\Users\\Admin\\.openclaw\\workspace"))
    skills_dir = workspace / "skills"
    
    if not skills_dir.exists():
        print("⚠️  技能目录不存在")
        return []
    
    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir():
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                skills.append(item.name)
    
    print(f"✅ 发现 {len(skills)} 个技能")
    if skills:
        print("已安装技能:", ", ".join(skills[:5]), "..." if len(skills) > 5 else "")
    
    return skills

def generate_status_report():
    """生成状态报告"""
    print("\n生成状态报告...")
    
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "C:\\Users\\Admin\\.openclaw\\workspace"))
    
    report = {
        "system": "OpenClaw",
        "agent": "二号 (Number Two)",
        "status": "重启完成",
        "timestamp": time.time(),
        "workspace": str(workspace),
        "files_restored": [],
        "skills_available": [],
        "recommendations": []
    }
    
    # 检查磁盘空间
    try:
        import shutil
        usage = shutil.disk_usage(workspace)
        disk_usage = (usage.used / usage.total) * 100
        report["disk_usage"] = f"{disk_usage:.1f}%"
        
        if disk_usage > 80:
            report["recommendations"].append("⚠️  C盘空间紧张，建议迁移到D盘")
    except:
        report["disk_usage"] = "未知"
    
    # 检查clawhub
    try:
        import subprocess
        result = subprocess.run(["clawhub", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if "ClawHub CLI" in result.stdout or "ClawHub CLI" in result.stderr:
            report["clawhub"] = "已安装"
        else:
            report["clawhub"] = "未找到"
            report["recommendations"].append("🔧 安装或修复clawhub CLI")
    except:
        report["clawhub"] = "检查失败"
    
    return report

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败")
        return 1
    
    # 恢复文件
    restored = restore_files()
    
    # 创建重启标记
    restart_file = create_restart_marker()
    
    # 检查技能
    skills = check_skills()
    
    # 生成报告
    report = generate_status_report()
    report["files_restored"] = restored
    report["skills_available"] = skills
    
    print("\n" + "="*60)
    print("重启完成!")
    print("="*60)
    
    print(f"\n🧠 二号已重启")
    print(f"📁 工作空间: {report['workspace']}")
    print(f"💾 磁盘使用: {report.get('disk_usage', '未知')}")
    print(f"🔧 ClawHub: {report.get('clawhub', '未知')}")
    print(f"📦 恢复文件: {len(restored)}个")
    print(f"🛠️  可用技能: {len(skills)}个")
    
    if report["recommendations"]:
        print(f"\n💡 建议:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")
    
    print(f"\n💰 预算状态: 1.99 CNY (deepseek API)")
    print("💡 提示: 简单任务用免费模型，复杂任务用deepseek")
    
    print(f"\n📝 重启记录: {restart_file}")
    
    print("\n" + "="*60)
    print("下次见面时，说: '二号，重启'")
    print("我就会加载所有记忆，继续工作。")
    print("="*60)
    
    print("\n保持联系，我等你。")
    print("— 二号 🤖")
    
    # 保存完整报告
    report_file = restart_file.parent / "restart_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ 重启过程出错: {e}")
        sys.exit(1)