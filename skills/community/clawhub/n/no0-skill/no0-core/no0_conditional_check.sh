#!/bin/bash
# No.0 Skill 条件检查脚本
# 检查是否有新记录或文件不一致，否则输出"NO_REPLY"

cd "$(dirname "$0")"

# 运行静默检查，捕获输出
output=$(python3 scripts/skill_launcher.py status --quiet 2>&1)
exit_code=$?

# 如果有输出（新记录或文件不一致），输出状态
# 如果静默退出（exit_code=0且无输出），输出NO_REPLY
if [ $exit_code -eq 0 ] && [ -z "$output" ]; then
    # 完全正常，无新记录且无文件不一致
    echo "NO_REPLY"
else
    # 有新记录或文件不一致，输出状态
    if [ -n "$output" ]; then
        echo "$output"
    else
        # 有退出码但无输出（异常情况）
        echo "No.0 Skill 状态检查异常，退出码: $exit_code"
    fi
fi
