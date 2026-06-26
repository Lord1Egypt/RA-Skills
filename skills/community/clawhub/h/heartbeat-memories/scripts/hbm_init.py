#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heartbeat-Memories System Initialization Script
Simple initialization for HBM skill.
"""

import os
import sys
import json
import shutil
from pathlib import Path
import platform
import subprocess
import argparse

def print_step(step, description):
    """Print step information"""
    print(f"[{step}] {description}")

def print_success(msg):
    """Print success message"""
    print(f"✅ {msg}")

def print_warning(msg):
    """Print warning message"""
    print(f"⚠️  {msg}")

def print_error(msg):
    """Print error message"""
    print(f"❌ {msg}")

def get_hbm_root():
    """Get HBM root directory (current directory)"""
    # Skill should be installed in OpenClaw skills directory
    # Use current script location as base
    script_dir = Path(__file__).parent.parent
    return script_dir.resolve()

def check_dependencies():
    """Check Python dependencies"""
    print_step("1", "Checking Python dependencies")
    
    required_packages = [
        "chromadb>=0.4.22",
        "sentence-transformers>=2.2.2",
        "faiss-cpu>=1.7.4",
    ]
    
    try:
        import chromadb
        import sentence_transformers
        import faiss
        print_success("All dependencies are installed")
        return True
    except ImportError as e:
        print_warning(f"Missing dependency: {e}")
        print("Please install required packages:")
        print(f"  pip install {' '.join(required_packages)}")
        return False

def setup_memory_structure(hbm_root):
    """Set up memory directory structure"""
    print_step("2", "Setting up memory structure")
    
    memory_dir = hbm_root / "memory"
    template_dir = memory_dir / "_templates"
    
    # Create directories
    directories = [
        memory_dir / "目标记忆库",
        memory_dir / "经验记忆库", 
        memory_dir / "情感记忆库",
        memory_dir / "会话记忆库",
        memory_dir / "版本记忆库",
        memory_dir / "心跳回忆",
        template_dir,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_success(f"Created directory: {directory.relative_to(hbm_root)}")
    
    # Copy template files if they exist
    template_source = hbm_root / "memory" / "_templates"
    if template_source.exists():
        for template_file in template_source.glob("*.md"):
            shutil.copy2(template_file, memory_dir)
            print_success(f"Copied template: {template_file.name}")
    
    return True

def create_config_file(hbm_root):
    """Create configuration file"""
    print_step("3", "Creating configuration file")
    
    config_dir = hbm_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    config_template = {
        "memory_system": {
            "enabled": True,
            "auto_record": True,
            "compression_ratio": 10
        },
        "semantic_search": {
            "enabled": True,
            "model_name": "all-MiniLM-L6-v2",
            "vector_db_path": "memory/vector_db"
        },
        "heartbeat_recall": {
            "enabled": True,
            "daily_limit": 3,
            "min_interval_minutes": 60,
            "scenarios": {
                "daily_conversation": 0.3,
                "after_task": 0.5,
                "forgotten_goal": 1.0,
                "special_day": 1.0
            }
        },
        "rag_system": {
            "enabled": False,  # Default OFF as requested
            "enable_limit_and_dedupe": False,
            "enable_cache": False,
            "enable_log_compression": True
        }
    }
    
    config_path = config_dir / "hbm_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_template, f, ensure_ascii=False, indent=2)
    
    print_success(f"Created config file: {config_path.relative_to(hbm_root)}")
    return True

def run_diagnostic(hbm_root):
    """Run diagnostic check"""
    print_step("4", "Running diagnostic check")
    
    checks = []
    
    # Check directories
    required_dirs = [
        hbm_root / "memory",
        hbm_root / "scripts",
        hbm_root / "config",
    ]
    
    for directory in required_dirs:
        if directory.exists():
            checks.append(("✅", f"Directory exists: {directory.relative_to(hbm_root)}"))
        else:
            checks.append(("❌", f"Directory missing: {directory.relative_to(hbm_root)}"))
    
    # Check files
    required_files = [
        hbm_root / "SKILL.md",
        hbm_root / "README.md",
        hbm_root / "requirements.txt",
    ]
    
    for file in required_files:
        if file.exists():
            checks.append(("✅", f"File exists: {file.relative_to(hbm_root)}"))
        else:
            checks.append(("❌", f"File missing: {file.relative_to(hbm_root)}"))
    
    # Display results
    print("\n📋 Diagnostic Results:")
    for status, message in checks:
        print(f"  {status} {message}")
    
    # Count errors
    error_count = sum(1 for status, _ in checks if status == "❌")
    return error_count == 0

def main():
    parser = argparse.ArgumentParser(description="Heartbeat-Memories Initialization")
    parser.add_argument("--check", action="store_true", help="Run diagnostic check only")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency check")
    parser.add_argument("--root", help="Specify HBM root directory")
    
    args = parser.parse_args()
    
    print("🚀 Heartbeat-Memories Initialization")
    print("=" * 50)
    
    # Get HBM root
    if args.root:
        hbm_root = Path(args.root).expanduser().resolve()
    else:
        hbm_root = get_hbm_root()
    
    print(f"📁 HBM Root: {hbm_root}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"💻 System: {platform.system()} {platform.release()}")
    
    if args.check:
        # Run diagnostic only
        success = run_diagnostic(hbm_root)
        return 0 if success else 1
    
    # Full initialization
    try:
        # 1. Check dependencies
        if not args.skip_deps:
            if not check_dependencies():
                print_warning("Dependency check failed, but continuing...")
        
        # 2. Setup memory structure
        if not setup_memory_structure(hbm_root):
            print_error("Failed to setup memory structure")
            return 1
        
        # 3. Create config file
        if not create_config_file(hbm_root):
            print_error("Failed to create config file")
            return 1
        
        # 4. Run diagnostic
        if not run_diagnostic(hbm_root):
            print_warning("Diagnostic found issues, but initialization completed")
        
        print("\n" + "=" * 50)
        print_success("Heartbeat-Memories Initialization Complete!")
        print("\n📌 Next Steps:")
        print("  1. Restart OpenClaw Gateway if needed")
        print("  2. Use trigger words in OpenClaw conversation:")
        print("     • 'memory system', 'help me recall'")
        print("     • 'save this', 'check goals'")
        print("  3. View documentation: README.md")
        
        return 0
        
    except Exception as e:
        print_error(f"Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())