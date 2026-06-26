#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 迁移脚本
#
# 用法: ./migrate.sh [--dry-run]
#
# 功能: 将原有 HOT/WARM/COLD 架构迁移到新的四类分类体系
#       并为每个动态 agent 创建独立的记忆空间
#
# 选项:
#   --dry-run  仅分析，不执行（预览迁移效果）
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE_DIR/memory"
OPENCLAW_DIR="$HOME/.openclaw"
TIMESTAMP=$(date +%Y-%m-%d)
DRY_RUN=false

if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
    echo "🔍 预演模式：不执行实际更改，仅分析"
    echo ""
fi

echo "🚀 huo15-memory-evolution 迁移"
echo "================================"
echo "   时间: ${TIMESTAMP}"
echo "   模式: $([ "$DRY_RUN" == "true" ] && echo "预演(dry-run)" || echo "执行")"
echo ""

#===========================================
# 步骤 1: 创建新的目录结构
#===========================================
echo "📁 步骤1: 创建新目录结构..."

NEW_TYPES=("user" "feedback" "project" "reference" "archive")

for type in "${NEW_TYPES[@]}"; do
    if [ "$DRY_RUN" == "false" ]; then
        mkdir -p "$MEMORY_DIR/$type"
        mkdir -p "$MEMORY_DIR/activity"  # 保留原有 activity 分层，标记为 legacy
    fi
done
echo "   ✓ 目录结构: memory/{user,feedback,project,reference,archive,activity}"

#===========================================
# 步骤 2: 创建 index.json
#===========================================
echo ""
echo "📋 步骤2: 创建 index.json..."

INDEX_JSON="$MEMORY_DIR/index.json"
if [ "$DRY_RUN" == "false" ]; then
    cat << 'EOF' > "$INDEX_JSON"
{
  "version": "1.0",
  "migratedAt": "@TIMESTAMP@",
  "migrationFrom": "HOT/WARM/COLD",
  "entries": []
}
EOF
    sed -i '' "s/@TIMESTAMP@/${TIMESTAMP}/" "$INDEX_JSON"
fi
echo "   ✓ $INDEX_JSON"

#===========================================
# 步骤 3: 生成新的 MEMORY.md 索引
#===========================================
echo ""
echo "📝 步骤3: 生成新 MEMORY.md 索引..."

NEW_MEMORY_MD="$WORKSPACE_DIR/MEMORY.md"
if [ "$DRY_RUN" == "false" ]; then
    cat << 'EOF' > "$NEW_MEMORY_MD"
# Memory Index

*最后更新: @TIMESTAMP@ | 最多 200 行*

## user
（用户偏好和习惯）

## feedback
（纠正和确认偏好）

## project
（项目上下文和进展）

## reference
（外部系统指针）

---

*此文件为索引，内容在 memory/{type}/ 目录下*
EOF
    sed -i '' "s/@TIMESTAMP@/${TIMESTAMP}/" "$NEW_MEMORY_MD"
fi
echo "   ✓ 新 MEMORY.md 索引已创建"

#===========================================
# 步骤 4: 迁移原有 hot/warm/cold 内容
#===========================================
echo ""
echo "🔄 步骤4: 迁移原有记忆到新分类..."

# 读取原有 hot memory
HOT_FILE="$MEMORY_DIR/hot/HOT_MEMORY.md"
WARM_FILE="$MEMORY_DIR/warm/WARM_MEMORY.md"

if [ -f "$HOT_FILE" ]; then
    echo "   → 发现 hot memory: $HOT_FILE"
    if [ "$DRY_RUN" == "false" ]; then
        # 简单处理：将 hot 内容标记为 project 类型
        cat << EOF > "$MEMORY_DIR/project/hot-migrated.md"
---
name: hot-memory-migrated
type: project
created: ${TIMESTAMP}
updated: ${TIMESTAMP}
migratedFrom: hot/
---

# 从 HOT 迁移的记忆
$(cat "$HOT_FILE")
EOF
        fi
    echo "   ✓ hot → project/hot-migrated.md"
fi

if [ -f "$WARM_FILE" ]; then
    echo "   → 发现 warm memory: $WARM_FILE"
    if [ "$DRY_RUN" == "false" ]; then
        cat << EOF > "$MEMORY_DIR/warm/warm-migrated.md"
---
name: warm-memory-migrated
type: feedback
created: ${TIMESTAMP}
updated: ${TIMESTAMP}
migratedFrom: warm/
---

# 从 WARM 迁移的记忆
$(cat "$WARM_FILE")
EOF
        fi
    echo "   ✓ warm → feedback/warm-migrated.md"
fi

#===========================================
# 步骤 5: 为动态 Agent 创建独立空间
#===========================================
echo ""
echo "🔒 步骤5: 隔离动态 Agent 记忆..."

