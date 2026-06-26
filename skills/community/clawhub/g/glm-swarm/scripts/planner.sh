#!/bin/bash
# glm-swarm planner: 작업 분해 + scratchpad 초기화
# Usage: planner.sh <task-id>
# task-id가 없으면 자동 생성

set -e

TASK_ID="${1:-swarm-$(date +%s)}"
SWARM_DIR="/tmp/swarm/${TASK_ID}"

# 작업 디렉토리 생성
mkdir -p "${SWARM_DIR}"

# Shared Scratchpad 초기화
cat > "${SWARM_DIR}/shared.md" << 'EOF'
# Shared Scratchpad
# 각 worker는 자기 섹션에만 쓰기

EOF

# Plan 파일 (Planner가 채울 템플릿)
cat > "${SWARM_DIR}/plan.json" << EOF
{
  "task_id": "${TASK_ID}",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "goal": "",
  "tasks": [],
  "aggregation": "concat",
  "status": "planning"
}
EOF

echo "${SWARM_DIR}"
