#!/bin/bash
# =============================================================================
# migrate_to_v2.sh — Mjolnir Brain 迁移到 v2.0 分区记忆系统
# Migration script to v2.0 Partitioned Memory System
#
# 功能 / Features:
#   1. 创建 memory/partitions/ 和 memory/archive/ 目录
#   2. 初始化空的 memory-index.json
#   3. 分析现有 MEMORY.md 内容，建议分区方案
#   4. 可选：自动拆分（需用户确认）
#   5. 保留原 MEMORY.md 作为兜底
#   6. 创建 v2.0 多用户目录结构
#
# 用法 / Usage:
#   scripts/migrate_to_v2.sh [--auto] [--workspace /path/to/workspace]
#
# 选项 / Options:
#   --auto          自动模式，跳过确认 / Auto mode, skip confirmations
#   --workspace     指定工作空间路径 / Specify workspace path
#   --dry-run       仅分析，不做修改 / Analyze only, no changes
#
# 依赖 / Dependencies:
#   - bash 4+ (必须 / required)
#   - jq (推荐 / recommended)
# =============================================================================

set -euo pipefail

# --- 配置 / Configuration ---------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 默认目标是模板目录（开发时）或工作空间（部署时）
# Default target: templates dir (dev) or workspace (deployed)
WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-}"
AUTO_MODE=false
DRY_RUN=false

# --- 参数解析 / Argument Parsing ---------------------------------------------

while [[ $# -gt 0 ]]; do
    case "$1" in
        --auto)     AUTO_MODE=true; shift ;;
        --dry-run)  DRY_RUN=true; shift ;;
        --workspace)
            WORKSPACE="$2"; shift 2 ;;
        --help|-h)
            echo "用法 / Usage: migrate_to_v2.sh [--auto] [--workspace /path] [--dry-run]"
            exit 0 ;;
        *)
            echo "未知参数 / Unknown option: $1" >&2
            exit 1 ;;
    esac
done

# 如果未指定工作空间，使用模板目录（开发模式）
# If no workspace specified, use templates dir (dev mode)
if [[ -z "$WORKSPACE" ]]; then
    # 检查是否在部署环境 / Check if in deployed environment
    if [[ -d "${HOME}/.openclaw/workspace/memory" ]]; then
        WORKSPACE="${HOME}/.openclaw/workspace"
    else
        WORKSPACE="${PROJECT_ROOT}/templates"
        echo "⚠️  未指定工作空间，使用模板目录: ${WORKSPACE}"
        echo "⚠️  No workspace specified, using templates dir: ${WORKSPACE}"
    fi
fi

MEMORY_DIR="${WORKSPACE}/memory"
PARTITIONS_DIR="${MEMORY_DIR}/partitions"
ARCHIVE_DIR="${MEMORY_DIR}/archive"
INDEX_FILE="${MEMORY_DIR}/memory-index.json"
MEMORY_MD="${WORKSPACE}/MEMORY.md"

# --- 颜色 / Colors ----------------------------------------------------------

if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' CYAN='' BOLD='' NC=''
fi

err() { echo -e "${RED}ERROR: $*${NC}" >&2; }
ok() { echo -e "${GREEN}✓ $*${NC}"; }
info() { echo -e "${BLUE}$*${NC}"; }
warn() { echo -e "${YELLOW}⚠ $*${NC}"; }

HAS_JQ=false
command -v jq &>/dev/null && HAS_JQ=true

# --- 工具函数 / Utility Functions -------------------------------------------

# 询问用户确认 / Ask for user confirmation
# 自动模式下返回 true / Returns true in auto mode
confirm() {
    local prompt="$1"
    if $AUTO_MODE; then
        echo -e "$prompt [auto: yes]"
        return 0
    fi
    read -rp "$(echo -e "$prompt [y/N] ")" answer
    [[ "$answer" =~ ^[Yy]$ ]]
}

# 获取文件大小 (KB) / Get file size in KB
file_size_kb() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local bytes
        bytes=$(wc -c < "$file")
        echo $(( (bytes + 1023) / 1024 ))
    else
        echo 0
    fi
}

# --- 步骤 1: 创建目录结构 / Step 1: Create directory structure ---------------

