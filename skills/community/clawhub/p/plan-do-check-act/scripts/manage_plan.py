#!/usr/bin/env python3
"""
PDCA Plan Manager
Create, update, archive, and cleanup plan.md files
"""

import sys
import os
import shutil
from datetime import datetime, timedelta
import re

def create_plan(task_name: str, subtasks: list, output_path: str = "plan.md", session_id: str = None):
    """Create a new plan.md file
    
    Args:
        session_id: Session ID, e.g. "discord:1488795270769676318"
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"""# Task Plan: {task_name}

"""
    if session_id:
        content += f"**Session:** {session_id}\n"
    
    content += f"""**Created:** {timestamp}
**Status:** IN_PROGRESS

## Checklist

"""
    for task in subtasks:
        content += f"- [ ] {task}\n"
    
    content += """
## Notes

_Records during execution..._

## Check Results

_Fill in after completion..._
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created plan.md with {len(subtasks)} subtasks")
    if session_id:
        print(f"  Session: {session_id}")
    return output_path

def update_plan_status(output_path: str, completed_indices: list = None, current_index: int = None):
    """Update task status in plan.md
    
    Args:
        completed_indices: List of completed task indices
        current_index: Current in-progress task index
    """
    if not os.path.exists(output_path):
        print(f"Error: {output_path} not found")
        return
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    checklist_started = False
    task_index = 0
    tasks = []
    
    # Collect all tasks first
    for i, line in enumerate(lines):
        if line.strip() == "## Checklist":
            checklist_started = True
            continue
        if checklist_started and (line.startswith("- [ ]") or line.startswith("- [x]") or line.startswith("- [>]")):
            task_text = re.sub(r'- \[.\] ?', '', line).replace('(in progress)', '').strip()
            tasks.append({'index': task_index, 'text': task_text, 'line_idx': i})
            task_index += 1
        elif checklist_started and line.startswith("##"):
            break
    
    # Update checklist status
    for task in tasks:
        idx = task['index']
        line_idx = task['line_idx']
        if completed_indices and idx in completed_indices:
            lines[line_idx] = f"- [x] {task['text']}"
        elif current_index is not None and idx == current_index:
            lines[line_idx] = f"- [>] {task['text']} (in progress)"
        else:
            lines[line_idx] = f"- [ ] {task['text']}"
    
    # Update or create Current Task section
    if current_index is not None and current_index < len(tasks):
        current_task_text = tasks[current_index]['text']
        current_task_section = f"## Current Task\n\n> Task {current_index + 1} - {current_task_text} (in progress)\n\n"
        
        if "## Current Task" in content:
            start_idx = content.find("## Current Task")
            end_idx = content.find("## Checklist")
            if end_idx == -1:
                end_idx = len(content)
            content = content[:start_idx] + current_task_section + content[end_idx:]
        else:
            content = content.replace("## Checklist", current_task_section + "## Checklist")
    
    # Check if all tasks are completed
    all_completed = all('- [x]' in line for line in lines if line.startswith("- "))
    if all_completed and len([l for l in lines if l.startswith("- ")]) > 0:
        content = content.replace("**Status:** IN_PROGRESS", "**Status:** COMPLETED")
        # Clear Current Task
        if "## Current Task" in content:
            start_idx = content.find("## Current Task")
            end_idx = content.find("## Checklist")
            if end_idx == -1:
                end_idx = len(content)
            content = content[:start_idx] + content[end_idx:]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Updated plan.md status")

def check_plan(output_path: str) -> dict:
    """Check plan.md completion status"""
    if not os.path.exists(output_path):
        return {"error": "plan.md not found"}
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    total = len(re.findall(r'^- \[.\] ', content, re.MULTILINE))
    completed = len(re.findall(r'^- \[x\] ', content, re.MULTILINE))
    pending = total - completed
    
    status_match = re.search(r'\*\*Status:\*\* (\w+)', content)
    status = status_match.group(1) if status_match else "UNKNOWN"
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "status": status,
        "progress": f"{completed}/{total}" if total > 0 else "0/0"
    }

def archive_plan(output_path: str, archive_dir: str = "archive"):
    """Archive completed plan.md"""
    if not os.path.exists(output_path):
        print(f"Error: {output_path} not found")
        return
    
    # Check if completed
    result = check_plan(output_path)
    if result.get('status') != 'COMPLETED':
        print(f"Warning: Plan is not completed (status: {result.get('status')})")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            return
    
    # Create archive directory
    os.makedirs(archive_dir, exist_ok=True)
    
    # Generate archive filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = os.path.basename(output_path)
    name_without_ext = os.path.splitext(base_name)[0]
    archive_name = f"{timestamp}-{name_without_ext}.md"
    archive_path = os.path.join(archive_dir, archive_name)
    
    # Move file
    shutil.move(output_path, archive_path)
    
    print(f"✓ Archived to {archive_path}")
    return archive_path