WORKSPACES=$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace-wecom-*" 2>/dev/null | sort)

SENSITIVE_PATTERNS=(
    "工商银行"
    "建设银行"
    "支付宝"
    "3803021019200476891"
    "37150198541000001436"
    "zhaobod1@126.com"
    "OLD_SYSTEM"
    "XINQiantu"
    "645612509@qq.com"
    "postmaster@huo15.com"
    "18554898815"
)

AGENT_COUNT=0
for ws in $WORKSPACES; do
    ws_name=$(basename "$ws")
    AGENT_COUNT=$((AGENT_COUNT + 1))
    
    echo "   → 处理: $ws_name"
    
    if [ "$DRY_RUN" == "false" ]; then
        # 创建新的 memory 目录结构
        mkdir -p "$ws/memory"/{user,feedback,project,reference,archive}
        
        # 创建 index.json
        cat << EOF > "$ws/memory/index.json"
{
  "version": "1.0",
  "migratedAt": "${TIMESTAMP}",
  "agentId": "${ws_name}",
  "entries": []
}
EOF
        
        # 替换为干净模板
        cat << 'TEMPLATE' > "$ws/MEMORY.md"
# Memory Index

*最后更新: @TIMESTAMP@*

## user
（用户偏好和习惯）

## feedback
（纠正和确认偏好）

## project
（项目上下文和进展）

## reference
（外部系统指针）

---

*此文件为索引，内容在 memory/{type}/ 目录下*
TEMPLATE
        sed -i '' "s/@TIMESTAMP@/${TIMESTAMP}/" "$ws/MEMORY.md"
        
        # 清除敏感信息
        for pattern in "${SENSITIVE_PATTERNS[@]}"; do
            if grep -q "$pattern" "$ws/MEMORY.md" 2>/dev/null; then
                echo "   ⚠️  发现敏感信息: $pattern → 已清除"
                cat << 'TEMPLATE' > "$ws/MEMORY.md"
# Memory Index

*最后更新: @TIMESTAMP@*

## user
（用户偏好和习惯）

## feedback
（纠正和确认偏好）

## project
（项目上下文和进展）

## reference
（外部系统指针）

---

*此文件为索引，内容在 memory/{type}/ 目录下*
TEMPLATE
                sed -i '' "s/@TIMESTAMP@/${TIMESTAMP}/" "$ws/MEMORY.md"
            fi
        done
    fi
done

echo "   ✓ 处理了 ${AGENT_COUNT} 个动态 Agent workspaces"

#===========================================
# 步骤 6: 生成迁移报告
#===========================================
echo ""
echo "📊 步骤6: 生成迁移报告..."

REPORT_FILE="$SKILL_DIR/MIGRATION-REPORT-${TIMESTAMP}.md"

if [ "$DRY_RUN" == "false" ]; then
    cat << EOF > "$REPORT_FILE"
# 记忆系统迁移报告
生成时间: ${TIMESTAMP}

## 迁移概览

| 项目 | 数值 |
|------|------|
| 迁移时间 | ${TIMESTAMP} |
| 模式 | $([ "$DRY_RUN" == "true" ] && echo "预演" || echo "执行") |
| 处理动态 Agent 数 | ${AGENT_COUNT} |

## 目录结构变更

### 主 Workspace
- 旧结构: memory/{hot/,warm/,cold/}
- 新结构: memory/{user/,feedback/,project/,reference/,archive/,activity/}

### 动态 Agent Workspaces
每个动态 agent 现在拥有独立的 memory/ 结构：
- memory/user/
- memory/feedback/
- memory/project/
- memory/reference/
- memory/archive/
- memory/index.json

## 敏感信息清理

已检查并清除以下敏感信息跨 agent 复制：
$(printf '  - %s\n' "${SENSITIVE_PATTERNS[@]}")

## 验证步骤

运行以下命令验证迁移结果：
```bash
./verify.sh
```

## 如需回滚

```bash
./rollback.sh <snapshot-tarball>
```
EOF
fi

echo "   ✓ 报告: MIGRATION-REPORT-${TIMESTAMP}.md"

#===========================================
# 完成
#===========================================
echo ""
if [ "$DRY_RUN" == "true" ]; then
    echo "🔍 预演完成，未执行实际更改"
    echo ""
    echo "如确认无误，执行实际迁移:"
    echo "   ./migrate.sh"
else
    echo "✅ 迁移完成!"
    echo ""
    echo "📋 下一步:"
    echo "   1. 审阅迁移报告: MIGRATION-REPORT-${TIMESTAMP}.md"
    echo "   2. 运行验证: ./verify.sh"
    echo ""
    echo "⚠️  重要: 建议先验证，确认无误后再开始使用新结构"
fi