step_create_dirs() {
    info "📁 步骤 1: 创建分区目录结构 / Step 1: Creating partition directories..."

    if $DRY_RUN; then
        info "  [dry-run] 会创建 / Would create: ${PARTITIONS_DIR}"
        info "  [dry-run] 会创建 / Would create: ${ARCHIVE_DIR}"
        return
    fi

    mkdir -p "$PARTITIONS_DIR"
    mkdir -p "$ARCHIVE_DIR"

    # 保留多用户目录（如果已存在则跳过）
    # Preserve multi-user dirs if they exist
    local users_dir="${MEMORY_DIR}/users"
    local shared_dir="${MEMORY_DIR}/shared"
    mkdir -p "$users_dir"
    mkdir -p "$shared_dir"/{projects,decisions,playbooks}

    # .gitkeep 文件 / gitkeep files
    touch "${PARTITIONS_DIR}/.gitkeep" 2>/dev/null || true
    touch "${ARCHIVE_DIR}/.gitkeep" 2>/dev/null || true

    ok "目录结构已创建 / Directory structure created"
}

# --- 步骤 2: 初始化索引 / Step 2: Initialize index ---------------------------

step_init_index() {
    info "📋 步骤 2: 初始化 memory-index.json / Step 2: Initializing memory-index.json..."

    if [[ -f "$INDEX_FILE" ]]; then
        warn "索引文件已存在 / Index file already exists: ${INDEX_FILE}"
        if ! confirm "  覆盖 / Overwrite?"; then
            info "  跳过 / Skipped"
            return
        fi
    fi

    if $DRY_RUN; then
        info "  [dry-run] 会创建 / Would create: ${INDEX_FILE}"
        return
    fi

    local now
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if $HAS_JQ; then
        jq -n \
            --arg ver "2.0" \
            --arg ts "$now" \
            '{
                version: $ver,
                updated_at: $ts,
                partitions: [],
                settings: {
                    max_partitions: 20,
                    default_max_size_kb: 20,
                    fallback_to_memory_md: true,
                    max_concurrent_load: 3,
                    auto_update_index: true
                }
            }' > "$INDEX_FILE"
    else
        cat > "$INDEX_FILE" << EOJSON
{
  "version": "2.0",
  "updated_at": "${now}",
  "partitions": [],
  "settings": {
    "max_partitions": 20,
    "default_max_size_kb": 20,
    "fallback_to_memory_md": true,
    "max_concurrent_load": 3,
    "auto_update_index": true
  }
}
EOJSON
    fi

    ok "索引文件已初始化 / Index file initialized"
}

# --- 步骤 3: 分析 MEMORY.md / Step 3: Analyze MEMORY.md ---------------------

