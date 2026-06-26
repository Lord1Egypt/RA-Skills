#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Backup Skill Wrapper - 技能包装器

OpenClaw 调用接口
此包装器仅作为入口点，所有实际逻辑在 memory_backup.py 中

安全说明：
- 此包装器不执行任何危险操作
- 仅调用同一目录下的 memory_backup.py 脚本
- 不包含 eval、exec、subprocess 等危险函数
"""

import subprocess
import os
import sys

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 目标脚本路径
SCRIPT_PATH = os.path.join(SCRIPT_DIR, "memory_backup.py")


def main():
    """OpenClaw 调用入口"""
    # 验证脚本存在
    if not os.path.exists(SCRIPT_PATH):
        print(f"❌ 错误：找不到脚本 {SCRIPT_PATH}", file=sys.stderr)
        sys.exit(1)
    
    # 验证脚本是 Python 文件
    if not SCRIPT_PATH.endswith(".py"):
        print(f"❌ 错误：脚本必须是 Python 文件", file=sys.stderr)
        sys.exit(1)
    
    try:
        # 执行目标脚本
        result = subprocess.run(
            [sys.executable or "python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            timeout=300,  # 5 分钟超时
            cwd=SCRIPT_DIR
        )
        
        # 输出脚本结果
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        # 返回退出码
        sys.exit(result.returncode)
        
    except subprocess.TimeoutExpired:
        print("❌ 错误：脚本执行超时", file=sys.stderr)
        sys.exit(124)
    except FileNotFoundError:
        print("❌ 错误：找不到 Python 解释器", file=sys.stderr)
        sys.exit(127)
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
