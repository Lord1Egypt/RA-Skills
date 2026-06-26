#!/bin/bash
# 每日检查脚本

if [ -z "$1" ]; then
  echo "用法: $0 <project-name>"
  exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="/root/.openclaw/projects/$PROJECT_NAME"
ERRORS=0
WARNINGS=0

echo "=== 每日检查: $PROJECT_NAME ==="
echo ""

# 1. 检查项目目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ 项目目录不存在: $PROJECT_DIR"
  exit 1
fi

# 2. 检查核心文件是否存在
echo "检查核心文件..."
for file in context.md todos.md milestones/milestones.md; do
  if [ ! -f "$PROJECT_DIR/$file" ]; then
    echo "❌ 缺少文件: $file"
    ERRORS=$((ERRORS+1))
  fi
done

# 3. 检查所有 agent 的 status 文件
echo ""
echo "检查 agent status..."
for agent in maker vibe commander killjoy main; do
  STATUS_FILE="$PROJECT_DIR/status/$agent.md"
  if [ ! -f "$STATUS_FILE" ]; then
    echo "❌ $agent 的 status 文件不存在"
    ERRORS=$((ERRORS+1))
  else
    # 检查是否今天更新过
    LAST_UPDATE=$(stat -c %Y "$STATUS_FILE" 2>/dev/null || stat -f %m "$STATUS_FILE" 2>/dev/null)
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_UPDATE))
    HOURS=$((DIFF / 3600))
    
    if [ $DIFF -gt 86400 ]; then  # 超过 24 小时
      echo "⚠️  $agent 的 status 超过 ${HOURS} 小时未更新"
      WARNINGS=$((WARNINGS+1))
    else
      echo "✅ $agent status 正常（${HOURS} 小时前更新）"
    fi
  fi
done

# 4. 检查文档命名规范
echo ""
echo "检查文档命名规范..."
INVALID_NAMES=0
for dir in logs docs/requirements docs/specs; do
  if [ -d "$PROJECT_DIR/$dir" ]; then
    while IFS= read -r file; do
      basename=$(basename "$file")
      if ! [[ $basename =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}- ]]; then
        echo "⚠️  文件命名不符合规范: $file"
        INVALID_NAMES=$((INVALID_NAMES+1))
      fi
    done < <(find "$PROJECT_DIR/$dir" -name "*.md" 2>/dev/null)
  fi
done

if [ $INVALID_NAMES -eq 0 ]; then
  echo "✅ 所有文档命名符合规范"
else
  echo "⚠️  发现 $INVALID_NAMES 个文件命名不符合规范"
  WARNINGS=$((WARNINGS+1))
fi

# 5. 检查知识库
echo ""
echo "检查知识库..."
KNOWLEDGE_DIR="/root/.openclaw/knowledge"
for file in decisions/decisions.md patterns/patterns.md glossary/glossary.md; do
  if [ ! -f "$KNOWLEDGE_DIR/$file" ]; then
    echo "⚠️  知识库文件不存在: $file"
    WARNINGS=$((WARNINGS+1))
  fi
done

# 6. 总结
echo ""
echo "=== 检查结果 ==="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo "✅ 所有检查通过"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo "⚠️  发现 $WARNINGS 个警告"
  exit 0
else
  echo "❌ 发现 $ERRORS 个错误，$WARNINGS 个警告"
  exit 1
fi
