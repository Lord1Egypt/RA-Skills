#!/bin/bash
# 初始化项目脚本

if [ -z "$1" ]; then
  echo "用法: $0 <project-name>"
  exit 1
fi

PROJECT_NAME="$1"
BASE_DIR="/root/.openclaw"
PROJECT_DIR="$BASE_DIR/projects/$PROJECT_NAME"
TEMPLATE_DIR="$BASE_DIR/skills/multi-agent-memory/templates"

echo "=== 初始化项目: $PROJECT_NAME ==="

# 1. 创建目录结构
echo "创建目录结构..."
mkdir -p "$PROJECT_DIR"/{status,weekly,handoffs,docs/{requirements,specs},logs,milestones}

# 2. 创建 context.md
echo "创建 context.md..."
DATE=$(date +'%Y-%m-%d')
sed "s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{DATE}/$DATE/g" \
  "$TEMPLATE_DIR/context.md.template" > "$PROJECT_DIR/context.md"

# 3. 创建 todos.md
echo "创建 todos.md..."
sed "s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{DATE}/$DATE/g" \
  "$TEMPLATE_DIR/todos.md.template" > "$PROJECT_DIR/todos.md"

# 4. 创建 milestones.md
echo "创建 milestones.md..."
DATE_TIME=$(date +'%Y-%m-%d %H:%M')
sed "s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{DATE} {TIME}/$DATE_TIME/g" \
  "$TEMPLATE_DIR/milestones.md.template" > "$PROJECT_DIR/milestones/milestones.md"

# 5. 创建每个 agent 的 status 文件
echo "创建 agent status 文件..."
for agent in maker vibe commander killjoy main; do
  AGENT_UPPER=$(echo "$agent" | tr '[:lower:]' '[:upper:]')
  sed "s/{AGENT}/$AGENT_UPPER/g; s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{DATE} {TIME}/$DATE_TIME/g" \
    "$TEMPLATE_DIR/status.md.template" > "$PROJECT_DIR/status/$agent.md"
done

# 6. 创建知识库（如果不存在）
echo "检查知识库..."
mkdir -p "$BASE_DIR/knowledge"/{decisions,patterns,glossary,index}
touch "$BASE_DIR/knowledge/decisions/decisions.md"
touch "$BASE_DIR/knowledge/patterns/patterns.md"
touch "$BASE_DIR/knowledge/glossary/glossary.md"
touch "$BASE_DIR/knowledge/index/keywords.txt"

# 7. 创建归档目录
echo "创建归档目录..."
mkdir -p "$BASE_DIR/archive/$PROJECT_NAME"

echo "✅ 项目初始化完成: $PROJECT_NAME"
echo ""
echo "下一步："
echo "1. 编辑 $PROJECT_DIR/context.md 填写项目背景"
echo "2. 编辑 $PROJECT_DIR/todos.md 添加初始任务"
echo "3. 编辑 $PROJECT_DIR/milestones/milestones.md 设置里程碑"
echo "4. 设置当前项目: echo '$PROJECT_NAME' > ~/workspace-<agent>/current-project.txt"
