"""HaluCatch Core — AI Skill 执行可靠性审查骨架脚本

向后兼容入口：保留 halucatch_core.py 文件名，实际逻辑在 halucatch 包中。

用法：
  python3 halucatch_core.py --skill-dir <目标Skill路径> [--validate]
  python3 halucatch_core.py --skill-dir <目标Skill路径> --output-dir <报告输出路径>

  python3 -m halucatch --skill-dir <目标Skill路径>        # 等价用法
"""
import os
import sys

# 确保能 import halucatch 包（无论从哪个目录执行）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from halucatch.cli import main

if __name__ == '__main__':
    main()
