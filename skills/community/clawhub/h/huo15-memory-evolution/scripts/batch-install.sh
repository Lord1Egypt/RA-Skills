#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 批量为所有动态 Agent 安装技能
#
# 用法: ./batch-install.sh
#
# 功能:
#   1. 为所有动态 agent 拷贝 huo15-memory-evolution 技能
#   2. 确保 memory/ 目录结构存在（四类分类）
#   3. 复制 HEARTBEAT.md 到每个 agent（触发 session-state 写侧）
#
# 注意：不再依赖第三方技能（fluid-memory/context-optimizer/
#       context-persistence/proactive-agent/clever-compact），
#       所有功能均已自主实现。
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
MAIN_WORKSPACE="$HOME/.openclaw/workspace"
SKILL_NAME="huo15-memory-evolution"
OPENCLAW_DIR="$HOME/.openclaw"
TIMESTAMP=$(date +%Y-%m-%d)

echo "🚀 huo15-memory-evolution 批量安装 v2.0"
echo "================================"
echo "   时间: ${TIMESTAMP}"
echo ""

#===========================================
# 步骤 1: 发现所有动态 agent
#===========================================
echo "🔍 步骤1: 发现动态 Agent..."

WORKSPACES=$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace-wecom-*" 2>/dev/null | sort)
WORKSPACE_COUNT=$(echo "$WORKSPACES" | wc -l | tr -d ' ')
echo "   ✓ 发现 ${WORKSPACE_COUNT} 个动态 Agent"
echo ""

#===========================================
# 核心技能列表（每个 agent 都要装）
# 注意：全部自主实现，不再依赖第三方技能
#===========================================
CORE_SKILLS=(
    "huo15-memory-evolution"
)

#===========================================
# 步骤 2: 为每个 agent 安装技能和配置
#===========================================
echo "📦 步骤2: 安装核心技能..."

INSTALLED_SKILLS=0
MEMORY_INIT_COUNT=0
HEARTBEAT_COUNT=0

for ws in $WORKSPACES; do
    ws_name=$(basename "$ws")
    skills_dir="$ws/skills"
    memory_dir="$ws/memory"

    echo "   → $ws_name"

    # 1. 确保 skills 目录存在
    mkdir -p "$skills_dir"

    # 2. 安装核心技能
    for skill in "${CORE_SKILLS[@]}"; do
        src_dir="$MAIN_WORKSPACE/skills/$skill"
        if [ -d "$src_dir" ]; then
            if [ ! -d "$skills_dir/$skill" ]; then
                cp -r "$src_dir" "$skills_dir/$skill"
                echo "     ✅ $skill 已安装"
            else
                # 更新：删除旧版本，复制新版本
                rm -rf "$skills_dir/$skill"
                cp -r "$src_dir" "$skills_dir/$skill"
                echo "     🔄 $skill 已更新"
            fi
            INSTALLED_SKILLS=$((INSTALLED_SKILLS + 1))
        else
            # 如果主workspace没有，尝试从已有agent复制
            existing_src="$OPENCLAW_DIR/workspace-wecom-default-dm-xun/skills/$skill"
            if [ -d "$existing_src" ]; then
                rm -rf "$skills_dir/$skill"
                cp -r "$existing_src" "$skills_dir/$skill"
                echo "     📦 $skill (从xun复制)"
            else
                echo "     ⚠️  $skill 源文件不存在，跳过"
            fi
        fi
    done

    # 3. 复制 HEARTBEAT.md
    if [ -f "$MAIN_WORKSPACE/HEARTBEAT.md" ]; then
        cp "$MAIN_WORKSPACE/HEARTBEAT.md" "$ws/HEARTBEAT.md"
        echo "     ✅ HEARTBEAT.md 已配置"
        HEARTBEAT_COUNT=$((HEARTBEAT_COUNT + 1))
    fi

    # 4. 确保 memory/ 目录结构存在（四类分类）
    if [ ! -d "$memory_dir" ]; then
        mkdir -p "$memory_dir/user"
        mkdir -p "$memory_dir/feedback"
        mkdir -p "$memory_dir/project"
        mkdir -p "$memory_dir/reference"
        mkdir -p "$memory_dir/archive"
        mkdir -p "$memory_dir/activity"
        mkdir -p "$memory_dir/project/wal"

        # 创建 index.json
        cat << EOF > "$memory_dir/index.json"
{
  "version": "2.0",
  "installedAt": "${TIMESTAMP}",
  "agentId": "${ws_name}",
  "entries": []
}
EOF
        echo "     ✅ memory/ 目录结构已创建"
        MEMORY_INIT_COUNT=$((MEMORY_INIT_COUNT + 1))
    else
        echo "     ⚠️  memory/ 已存在"
    fi

    echo ""
done

#===========================================
# 步骤 3: 统计报告
#===========================================
echo "================================"
echo "📊 安装结果汇总"
echo "================================"
echo "   处理动态 Agent: ${WORKSPACE_COUNT}"
echo "   技能安装次数: ${INSTALLED_SKILLS}"
echo "   HEARTBEAT 配置: ${HEARTBEAT_COUNT}"
echo "   记忆目录初始化: ${MEMORY_INIT_COUNT}"
echo ""

#===========================================
# 步骤 4: 验证安装
#===========================================
echo "🔍 步骤4: 验证安装..."

CHECK_AGENTS=(
    "workspace-wecom-default-dm-xun"
    "workspace-wecom-default-dm-panduoduo"
    "workspace-wecom-default-group-wrgzumeqaaczxscaws2mzhbhulsf8upq"
)

for ws_name in "${CHECK_AGENTS[@]}"; do
    ws="$OPENCLAW_DIR/$ws_name"
    if [ -d "$ws" ]; then
        echo "   → $ws_name"
        for skill in "${CORE_SKILLS[@]}"; do
            if [ -d "$ws/skills/$skill" ]; then
                echo "     ✅ $skill"
            else
                echo "     ❌ $skill (缺失)"
            fi
        done
        if [ -f "$ws/HEARTBEAT.md" ]; then
            echo "     ✅ HEARTBEAT.md"
        else
            echo "     ❌ HEARTBEAT.md (缺失)"
        fi
    fi
done

echo ""
echo "✅ 批量安装完成!"
echo ""
echo "📋 安装的技能栈:"
echo "   🧠 huo15-memory-evolution - 四类记忆分类 + Dream Agent"
echo "   💧 fluid-memory - 艾宾浩斯遗忘曲线"
echo "   🗜️  context-optimizer - 上下文压缩优化"
echo "   🔗 context-persistence - 跨会话持久化"
echo "   🦞 proactive-agent - 主动行为 + WAL Protocol"
echo ""
echo "📋 下一步:"
echo "   1. 重启 gateway: openclaw gateway restart"
echo "   2. 验证: OC_AGENT_ID=wecom-default-dm-xun ./scripts/verify.sh"
