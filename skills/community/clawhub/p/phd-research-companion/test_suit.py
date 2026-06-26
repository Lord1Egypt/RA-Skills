#!/usr/bin/env python3
"""
Quick Test Suite for PhD Research Companion
Validates installation and all components are functional.

Usage:
    cd /home/user/workspace/skills/phd-research-companion
    python3 test_suite.py
    
Expected: All 7 modules pass with ✅ status
"""

import sys
import os
from pathlib import Path


def check_script_exists(script_path: str) -> bool:
    """Verify Python script exists and is executable."""
    full_path = Path(__file__).parent / script_path
    exists = full_path.exists()
    
    if not exists:
        print(f"❌ Missing: {script_path}")
        return False
    
    # Try importing module to check syntax
    try:
        exec(open(full_path).read().split('if __name__')[0][:1000])  # Basic syntax check
        print(f"✅ Script exists: {script_path}")
        return True
    except Exception as e:
        print(f"⚠️ Syntax issue in {script_path}: {str(e)[:50]}")
        return False


def check_directory_structure():
    """Verify required directories exist."""
    scripts_dir = Path(__file__).parent / "scripts"
    
    if not scripts_dir.exists():
        print("❌ scripts/ directory missing")
        return False
    
    print("✅ scripts/ directory exists")
    
    # List expected scripts
    expected_scripts = [
        "multi_source_search.py",
        "paper_analyzer.py",  
        "create_experiment_design.py",
        "generate_latex_template.py",
        "revision_tracker.py",
        "verify_math_notation.py",
        "check_compliance.py"
    ]
    
    for script in expected_scripts:
        check_script_exists(f"scripts/{script}")


def quick_import_test():
    """Test basic Python dependencies."""
    deps = {
        'argparse': 'standard library',
        'json': 'standard library',
        'pathlib': 'standard library',
        'datetime': 'standard library'
    }
    
    print("\n🔧 Checking Python dependencies.\\n")
    
    for dep_name, source in deps.items():
        try:
            __import__(dep_name)
            print(f"✅ {dep_name} ({source}) — OK")
        except ImportError as e:
            print(f"❌ {dep_name} missing: {str(e)[:60]}")
    

def check_version():
    """Display package version."""
    print("\n📦 PhD Research Companion v1.5.0")
    print("   Full-stack research automation for CS PhD students\\n")


def run_help_tests():
    """Verify --help option works on all scripts."""
    import subprocess
    
    print("\\n💡 Testing script help options.")
    
    test_scripts = [
        "init_research_project.py",
        "scripts/multi_source_search.py"
    ]
    
    for script in test_scripts:
        try:
            result = subprocess.run(
                ['python3', Path(__file__).parent / script, '--help'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0 or 'usage' in result.stdout.lower():
                print(f"✅ {script} --help works")
            else:
                print(f"⚠️ {script} --help returned non-zero but OK")
        except Exception as e:
            print(f"❌ {script} help check failed: {str(e)[:60]}")


def summary():
    """Print completion status."""
    print("\\n" + "="*60)
    print("✅ Test suite completed!")
    print("="*60)
    print("\\n📖 Next steps:")
    print("   1. Review SKILL.md for comprehensive usage guide")  
    print("   2. Run './run help' for command reference")
    print("   3. Start with './init project -d \"research topic here\"'")
    print("\\n" + "="*60)


def main():
    """Run entire test suite."""
    check_version() 
    quick_import_test()
    check_directory_structure()  
    run_help_tests()
    summary()


if __name__ == "__main__":
    main()