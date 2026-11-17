# -*- coding: utf-8 -*-
"""MC Skill Agent 入口脚本

Agent AI 通过此脚本调用 MC Skill 的各功能，返回 JSON 格式结果。

用法:
    python scripts/mc_skill.py <feature> [参数...]

示例:
    python scripts/mc_skill.py jar_parser --jar-path "create.jar"
    python scripts/mc_skill.py mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"
    python scripts/mc_skill.py mixin_scanner --mods-dir "./mods"
    python scripts/mc_skill.py crash_analyzer --crash-log "crash.txt"
    python scripts/mc_skill.py migration_assess --jar-path "create.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"
"""

import sys
import os
import json

# 将项目根目录加入路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "缺少功能参数",
            "usage": "python scripts/mc_skill.py <feature> [参数...]",
            "features": [
                "jar_parser - JAR结构解析",
                "mod_searcher - 模组检索下载",
                "env_builder - 环境引导搭建",
                "mixin_scanner - Mixin冲突扫描",
                "repacker - 资源重打包",
                "save_sync - 存档同步",
                "translator - 基础汉化",
                "crash_analyzer - 报错修复",
                "auto_fix - 自动修复",
                "migration_assess - 移植可行性评估",
            ],
        }, ensure_ascii=False, indent=2))
        return 1

    feature = sys.argv[1]
    args = sys.argv[2:]

    # 构建参数并调用 main.py
    cmd_args = ["main.py", "--feature", feature] + args

    # 保存原始 sys.argv
    original_argv = sys.argv
    sys.argv = cmd_args

    try:
        from main import main as main_entry
        main_entry()
        return 0
    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "feature": feature,
        }, ensure_ascii=False, indent=2))
        return 1
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    sys.exit(main())
