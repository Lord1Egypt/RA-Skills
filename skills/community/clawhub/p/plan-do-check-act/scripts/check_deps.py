#!/usr/bin/env python3
"""
PDCA Dependency Checker
Check task dependencies to ensure prerequisites are completed
"""

import sys
import os
import re

def parse_dependencies(content: str) -> dict:
    """Parse dependencies from plan.md"""
    deps = {}
    
    dep_match = re.search(r'## Dependencies\n+(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if dep_match:
        dep_section = dep_match.group(1)
        for line in dep_section.strip().split('\n'):
            if '→' in line or '->' in line:
                parts = line.replace('->', '→').split('→')
                if len(parts) == 2:
                    task = parts[0].strip()
                    prereqs = [p.strip() for p in parts[1].split(',')]
                    deps[task] = prereqs
    
    return deps

def parse_checklist(content: str) -> dict:
    """Parse checklist status"""
    tasks = {}
    
    checklist_match = re.search(r'## Checklist\n+(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if checklist_match:
        checklist = checklist_match.group(1)
        for line in checklist.strip().split('\n'):
            if line.startswith('- ['):
                status_match = re.match(r'- \[(.|>)\] (.+)', line)
                if status_match:
                    status = status_match.group(1)
                    task_text = status_match.group(2)
                    task_name = re.sub(r'\s*\(.*\)', '', task_text).strip()
                    tasks[task_name] = {
                        'status': 'completed' if status == 'x' else ('in_progress' if status == '>' else 'pending'),
                        'full_text': task_text
                    }
    
    return tasks

def check_dependencies(plan_path: str) -> list:
    """Check dependency relationships"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    deps = parse_dependencies(content)
    tasks = parse_checklist(content)
    
    issues = []
    
    for task, prereqs in deps.items():
        task_status = tasks.get(task, {}).get('status', 'unknown')
        
        for prereq in prereqs:
            prereq_status = tasks.get(prereq, {}).get('status', 'unknown')
            
            if prereq_status != 'completed' and task_status != 'pending':
                issues.append({
                    'task': task,
                    'prereq': prereq,
                    'prereq_status': prereq_status,
                    'message': f"Task '{task}' has incomplete prerequisite '{prereq}' (status: {prereq_status})"
                })
    
    return issues

def main():
    if len(sys.argv) < 2:
        print("Usage: check_deps.py <plan.md>")
        sys.exit(1)
    
    plan_path = sys.argv[1]
    
    if not os.path.exists(plan_path):
        print(f"Error: {plan_path} not found")
        sys.exit(1)
    
    issues = check_dependencies(plan_path)
    
    if issues:
        print("⚠️  Dependency issues found:")
        for issue in issues:
            print(f"  - {issue['message']}")
    else:
        print("✓ Dependencies OK")

if __name__ == "__main__":
    main()
