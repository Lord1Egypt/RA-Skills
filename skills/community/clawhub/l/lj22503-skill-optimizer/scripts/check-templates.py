#!/usr/bin/env python3
"""
技能模板文件校验器
检查技能中提到的所有模板/参考文件是否实际存在
"""

import os
import re
import sys
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def check_skill_templates(skill_dir):
    """检查单个技能的模板文件"""
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    
    if not os.path.exists(skill_md):
        return {'status': '❌ FAIL', 'missing': ['SKILL.md 不存在'], 'mentioned': []}
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取提到的文件
    mentioned_files = set()
    
    # 匹配 templates/xxx.md 格式
    patterns = [
        r'templates/[\w-]+\.md',
        r'references/[\w-]+\.md',
        r'scripts/[\w-]+\.py',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        mentioned_files.update(matches)
    
    # 检查文件是否存在
    missing = []
    found = []
    
    for file_path in mentioned_files:
        full_path = os.path.join(skill_dir, file_path)
        if os.path.exists(full_path):
            found.append(file_path)
        else:
            missing.append(file_path)
    
    if missing:
        return {
            'status': '❌ FAIL',
            'missing': missing,
            'found': found,
            'mentioned': list(mentioned_files)
        }
    else:
        return {
            'status': '✅ PASS',
            'missing': [],
            'found': found,
            'mentioned': list(mentioned_files)
        }

def check_all_skills(skills_root):
    """检查所有技能"""
    results = []
    
    for root, dirs, files in os.walk(skills_root):
        if 'SKILL.md' in files:
            result = check_skill_templates(root)
            skill_name = os.path.basename(root)
            results.append({
                'skill': skill_name,
                'path': root,
                'result': result
            })
    
    return results

def main():
    if len(sys.argv) > 1:
        # 检查单个技能
        skill_dir = sys.argv[1]
        result = check_skill_templates(skill_dir)
        skill_name = os.path.basename(skill_dir)
        
        print(f"{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}║   技能模板文件校验 - {skill_name:<40}║{Colors.RESET}")
        print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        print(f"状态：{result['status']}")
        print(f"\n提到的文件 ({len(result['mentioned'])}个):")
        for f in result['mentioned']:
            if f in result['found']:
                print(f"  {Colors.GREEN}✅{Colors.RESET} {f}")
            else:
                print(f"  {Colors.RED}❌{Colors.RESET} {f} (缺失)")
        
        if result['missing']:
            print(f"\n{Colors.RED}❌ 缺少 {len(result['missing'])} 个文件：{Colors.RESET}")
            for f in result['missing']:
                print(f"  - {f}")
            print(f"\n{Colors.RED}❌ 校验不通过！请先创建缺失的模板文件。{Colors.RESET}")
            print(f"{Colors.YELLOW}⚠️  根据技能优化器标准，模板文件缺失直接判定为不合格（<60 分）{Colors.RESET}")
            sys.exit(1)
        else:
            print(f"\n{Colors.GREEN}✅ 所有提到的文件都存在，校验通过！{Colors.RESET}")
            sys.exit(0)
    
    else:
        # 检查所有技能
        skills_root = '/home/admin/.openclaw/workspace/betterlife/skills'
        results = check_all_skills(skills_root)
        
        print(f"{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}║   BetterLife 技能模板文件批量校验                        ║{Colors.RESET}")
        print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        passed = 0
        failed = 0
        total_files = 0
        missing_files = 0
        
        failed_skills = []
        
        for r in results:
            if r['result']['status'] == '✅ PASS':
                passed += 1
                total_files += len(r['result']['found'])
            else:
                failed += 1
                missing_files += len(r['result']['missing'])
                failed_skills.append(r)
        
        print(f"{Colors.GREEN}✅ 通过：{passed} 个技能{Colors.RESET}")
        print(f"{Colors.RED}❌ 失败：{failed} 个技能{Colors.RESET}")
        print(f"\n总文件数：{total_files} 个")
        print(f"缺失文件：{missing_files} 个\n")
        
        if failed_skills:
            print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            print(f"{Colors.RED}失败的技能 ({failed}个):{Colors.RESET}\n")
            
            for r in failed_skills:
                print(f"{Colors.YELLOW}{r['skill']}{Colors.RESET}")
                print(f"  路径：{r['path']}")
                print(f"  缺失文件:")
                for f in r['result']['missing']:
                    print(f"    - {f}")
                print()
            
            print(f"{Colors.RED}❌ 校验不通过！请先创建缺失的模板文件。{Colors.RESET}")
            print(f"{Colors.YELLOW}⚠️  根据技能优化器标准，模板文件缺失直接判定为不合格（<60 分）{Colors.RESET}")
            sys.exit(1)
        else:
            print(f"{Colors.GREEN}✅ 所有技能的模板文件校验通过！{Colors.RESET}")
            sys.exit(0)

if __name__ == '__main__':
    main()
