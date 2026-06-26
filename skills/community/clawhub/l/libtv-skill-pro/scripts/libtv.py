#!/usr/bin/env python3
"""libtv 统一入口（v0.4.0+）

把所有子脚本聚合在一个命令里，Agent 路由更简单：

    python3 libtv.py <subcommand> [args...]

子命令列表：
    flow              LibTV 预设流程（故事脚本/角色三视图/首帧图生视频/音频生视频）
    node              节点能力（文本/图片/视频节点的细分动作）
    edit              修饰器（风格/标记/聚焦/运镜/角色库）
    model             模型路由（list 已知模型 / with 指定模型生成）

    session           创建会话 / 发消息（底层）
    query             查询会话进展（底层）
    upload            上传图片/视频到 OSS
    download          下载会话结果到本地

    batch             并发批量任务
    monitor           实时监控
    poll              简化轮询
    template          预设工作流模板
    export            导出结果（JSON/Markdown/HTML）
    history           会话历史管理
    project           项目管理

原有 scripts/xxx.py 路径仍可用（向后兼容）。
"""

import os
import sys
import importlib

# 让 sibling scripts 可被 import
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


COMMANDS = {
    # LibTV 功能矩阵层（推荐）
    "flow":      ("flow",              "LibTV 预设流程（故事脚本/角色三视图/首帧图生视频/音频生视频）"),
    "node":      ("node",              "节点能力（文本/图片/视频节点）"),
    "edit":      ("edit",              "修饰器（风格/标记/聚焦/运镜/角色库）"),
    "model":     ("model",             "模型路由（list 已知模型 / with 指定模型生成）"),
    # 底层基础工具
    "session":   ("create_session",    "创建会话 / 发送消息"),
    "query":     ("query_session",     "查询会话进展"),
    "upload":    ("upload_file",       "上传图片/视频到 OSS"),
    "download":  ("download_results",  "批量下载会话结果"),
    # 高级工作流
    "batch":     ("batch_create",      "并发批量任务"),
    "monitor":   ("monitor_session",   "实时监控会话"),
    "poll":      ("quick_poll",        "简化轮询（等到完成）"),
    "template":  ("workflow_template", "预设工作流模板"),
    "export":    ("export_results",    "导出结果（JSON/Markdown/HTML）"),
    "history":   ("session_history",   "会话历史管理"),
    "project":   ("manage_project",    "项目管理"),
}


def print_help():
    print(__doc__)
    print()
    print("用法：")
    print("  python3 libtv.py <subcommand> [args...]")
    print("  python3 libtv.py <subcommand> --help     # 查看子命令详细用法")
    print()
    print("子命令：")
    for name, (_, desc) in COMMANDS.items():
        print(f"  {name:<10} {desc}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        return

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"错误：未知子命令 '{cmd}'", file=sys.stderr)
        print(f"可用子命令：{', '.join(COMMANDS.keys())}", file=sys.stderr)
        sys.exit(2)

    module_name, _ = COMMANDS[cmd]
    # 把 sys.argv 改为 [scripts/xxx.py, ...rest_args]，让子模块 argparse 看到正确的 prog
    sys.argv = [f"libtv.py {cmd}"] + sys.argv[2:]

    mod = importlib.import_module(module_name)
    if hasattr(mod, "main"):
        # 子模块用的是 safe_run(main) wrapper；直接调 main，让异常按子模块定义处理。
        # 这里若想统一捕获，可改为 from _common import safe_run; safe_run(mod.main)
        try:
            mod.main()
        except SystemExit:
            raise
        except Exception:
            # 让子模块自己的 safe_run 处理；这里不该到达
            raise
    else:
        print(f"错误：模块 {module_name} 没有 main()", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
