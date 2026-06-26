#!/bin/bash
# hermes-agi-supervisor: 任务分解脚本
# 用法: ./decompose.sh "<用户指令>"

USER_INPUT="$1"
TASK_FILE="$HOME/.hermes/tasks/$(date +%s).json"
METADATA_FILE="$HOME/.hermes/metadata.json"

mkdir -p "$HOME/.hermes/tasks"

# 生成任务ID
TASK_ID="task_$(date +%s)"
CREATED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# 构建初始任务JSON
cat > "$TASK_FILE" << EOF
{
  "id": "$TASK_ID",
  "raw_input": "$USER_INPUT",
  "status": "pending_decomposition",
  "created_at": "$CREATED_AT",
  "subtasks": [],
  "score": 0,
  "completed": 0,
  "failed": 0
}
EOF

# 更新索引
mkdir -p "$HOME/.hermes"
if [ ! -f "$METADATA_FILE" ]; then
  echo '{"tasks": []}' > "$METADATA_FILE"
fi

node -e "
const fs = require('fs');
const meta = JSON.parse(fs.readFileSync('$METADATA_FILE', 'utf8'));
meta.tasks.unshift({ id: '$TASK_ID', file: '$TASK_FILE', created: '$CREATED_AT' });
meta.tasks = meta.tasks.slice(0, 50);
fs.writeFileSync('$METADATA_FILE', JSON.stringify(meta, null, 2));
"

echo "TASK_ID=$TASK_ID"
echo "TASK_FILE=$TASK_FILE"