step_analyze_memory() {
    info "🔍 步骤 3: 分析现有 MEMORY.md / Step 3: Analyzing existing MEMORY.md..."

    if [[ ! -f "$MEMORY_MD" ]]; then
        info "  未找到 MEMORY.md，跳过分析 / No MEMORY.md found, skipping analysis"
        return
    fi

    local size
    size=$(file_size_kb "$MEMORY_MD")
    info "  文件大小 / File size: ${size}KB"

    # 提取二级标题作为主题 / Extract h2 headers as topics
    echo ""
    echo -e "${BOLD}  📊 检测到的主题 / Detected Topics:${NC}"

    local topic_count=0
    local -a topics=()
    local -a topic_lines=()

    while IFS= read -r line; do
        local topic
        topic=$(echo "$line" | sed 's/^## //')
        topics+=("$topic")
        ((topic_count++))
    done < <(grep '^## ' "$MEMORY_MD" 2>/dev/null || true)

    if [[ $topic_count -eq 0 ]]; then
        info "  未检测到二级标题 / No h2 headers detected"
        info "  建议：手动查看 MEMORY.md 并规划分区"
        info "  Suggestion: Review MEMORY.md manually and plan partitions"
        return
    fi

    # 计算每个主题的大致行数 / Estimate lines per topic
    local total_lines
    total_lines=$(wc -l < "$MEMORY_MD")

    for i in "${!topics[@]}"; do
        local topic="${topics[$i]}"
        # 估算主题下的行数 / Estimate lines under this topic
        local start_line end_line lines_count
        start_line=$(grep -n "^## ${topic}$" "$MEMORY_MD" | head -1 | cut -d: -f1)
        
        if [[ $((i + 1)) -lt $topic_count ]]; then
            local next_topic="${topics[$((i + 1))]}"
            end_line=$(grep -n "^## ${next_topic}$" "$MEMORY_MD" | head -1 | cut -d: -f1)
            lines_count=$(( end_line - start_line ))
        else
            lines_count=$(( total_lines - start_line + 1 ))
        fi

        printf "    ${CYAN}%2d.${NC} %-40s (~%d 行/lines)\n" "$((i + 1))" "$topic" "$lines_count"
    done

    echo ""
    echo -e "${BOLD}  💡 建议分区方案 / Suggested Partition Plan:${NC}"
    echo ""

    # 根据主题生成建议 / Generate suggestions based on topics
    local -A category_map
    category_map=(
        ["创作"]="creative"
        ["故事"]="creative"
        ["IP"]="creative"
        ["角色"]="creative"
        ["运维"]="ops"
        ["服务器"]="ops"
        ["部署"]="ops"
        ["SSH"]="ops"
        ["Docker"]="ops"
        ["项目"]="project"
        ["决策"]="project"
        ["架构"]="project"
        ["计划"]="project"
        ["工具"]="tools"
        ["配置"]="tools"
        ["错误"]="troubleshooting"
        ["教训"]="troubleshooting"
    )

    local suggested_count=0
    for topic in "${topics[@]}"; do
        local category="general"
        for keyword in "${!category_map[@]}"; do
            if echo "$topic" | grep -qi "$keyword"; then
                category="${category_map[$keyword]}"
                break
            fi
        done

        local safe_id
        safe_id=$(echo "$topic" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
        [[ -z "$safe_id" ]] && safe_id="partition-${suggested_count}"

        printf "    建议 / Suggest: ${GREEN}partition_manager.sh create \"%s\" \"%s\" \"%s,%s\"${NC}\n" \
            "$safe_id" "$topic" "$topic" "$category"
        ((suggested_count++))
    done

    echo ""
    info "  共检测到 ${topic_count} 个主题，建议创建 ${suggested_count} 个分区"
    info "  Found ${topic_count} topics, suggesting ${suggested_count} partitions"
}

# --- 步骤 4: 可选自动拆分 / Step 4: Optional auto-split ---------------------

step_auto_split() {
    if [[ ! -f "$MEMORY_MD" ]]; then
        return
    fi

    if $DRY_RUN; then
        info "  [dry-run] 跳过自动拆分 / Skipping auto-split in dry-run mode"
        return
    fi

    echo ""
    if ! confirm "🔪 是否尝试自动拆分 MEMORY.md 到分区？/ Auto-split MEMORY.md into partitions?"; then
        info "  跳过自动拆分 / Skipping auto-split"
        info "  你可以稍后手动使用 partition_manager.sh create 创建分区"
        info "  You can manually create partitions later with partition_manager.sh create"
        return
    fi

    info "📦 开始自动拆分 / Starting auto-split..."

    local current_topic=""
    local current_id=""
    local current_content=""
    local split_count=0
    local partition_mgr="${SCRIPT_DIR}/partition_manager.sh"

    while IFS= read -r line; do
        if [[ "$line" =~ ^##[[:space:]] ]]; then
            # 保存上一个分区 / Save previous partition
            if [[ -n "$current_id" && -n "$current_content" ]]; then
                local partition_file="${PARTITIONS_DIR}/${current_id}.md"
                echo "$current_content" > "$partition_file"
                ((split_count++))
                ok "  拆分 / Split: ${current_id} ← ${current_topic}"
            fi

            # 开始新分区 / Start new partition
            current_topic=$(echo "$line" | sed 's/^## //')
            current_id=$(echo "$current_topic" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
            [[ -z "$current_id" ]] && current_id="partition-${split_count}"
            current_content="# ${current_topic}"$'\n'"<!-- Partition: ${current_id} -->"$'\n'"<!-- Keywords: ${current_topic} -->"$'\n'"<!-- Max Size: 20KB -->"$'\n'
        else
            current_content+="$line"$'\n'
        fi
    done < "$MEMORY_MD"

    # 保存最后一个分区 / Save last partition
    if [[ -n "$current_id" && -n "$current_content" ]]; then
        local partition_file="${PARTITIONS_DIR}/${current_id}.md"
        echo "$current_content" > "$partition_file"
        ((split_count++))
        ok "  拆分 / Split: ${current_id} ← ${current_topic}"
    fi

    ok "自动拆分完成，共 ${split_count} 个分区 / Auto-split done: ${split_count} partitions"
    info "  请运行 partition_manager.sh update-index 更新索引"
    info "  Run partition_manager.sh update-index to refresh the index"
}

# --- 步骤 5: 保留原始 MEMORY.md / Step 5: Preserve original MEMORY.md ------

step_preserve_memory() {
    if [[ ! -f "$MEMORY_MD" ]]; then
        return
    fi

    info "💾 步骤 5: 保留原始 MEMORY.md / Step 5: Preserving original MEMORY.md..."

    if $DRY_RUN; then
        info "  [dry-run] MEMORY.md 将被保留为兜底 / MEMORY.md would be preserved as fallback"
        return
    fi

    # 创建备份 / Create backup
    local backup_file="${MEMORY_DIR}/MEMORY.md.v1-backup.$(date +%Y%m%d)"
    if [[ ! -f "$backup_file" ]]; then
        cp "$MEMORY_MD" "$backup_file"
        ok "备份已创建 / Backup created: ${backup_file}"
    else
        info "  备份已存在 / Backup already exists: ${backup_file}"
    fi

    # MEMORY.md 保留原位，作为 fallback
    info "  MEMORY.md 保留在原位作为兜底 / MEMORY.md kept in place as fallback"
    info "  当 fallback_to_memory_md=true 时，找不到匹配分区会读取 MEMORY.md"
    info "  When fallback_to_memory_md=true, MEMORY.md is read if no partition matches"
}

# --- 总结 / Summary ---------------------------------------------------------

show_summary() {
    echo ""
    echo -e "${BOLD}${GREEN}========================================${NC}"
    echo -e "${BOLD}${GREEN}  ✅ 迁移到 v2.0 完成! / Migration to v2.0 Complete!${NC}"
    echo -e "${BOLD}${GREEN}========================================${NC}"
    echo ""
    info "📂 新目录结构 / New directory structure:"
    info "  ${MEMORY_DIR}/"
    info "  ├── memory-index.json    ← 分区索引 / Partition index"
    info "  ├── partitions/          ← 分区文件 / Partition files"
    info "  │   └── *.md"
    info "  ├── archive/             ← 已归档分区 / Archived partitions"
    info "  ├── users/               ← 多用户目录 / Multi-user dirs"
    info "  └── shared/              ← 共享记忆 / Shared memory"
    echo ""
    info "📋 下一步 / Next steps:"
    info "  1. 查看索引: cat ${INDEX_FILE}"
    info "     View index: cat ${INDEX_FILE}"
    info "  2. 创建分区: scripts/partition_manager.sh create <id> <name> <keywords>"
    info "     Create partition: scripts/partition_manager.sh create <id> <name> <keywords>"
    info "  3. 列出分区: scripts/partition_manager.sh list"
    info "     List partitions: scripts/partition_manager.sh list"
    info "  4. 更新 AGENTS.md 中的会话启动步骤"
    info "     Update session startup steps in AGENTS.md"
    echo ""
    if [[ -f "$MEMORY_MD" ]]; then
        warn "MEMORY.md 已保留作为兜底。当分区系统稳定后，可考虑精简或移除。"
        warn "MEMORY.md preserved as fallback. Consider trimming after partition system is stable."
    fi
    echo ""
}

# --- 主入口 / Main Entry Point -----------------------------------------------

main() {
    echo ""
    echo -e "${BOLD}🧠 Mjolnir Brain — 迁移到 v2.0 分区记忆系统${NC}"
    echo -e "${BOLD}   Migration to v2.0 Partitioned Memory System${NC}"
    echo -e "${BOLD}$(printf '%.0s═' {1..50})${NC}"
    echo ""
    info "工作空间 / Workspace: ${WORKSPACE}"
    info "记忆目录 / Memory dir: ${MEMORY_DIR}"
    $DRY_RUN && warn "DRY-RUN 模式：仅分析，不做修改 / DRY-RUN: analysis only, no changes"
    echo ""

    if ! $AUTO_MODE && ! $DRY_RUN; then
        if ! confirm "开始迁移？/ Start migration?"; then
            info "迁移已取消 / Migration cancelled"
            exit 0
        fi
        echo ""
    fi

    step_create_dirs
    echo ""
    step_init_index
    echo ""
    step_analyze_memory
    step_auto_split
    echo ""
    step_preserve_memory
    
    if ! $DRY_RUN; then
        show_summary
    else
        echo ""
        ok "[dry-run] 分析完成，未做任何修改 / Analysis complete, no changes made"
    fi
}

main "$@"
