#!/bin/bash
# batch-create-rescue-instances.sh - 批量创建 OpenClaw 救援 Gateway 实例
# 用法：./batch-create-rescue-instances.sh [起始编号] [实例数量] [起始端口]

set -e

START_NUM=${1:-1}
COUNT=${2:-1}
START_PORT=${3:-19001}

echo "=== 批量创建 $COUNT 个救援实例 ==="
echo "起始编号：$START_NUM"
echo "起始端口：$START_PORT"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for i in $(seq 0 $((COUNT - 1))); do
  INSTANCE_NUM=$((START_NUM + i))
  PORT=$((START_PORT + i * 1000))
  
  echo "--- 创建实例 $i/$COUNT ---"
  "$SCRIPT_DIR/create-rescue-instance.sh" "$INSTANCE_NUM" "$PORT"
  echo ""
done

echo "=== 批量创建完成 ==="
echo ""
echo "所有实例状态:"
launchctl list | grep "openclaw.gateway-rescue" || echo "无救援实例运行"
