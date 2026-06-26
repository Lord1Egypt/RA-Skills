#!/bin/bash
#
# llm-key-pool Skill入口脚本
#

# 获取参数
PROMPT="$1"
shift

# 运行llm-key-pool，默认使用Skill目录下的配置
llm-key-pool --prompt "$PROMPT" "$@"