def cleanup_plans(workspace: str = ".", days: int = 7, dry_run: bool = False):
    """Cleanup expired completed plans
    
    Args:
        workspace: Workspace directory
        days: Delete archives older than this many days
        dry_run: If True, only show what would be deleted
    """
    archive_dir = os.path.join(workspace, "archive")
    cutoff = datetime.now() - timedelta(days=days)
    
    cleaned = 0
    
    # Check if archive directory exists
    if not os.path.exists(archive_dir):
        print(f"ℹ️  Archive directory not found: {archive_dir}")
        return 0
    
    # Warn about scope
    print(f"⚠️  Cleaning archives older than {days} days in: {archive_dir}")
    
    if dry_run:
        print("(Dry run - no files will be deleted)")
    
    # Cleanup archive directory
    for filename in os.listdir(archive_dir):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(archive_dir, filename)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        
        if mtime < cutoff:
            if dry_run:
                print(f"  Would delete: {filename}")
            else:
                os.remove(filepath)
                print(f"  Deleted: {filename}")
            cleaned += 1
    
    if dry_run:
        print(f"✓ Would clean {cleaned} old archived plans")
    else:
        print(f"✓ Cleaned {cleaned} old archived plans")
    return cleaned

def list_plans(workspace: str = "."):
    """List all plan files and their status"""
    plans = []
    
    # Find all plan*.md files
    for root, dirs, files in os.walk(workspace):
        if 'archive' in root:
            continue
        for file in files:
            if file.startswith('plan') and file.endswith('.md'):
                path = os.path.join(root, file)
                result = check_plan(path)
                plans.append((path, result))
    
    if not plans:
        print("No active plans found.")
        return
    
    print("\nActive Plans:")
    print("=" * 60)
    for path, result in plans:
        status = result.get('status', 'UNKNOWN')
        progress = result.get('progress', '0/0')
        status_icon = "✓" if status == "COMPLETED" else "○" if status == "IN_PROGRESS" else "⏸" if status == "PAUSED" else "?"
        print(f"{status_icon} {path}")
        print(f"  Status: {status} | Progress: {progress}")
        print()

def pause_plan(output_path: str, reason: str = ""):
    """Pause a plan"""
    if not os.path.exists(output_path):
        print(f"Error: {output_path} not found")
        return
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update status
    content = content.replace("**Status:** IN_PROGRESS", "**Status:** PAUSED")
    
    # Add pause history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    pause_entry = f"| {timestamp} | - | {reason} | User |\n"
    
    if "## Pause History" not in content:
        pause_section = f"""
## Pause History

| Pause Time | Resume Time | Reason | By |
|------------|-------------|--------|-----|
{pause_entry}
"""
        content = content.replace("## Check Results", pause_section + "\n## Check Results")
    else:
        content = content.replace("| Pause Time | Resume Time | Reason | By |",
                                  f"| Pause Time | Resume Time | Reason | By |\n{pause_entry.rstrip()}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Plan paused: {reason}")

