#!/usr/bin/env python3
"""
Test script for minimax-vision-search skill.
Run this before publishing to verify the skill works.
"""

import subprocess
import sys
import os


def check_uvx():
    """Check if uvx is installed."""
    print("1. Checking uvx installation...")
    result = subprocess.run(['which', 'uvx'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✓ uvx found at: {result.stdout.strip()}")
        return True
    else:
        print("   ✗ uvx not found. Install: brew install uv")
        return False


def check_api_key():
    """Check if MINIMAX_API_KEY is set."""
    print("2. Checking MINIMAX_API_KEY...")
    api_key = os.environ.get('MINIMAX_API_KEY')
    if api_key:
        print(f"   ✓ MINIMAX_API_KEY is set (length: {len(api_key)})")
        return True
    else:
        print("   ✗ MINIMAX_API_KEY not set")
        print("   Run: export MINIMAX_API_KEY=your_key")
        return False


def check_api_host():
    """Check if MINIMAX_API_HOST is set."""
    print("3. Checking MINIMAX_API_HOST...")
    api_host = os.environ.get('MINIMAX_API_HOST')
    if api_host:
        print(f"   ✓ MINIMAX_API_HOST is set: {api_host}")
        return True
    else:
        print("   ℹ MINIMAX_API_HOST not set (will use default)")
        return True  # Not required, just informational


def check_scripts():
    """Check if scripts are valid Python."""
    print("4. Checking Python scripts...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    scripts = ['understand_image.py', 'web_search.py']
    all_valid = True
    
    for script in scripts:
        path = os.path.join(script_dir, script)
        if os.path.exists(path):
            result = subprocess.run(['python3', '-m', 'py_compile', path], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✓ {script} is valid Python")
            else:
                print(f"   ✗ {script} has syntax errors: {result.stderr}")
                all_valid = False
        else:
            print(f"   ✗ {script} not found")
            all_valid = False
    
    return all_valid


def main():
    print("=" * 50)
    print("minimax-vision-search Skill Test")
    print("=" * 50)
    print()
    
    results = []
    
    results.append(check_uvx())
    results.append(check_api_key())
    results.append(check_api_host())
    results.append(check_scripts())
    
    print()
    print("=" * 50)
    
    if all(results):
        print("✓ All checks passed! Skill is ready to publish.")
        return 0
    else:
        print("✗ Some checks failed. Please fix before publishing.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
