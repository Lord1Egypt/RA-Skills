"""HaluCatch Core — AI Skill 执行可靠性审查骨架脚本

向后兼容入口：保留 halucatch_core.py 文件名，实际逻辑在 halucatch 包中。

用法：
  python3 halucatch_core.py --skill-dir <目标Skill路径> [--validate]
  python3 halucatch_core.py --skill-dir <目标Skill路径> --output-dir <报告输出路径>

  python3 -m halucatch --skill-dir <目标Skill路径>        # 等价用法
"""
from halucatch.cli import main

if __name__ == '__main__':
    main()
