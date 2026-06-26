#!/usr/bin/env python3
"""
自我进化检查脚本
定期检查自身行为，发现问题并记录
"""

import os
import sys
import json
from datetime import datetime

# 路径配置
WORKSPACE = "/root/.openclaw/workspace"
SKILL_DIR = "/root/.openclaw/skills/self-evolution"
LOG_FILE = os.path.join(WORKSPACE, "memory", "evolution-log.md")


def ensure_log_file():
    """确保日志文件存在"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("# 进化日志\n\n")
            f.write("记录Manager的自我诊断和改进过程。\n\n")
            f.write("| 日期 | 类型 | 问题 | 状态 |\n")
            f.write("|------|------|------|------|\n")


def log_entry(entry_type: str, problem: str, status: str = "待处理"):
    """记录日志条目"""
    ensure_log_file()
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"| {date} | {entry_type} | {problem} | {status} |\n")


def diagnose_conversation_understanding():
    """诊断对话理解能力"""
    issues = []
    
    # 检查最近的对话记录（如果存在）
    recent_log = os.path.join(WORKSPACE, "memory", datetime.now().strftime("%Y-%m-%d") + ".md")
    
    if os.path.exists(recent_log):
        with open(recent_log, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 检查是否有上下文混淆的迹象
            if "混淆" in content or "理解错误" in content:
                issues.append("近期存在对话理解问题记录")
    
    return issues


def diagnose_memory_discipline():
    """检查记忆纪律"""
    issues = []
    
    # 检查MEMORY.md是否存在教训但未落实
    memory_file = os.path.join(WORKSPACE, "MEMORY.md")
    if os.path.exists(memory_file):
        with open(memory_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 检查是否有"教训"但没有对应改进
            if "教训" in content and "已落实" not in content:
                issues.append("MEMORY.md中存在未落实的教训")
    
    return issues


def diagnose_soul_following():
    """检查SOUL.md原则遵守"""
    issues = []
    
    # 检查SOUL.md是否有对话理解原则
    soul_file = os.path.join(WORKSPACE, "SOUL.md")
    if os.path.exists(soul_file):
        with open(soul_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 检查是否有对话理解章节
            if "对话理解" not in content:
                issues.append("SOUL.md缺少对话理解原则")
    
    return issues


def diagnose_skill_integrity():
    """检查skill完整性"""
    issues = []
    
    # 检查skill文件
    skill_dir = "/root/.openclaw/skills"
    if os.path.exists(skill_dir):
        for skill in os.listdir(skill_dir):
            skill_path = os.path.join(skill_dir, skill)
            if os.path.isdir(skill_path):
                # 检查是否有SKILL.md但没有实现
                skill_md = os.path.join(skill_path, "SKILL.md")
                if os.path.exists(skill_md):
                    # 检查是否有对应的执行脚本
                    py_files = [f for f in os.listdir(skill_path) if f.endswith('.py')]
                    if not py_files and skill not in ['self-evolution']:
                        issues.append(f"Skill '{skill}' 有SKILL.md但无执行脚本")
    
    return issues


def run_diagnosis():
    """运行完整诊断"""
    print("🔍 开始自我诊断...")
    print("=" * 50)
    
    all_issues = []
    
    # 对话理解诊断
    print("\n📋 对话理解诊断...")
    cu_issues = diagnose_conversation_understanding()
    if cu_issues:
        print(f"  ⚠️ 发现 {len(cu_issues)} 个问题")
        all_issues.extend(cu_issues)
    else:
        print("  ✅ 无问题")
    
    # 记忆纪律诊断
    print("\n📋 记忆纪律诊断...")
    md_issues = diagnose_memory_discipline()
    if md_issues:
        print(f"  ⚠️ 发现 {len(md_issues)} 个问题")
        all_issues.extend(md_issues)
    else:
        print("  ✅ 无问题")
    
    # SOUL.md原则诊断
    print("\n📋 SOUL.md原则诊断...")
    sf_issues = diagnose_soul_following()
    if sf_issues:
        print(f"  ⚠️ 发现 {len(sf_issues)} 个问题")
        all_issues.extend(sf_issues)
    else:
        print("  ✅ 无问题")
    
    # Skill完整性诊断
    print("\n📋 Skill完整性诊断...")
    sh_issues = diagnose_skill_integrity()
    if sh_issues:
        print(f"  ⚠️ 发现 {len(sh_issues)} 个问题")
        all_issues.extend(sh_issues)
    else:
        print("  ✅ 无问题")
    
    # 汇总
    print("\n" + "=" * 50)
    if all_issues:
        print(f"⚠️ 共发现 {len(all_issues)} 个问题需要关注")
        for issue in all_issues:
            print(f"  - {issue}")
            log_entry("自我诊断", issue, "已记录")
        return False
    else:
        print("✅ 自我诊断通过，无明显问题")
        return True


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "diagnose":
        run_diagnosis()
    else:
        print("用法: python3 self-check.py diagnose")
        print("  运行自我诊断，检查自身问题")


if __name__ == "__main__":
    main()
