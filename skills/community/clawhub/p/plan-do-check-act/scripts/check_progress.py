#!/usr/bin/env python3
"""
PDCA Progress Checker
Infer task progress by checking git status and file modification times
"""

import sys
import os
import subprocess
from datetime import datetime, timedelta
import re

def get_git_status(workspace: str = "."):
    """Get git status"""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return [l for l in lines if l.strip()]
    except:
        pass
    return []

def get_recent_files(workspace: str = ".", minutes: int = 10) -> list:
    """Get recently modified files
    
    Args:
        minutes: Check files modified within this many minutes, default 10
    """
    recent = []
    cutoff = datetime.now() - timedelta(minutes=minutes)
    
    for root, dirs, files in os.walk(workspace):
        # Skip common directories
        skip_dirs = {'node_modules', '.git', '__pycache__', 'venv', 'dist', 'build', 'archive'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith(('.skill', '.pyc', '.log')):
                continue
            
            filepath = os.path.join(root, file)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime > cutoff:
                    rel_path = os.path.relpath(filepath, workspace)
                    recent.append({
                        'path': rel_path,
                        'mtime': mtime,
                        'age': datetime.now() - mtime
                    })
            except:
                pass
    
    # Sort by modification time
    recent.sort(key=lambda x: x['mtime'], reverse=True)
    return recent

def analyze_task_progress(task_text: str, recent_files: list, git_status: list) -> dict:
    """Analyze task progress
    
    Args:
        task_text: Task description
        recent_files: Recently modified files
        git_status: Git status list
    """
    progress = {
        'likely_started': False,
        'likely_completed': False,
        'evidence': [],
        'confidence': 'low',
        'task_type': 'unknown'
    }
    
    # Determine task type
    task_lower = task_text.lower()
    if any(kw in task_lower for kw in ['write', 'code', 'implement', 'api', 'function', '.py', '.js', '.ts']):
        progress['task_type'] = 'coding'
    elif any(kw in task_lower for kw in ['test', 'check', 'verify']):
        progress['task_type'] = 'testing'
    elif any(kw in task_lower for kw in ['deploy', 'config', 'server']):
        progress['task_type'] = 'deploy'
    elif any(kw in task_lower for kw in ['doc', 'readme']):
        progress['task_type'] = 'docs'
    elif any(kw in task_lower for kw in ['design', 'prototype']):
        progress['task_type'] = 'design'
    else:
        progress['task_type'] = 'general'
    
    # Extract keywords from task text
    clean_text = re.sub(r'[（(].*?[）)]', '', task_text)
    
    # Extract file extensions
    keywords = re.findall(r'[\w_]+\.(py|js|ts|html|css|json|md|yaml|yml|txt|doc|xlsx)', clean_text)
    
    # Extract English words
    keywords += re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', clean_text)
    
    # Add manual mappings for common programming terms
    if 'login' in clean_text.lower():
        keywords.extend(['login', 'auth', 'signin'])
    if 'register' in clean_text.lower() or 'signup' in clean_text.lower():
        keywords.extend(['register', 'signup', 'sign_up'])
    if 'api' in clean_text.lower():
        keywords.append('api')
    if 'user' in clean_text.lower():
        keywords.extend(['user', 'users'])
    if 'test' in clean_text.lower():
        keywords.extend(['test', 'tests', 'spec'])
    
    keywords = [k.lower() for k in keywords if len(k) >= 2]
    
    # Check based on task type
    if progress['task_type'] == 'coding':
        matched_files = []
        seen_files = set()
        for file_info in recent_files[:10]:
            filename = file_info['path'].lower()
            for kw in keywords:
                if kw in filename and file_info['path'] not in seen_files:
                    matched_files.append(file_info['path'])
                    seen_files.add(file_info['path'])
                    mins_ago = int(file_info['age'].total_seconds() / 60)
                    progress['evidence'].append(f"File {file_info['path']} modified ({mins_ago} min ago)")
                    progress['likely_started'] = True
                    break
        
        seen_git = set()
        for status in git_status:
            if status.startswith((' M', 'M ', 'A ', ' A')):
                filepath = status[3:].strip()
                for kw in keywords:
                    if kw in filepath.lower() and filepath not in seen_git:
                        seen_git.add(filepath)
                        progress['evidence'].append(f"Git modified: {filepath}")
                        progress['likely_started'] = True
                        break
    
    elif progress['task_type'] == 'testing':
        test_files = [f for f in recent_files if 'test' in f['path'].lower() or 'spec' in f['path'].lower()]
        if test_files:
            progress['likely_started'] = True
            progress['evidence'].append(f"Test file: {test_files[0]['path']}")
    
    elif progress['task_type'] == 'deploy':
        deploy_files = [f for f in recent_files 
                       if any(kw in f['path'].lower() for kw in ['config', 'docker', 'deploy', '.env', 'log'])]
        if deploy_files:
            progress['likely_started'] = True
            progress['evidence'].append(f"Deploy related: {deploy_files[0]['path']}")
    
    elif progress['task_type'] == 'docs':
        doc_files = [f for f in recent_files 
                    if f['path'].endswith(('.md', '.txt', '.docx', '.pdf'))]
        if doc_files:
            progress['likely_started'] = True
            progress['evidence'].append(f"Document: {doc_files[0]['path']}")
    
    else:
        if recent_files:
            progress['likely_started'] = True
            mins_ago = int(recent_files[0]['age'].total_seconds() / 60)
            progress['evidence'].append(f"Recent activity: {recent_files[0]['path']} ({mins_ago} min ago)")
    
    # Confidence判断
    if len(progress['evidence']) >= 2:
        progress['confidence'] = 'high'
    elif len(progress['evidence']) >= 1:
        progress['confidence'] = 'medium'
    
    return progress

def check_completion(plan_path: str) -> dict:
    """Check task completion confirmation"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'has_check_section': False,
        'check_items': [],
        'completed_items': [],
        'pending_items': []
    }
    
    # Find Check Results section
    check_match = re.search(r'## Check Results\n+(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if check_match:
        result['has_check_section'] = True
        check_section = check_match.group(1)
        
        for line in check_section.strip().split('\n'):
            if line.startswith('- ['):
                status_match = re.match(r'- \[(.|>)\] (.+)', line)
                if status_match:
                    status = status_match.group(1)
                    item = status_match.group(2)
                    if status == 'x':
                        result['completed_items'].append(item)
                    else:
                        result['pending_items'].append(item)
    
    return result

def check_recovery(workspace: str = ".", plan_path: str = None):
    """Check recovery progress"""
    print("\n=== PDCA Progress Check ===\n")
    
    if plan_path is None:
        plan_path = os.path.join(workspace, "plan.md")
    
    if not os.path.exists(plan_path):
        print("❌ plan.md not found")
        return
    
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_tasks = re.findall(r'^- \[.\] (.+)$', content, re.MULTILINE)
    completed_tasks = re.findall(r'^- \[x\] (.+)$', content, re.MULTILINE)
    pending_tasks = [t for t in all_tasks if t not in completed_tasks]
    
    created_match = re.search(r'\*\*Created:\*\* (\d{4}-\d{2}-\d{2} \d{2}:\d{2})', content)
    created_time = datetime.strptime(created_match.group(1), "%Y-%m-%d %H:%M") if created_match else None
    plan_age = datetime.now() - created_time if created_time else None
    
    print(f"📋 Task Progress: {len(completed_tasks)}/{len(all_tasks)} completed")
    if completed_tasks:
        print(f"   Completed: {', '.join(completed_tasks[:3])}{'...' if len(completed_tasks) > 3 else ''}")
    if pending_tasks:
        print(f"   Pending: {pending_tasks[0]}{'...' if len(pending_tasks) > 1 else ''}")
    
    if plan_age:
        hours = int(plan_age.total_seconds() / 3600)
        print(f"   Plan created: {hours} hours ago")
    
    git_status = get_git_status(workspace)
    print(f"\n💻 Git Status: {len(git_status)} changes")
    if git_status:
        for status in git_status[:5]:
            print(f"   {status}")
        if len(git_status) > 5:
            print(f"   ... and {len(git_status) - 5} more")
    
    check_minutes = 10
    recent = get_recent_files(workspace, minutes=check_minutes)
    
    print(f"\n📁 Recent Changes: {len(recent)} files (within {check_minutes} min)")
    if recent:
        for f in recent[:5]:
            mins_ago = int(f['age'].total_seconds() / 60)
            print(f"   {f['path']} ({mins_ago} min ago)")
        if len(recent) > 5:
            print(f"   ... and {len(recent) - 5} more")
    
    dep_script = os.path.join(os.path.dirname(__file__), 'check_deps.py')
    if os.path.exists(dep_script):
        import subprocess
        try:
            proc = subprocess.run(
                ['python3', dep_script, plan_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            if proc.stdout.strip():
                print(f"\n🔗 Dependency Check:")
                for line in proc.stdout.strip().split('\n'):
                    print(f"   {line}")
        except:
            pass
    
    completion = check_completion(plan_path)
    if completion['has_check_section']:
        print(f"\n✅ Completion Checklist:")
        if completion['completed_items']:
            for item in completion['completed_items']:
                print(f"   ✓ {item}")
        if completion['pending_items']:
            for item in completion['pending_items']:
                print(f"   ☐ {item}")
    
    if pending_tasks:
        next_task = pending_tasks[0]
        print(f"\n🔍 Analyzing next task: {next_task}")
        progress = analyze_task_progress(next_task, recent, git_status)
        
        if progress['confidence'] == 'high':
            print(f"   ✅ Likely completed")
        elif progress['likely_started']:
            print(f"   🔄 In progress (activity detected)")
        else:
            print(f"   ⏸️ Not started (no activity)")
        
        if progress['evidence']:
            print(f"   Evidence:")
            for ev in progress['evidence'][:3]:
                print(f"     - {ev}")
        
        print(f"\n💡 Suggestion:")
        if progress['confidence'] == 'high':
            print(f"   → Verify task is really done, then check it off")
        elif progress['likely_started']:
            print(f"   → Continue this task, progress should be there")
        else:
            print(f"   → Start this task from scratch")
    
    print()

def main():
    if len(sys.argv) > 1:
        workspace = sys.argv[1]
    else:
        workspace = "."
    
    plan_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    check_recovery(workspace, plan_path)

if __name__ == "__main__":
    main()
