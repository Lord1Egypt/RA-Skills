#!/bin/bash
# 长桥智能投资助手 - 运行脚本

cd "$(dirname "$0")"

# 激活虚拟环境
source ~/.venv/longbridge/bin/activate

# 加载环境变量
export $(grep -v '^#' ~/.longbridge/env | xargs)

# 运行 Skill
python longbridge_skill.py "$@"