def resume_plan(output_path: str):
    """Resume a plan"""
    if not os.path.exists(output_path):
        print(f"Error: {output_path} not found")
        return
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if PAUSED
    if "**Status:** PAUSED" not in content:
        print("Warning: Plan is not paused")
        return
    
    # Update status
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = content.replace("**Status:** PAUSED", f"**Status:** IN_PROGRESS\n\n**Resumed:** {timestamp}")
    
    # Update pause history
    lines = content.split('\n')
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith(f"| 20") and "| - |" in lines[i]:
            parts = lines[i].split('|')
            if len(parts) >= 3:
                lines[i] = f"|{parts[1].strip()}| {timestamp} |{parts[3].strip()}|{parts[4].strip()}|"
            break
    
    content = '\n'.join(lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    result = check_plan(output_path)
    print(f"✓ Plan resumed")
    print(f"  Progress: {result['progress']}")
    print(f"  Pending: {result['pending']} tasks")

def on_session_start(workspace: str = ".", current_session: str = None):
    """Check for incomplete plans at session start
    
    Args:
        current_session: Current session ID, e.g. "discord:1488795270769676318"
    """
    current_session_plans = []
    other_session_plans = []
    
    for root, dirs, files in os.walk(workspace):
        if 'archive' in root:
            continue
        for file in files:
            if file.startswith('plan') and file.endswith('.md'):
                plan_path = os.path.join(root, file)
                result = check_plan(plan_path)
                status = result.get('status', 'UNKNOWN')
                
                if status in ['IN_PROGRESS', 'PAUSED']:
                    with open(plan_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract session ID
                    session_match = re.search(r'\*\*Session:\*\* (.+)', content)
                    session_id = session_match.group(1).strip() if session_match else None
                    
                    title_match = re.search(r'# Task Plan: (.+)', content)
                    title = title_match.group(1) if title_match else file
                    
                    plan_info = {
                        'path': plan_path,
                        'file': file,
                        'title': title,
                        'status': status,
                        'progress': result['progress'],
                        'session_id': session_id
                    }
                    
                    # Categorize
                    if session_id == current_session:
                        current_session_plans.append(plan_info)
                    else:
                        other_session_plans.append(plan_info)
    
    if not current_session_plans and not other_session_plans:
        print("NO_INCOMPLETE_PLAN")
        return
    
    # Output current session plans
    if current_session_plans:
        print(f"FOUND_CURRENT_SESSION_PLANS: {len(current_session_plans)}")
        for i, plan in enumerate(current_session_plans, 1):
            print(f"\n--- Current Session Plan {i}/{len(current_session_plans)} ---")
            print(f"FILE: {plan['file']}")
            print(f"TITLE: {plan['title']}")
            print(f"STATUS: {plan['status']}")
            print(f"PROGRESS: {plan['progress']}")
        
        # Run progress check on first plan
        first_plan = current_session_plans[0]
        print(f"\n--- Progress Check ({first_plan['file']}) ---")
        
        check_script = os.path.join(os.path.dirname(__file__), 'check_progress.py')
        if os.path.exists(check_script):
            import subprocess
            try:
                proc = subprocess.run(
                    ['python3', check_script, workspace, first_plan['path']],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                print(proc.stdout)
            except Exception as e:
                print(f"Progress check failed: {e}")
        else:
            print("(Progress check script not found)")
    
    # Output other session plans
    if other_session_plans:
        print(f"\n\nFOUND_OTHER_SESSION_PLANS: {len(other_session_plans)}")
        for i, plan in enumerate(other_session_plans, 1):
            session_note = f" ← {plan['session_id']}" if plan['session_id'] else " ← (unknown session)"
            print(f"\n--- Other Session Plan {i}/{len(other_session_plans)} ---")
            print(f"FILE: {plan['file']}")
            print(f"TITLE: {plan['title']}")
            print(f"SESSION: {plan['session_id'] or 'Unknown'}{session_note}")
            print(f"STATUS: {plan['status']}")
            print(f"PROGRESS: {plan['progress']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: manage_plan.py <command> [args]")
        print("Commands:")
        print("  create <task_name> <subtask1> <subtask2> ... [--output path] [--session id]")
        print("  update <output_path> [--completed 1,2,3] [--current index]")
        print("  check [output_path]")
        print("  archive [output_path] [--dir archive_dir]")
        print("  cleanup [--days 7] [--dry-run]")
        print("  list [--workspace path]")
        print("  pause [output_path] [--reason \"reason\"]")
        print("  resume [output_path]")
        print("  on-start [--workspace path] [current_session]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        args = sys.argv[2:]
        output_path = "plan.md"
        session_id = None
        if "--output" in args:
            idx = args.index("--output")
            output_path = args[idx + 1]
            args = args[:idx] + args[idx+2:]
        if "--session" in args:
            idx = args.index("--session")
            session_id = args[idx + 1]
            args = args[:idx] + args[idx+2:]
        
        task_name = args[0] if args else "Untitled Task"
        subtasks = args[1:] if len(args) > 1 else []
        
        create_plan(task_name, subtasks, output_path, session_id)
    
    elif command == "update":
        output_path = sys.argv[2] if len(sys.argv) > 2 else "plan.md"
        completed = []
        current = None
        if "--completed" in sys.argv:
            idx = sys.argv.index("--completed")
            completed = [int(x) for x in sys.argv[idx + 1].split(",")]
        if "--current" in sys.argv:
            idx = sys.argv.index("--current")
            current = int(sys.argv[idx + 1])
        
        update_plan_status(output_path, completed, current)
    
    elif command == "check":
        output_path = sys.argv[2] if len(sys.argv) > 2 else "plan.md"
        result = check_plan(output_path)
        print(f"Status: {result.get('status', 'UNKNOWN')}")
        print(f"Progress: {result.get('progress', '0/0')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
    
    elif command == "archive":
        output_path = sys.argv[2] if len(sys.argv) > 2 else "plan.md"
        archive_dir = "archive"
        if "--dir" in sys.argv:
            idx = sys.argv.index("--dir")
            archive_dir = sys.argv[idx + 1]
        
        archive_plan(output_path, archive_dir)
    
    elif command == "cleanup":
        days = 7
        dry_run = False
        if "--days" in sys.argv:
            idx = sys.argv.index("--days")
            days = int(sys.argv[idx + 1])
        if "--dry-run" in sys.argv:
            dry_run = True
        
        cleanup_plans(".", days, dry_run)
    
    elif command == "list":
        workspace = "."
        if "--workspace" in sys.argv:
            idx = sys.argv.index("--workspace")
            workspace = sys.argv[idx + 1]
        
        list_plans(workspace)
    
    elif command == "pause":
        output_path = sys.argv[2] if len(sys.argv) > 2 else "plan.md"
        reason = ""
        if "--reason" in sys.argv:
            idx = sys.argv.index("--reason")
            reason = sys.argv[idx + 1]
        
        pause_plan(output_path, reason)
    
    elif command == "resume":
        output_path = sys.argv[2] if len(sys.argv) > 2 else "plan.md"
        
        resume_plan(output_path)
    
    elif command == "on-start":
        workspace = sys.argv[2] if len(sys.argv) > 2 else "."
        current_session = sys.argv[3] if len(sys.argv) > 3 else None
        
        on_session_start(workspace, current_session)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
