#!/bin/bash

# 结构化面试助手 - 执行脚本
# 调用全局安装的 interview-assistant 命令

# 检查 interview-assistant 是否已安装
if ! command -v interview-assistant &> /dev/null; then
    echo "错误：interview-assistant 命令未找到"
    echo "请先安装：cd /Users/claw/.openclaw/workspace-ideacat/hr-skills/interview-assistant && npm link"
    exit 1
fi

# 执行 interview-assistant 命令，传递所有参数
interview-assistant "$@"
