#!/bin/bash
# project - 项目共享系统 CLI 快捷命令
# 用法: project <command> [options]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$SCRIPT_DIR/project.js" "$@"
