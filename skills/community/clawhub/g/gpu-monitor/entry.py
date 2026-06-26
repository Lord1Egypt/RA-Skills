#!/usr/bin/env python3
"""
GPU Monitor - Entry point for ClawHub deployment

This script wraps gpu_monitor.py and provides a clean CLI interface.
"""

import sys
import os

# 添加脚本所在目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from gpu_monitor import main, load_config


def create_entry_script():
    """创建可执行的入口脚本"""
    content = '''#!/usr/bin/env python3
"""GPU Monitor CLI Entry Point"""
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from gpu_monitor import main, load_config


def create_entry_script():
    """Create the entry script"""
    config = load_config()
    
    # 读取命令行参数
    args = sys.argv[1:]
    
    if not args or 'auto-start' not in args:
        print("GPU Monitor")
        print("=" * 40)
        main()


if __name__ == "__main__":
    create_entry_script()
'''
    with open(os.path.join(script_dir, "entry.py"), "w", encoding="utf-8") as f:
        f.write(content)


def package_skill():
    """打包技能"""
    import glob
    
    skill_files = [
        os.path.join(script_dir, "gpu_monitor.py"),
        os.path.join(script_dir, "entry.py"),
        os.path.join(script_dir, "SKILL.md"),
        os.path.join(script_dir, "README.md")
    ]
    
    return skill_files


if __name__ == "__main__":
    main()
