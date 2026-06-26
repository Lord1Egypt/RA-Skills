#!/usr/bin/env python3
"""
PDCA Setup Wizard
Guide users through initial setup after installing the skill
"""

import sys
import os
import subprocess

def check_python():
    """Check Python version"""
    try:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Python: {result.stdout.strip()}")
            return True
        else:
            print("✗ Python 3.6+ not found")
            return False
    except:
        print("✗ Python 3.6+ not found")
        return False

def check_git():
    """Check if Git is available"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Git: {result.stdout.strip()}")
            return True
        else:
            print("⚠ Git not found")
            print("  → Git is optional. PDCA works without it.")
            print("  → Progress check will use file modification times only.")
            return False
    except:
        print("⚠ Git not found")
        print("  → Git is optional. PDCA works without it.")
        print("  → Progress check will use file modification times only.")
        return False

def create_workspace(workspace: str):
    """Create workspace directory"""
    if os.path.exists(workspace):
        print(f"✓ Workspace exists: {workspace}")
        return True
    
    try:
        os.makedirs(workspace, exist_ok=True)
        print(f"✓ Created workspace: {workspace}")
        return True
    except Exception as e:
        print(f"✗ Failed to create workspace: {e}")
        return False

def create_test_plan(workspace: str):
    """Create a test plan to verify installation"""
    plan_path = os.path.join(workspace, "plan.md")
    
    if os.path.exists(plan_path):
        print(f"ℹ️  Test plan already exists: {plan_path}")
        return True
    
    content = """# Task Plan: My First Plan

**Session:** not-set
**Created:** 2026-04-01 00:00
**Status:** IN_PROGRESS

## Checklist

- [ ] Task 1 - Get familiar with PDCA
- [ ] Task 2 - Create a real plan
- [ ] Task 3 - Complete a task

## Notes

_This is a test plan. Delete it when you're done._

## Check Results

_Fill in after completion..._
"""
    
    try:
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created test plan: {plan_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create test plan: {e}")
        return False

def init_git(workspace: str):
    """Initialize git repository (optional)"""
    git_dir = os.path.join(workspace, '.git')
    
    if os.path.exists(git_dir):
        print(f"ℹ️  Git already initialized in {workspace}")
        return True
    
    try:
        result = subprocess.run(
            ['git', 'init'],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Git initialized in {workspace}")
            return True
        else:
            print(f"⚠ Git init failed: {result.stderr.strip()}")
            return False
    except:
        print("⚠ Git not available, skipping git init")
        return False

def show_next_steps(workspace: str):
    """Show next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Setup complete! Here's what you can do next:")
    print("="*60)
    print(f"""
1. View your test plan:
   cd {workspace}
   cat plan.md

2. Create a real plan:
   manage_plan.py create "My Project" "Task 1" "Task 2" "Task 3"

3. Check progress:
   manage_plan.py check plan.md

4. Update task status:
   manage_plan.py update plan.md --completed 0 --current 1

5. Session start check (add to your workflow):
   manage_plan.py on-start {workspace} "your-session-id"

For more commands:
   manage_plan.py --help
""")

def main():
    print("="*60)
    print("🦞 PDCA Skill - Setup Wizard")
    print("="*60)
    print()
    
    # Step 1: Check dependencies
    print("Step 1/4: Checking dependencies...")
    python_ok = check_python()
    git_ok = check_git()
    print()
    
    if not python_ok:
        print("✗ Python 3.6+ is required. Please install Python and try again.")
        sys.exit(1)
    
    # Step 2: Create workspace
    print("Step 2/4: Setting up workspace...")
    default_workspace = os.path.expanduser("~/pdca-workspace")
    workspace = input(f"Workspace directory [{default_workspace}]: ").strip()
    if not workspace:
        workspace = default_workspace
    
    if not create_workspace(workspace):
        print("✗ Failed to create workspace. Please create it manually.")
        sys.exit(1)
    print()
    
    # Step 3: Create test plan
    print("Step 3/4: Creating test plan...")
    if not create_test_plan(workspace):
        print("⚠ Failed to create test plan, but you can create it manually.")
    print()
    
    # Step 4: Initialize git (optional)
    print("Step 4/4: Git Setup (optional)...")
    if git_ok:
        print("ℹ️  Git is available. It helps track file changes for progress recovery.")
        response = input("Initialize git repository in workspace? [Y/n]: ").strip().lower()
        if response != 'n':
            init_git(workspace)
    else:
        print("ℹ️  Git is not required. PDCA works fine without it.")
        print("   Progress recovery will use file modification times instead.")
    print()
    
    # Show next steps
    show_next_steps(workspace)
    
    print("\n💡 Tip: Add this to your SOUL.md or workflow:")
    print(f'   manage_plan.py on-start {workspace} "discord:YOUR_CHANNEL_ID"')

if __name__ == "__main__":
    main()
