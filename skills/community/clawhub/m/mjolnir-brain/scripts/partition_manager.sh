#!/bin/bash
# =============================================================================
# partition_manager.sh — Mjolnir Brain 分区记忆管理器
# Partition Manager for Mjolnir Brain's Partitioned Memory System (v2.0)
#
# 功能 / Features:
#   create <id> <name> <keywords>  — 创建新分区 / Create a new partition
#   delete <id>                     — 归档分区 / Archive a partition
#   list                            — 列出所有分区 / List all partitions
#   update-index                    — 更新索引 / Update index metadata
#   check-capacity                  — 容量检查 / Check capacity warnings
#   search <keyword>                — 搜索分区 / Search partitions by keyword
#
# 依赖 / Dependencies:
#   - bash 4+ (必须 / required)
#   - jq (推荐，可降级到 grep/sed / recommended, fallback to grep/sed)
#
# 环境变量 / Environment Variables:
#   MJOLNIR_BRAIN_WORKSPACE — 工作空间路径 (默认: $HOME/.openclaw/workspace)
#
# 用法 / Usage:
#   scripts/partition_manager.sh <command> [args...]
#   MJOLNIR_BRAIN_WORKSPACE=/path/to/ws scripts/partition_manager.sh list
# =============================================================================

set -euo pipefail

# --- 配置 / Configuration ---------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 工作空间路径：优先环境变量，其次默认路径
# Workspace path: env var takes priority, then default
WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-${HOME}/.openclaw/workspace}"

MEMORY_DIR="${WORKSPACE}/memory"
PARTITIONS_DIR="${MEMORY_DIR}/partitions"
ARCHIVE_DIR="${MEMORY_DIR}/archive"
INDEX_FILE="${MEMORY_DIR}/memory-index.json"

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

# --- 工具函数 / Utility Functions -------------------------------------------

# 打印错误信息 / Print error message
err() { echo -e "${RED}ERROR: $*${NC}" >&2; }

# 打印成功信息 / Print success message
ok() { echo -e "${GREEN}✓ $*${NC}"; }

# 打印信息 / Print info message
info() { echo -e "${BLUE}$*${NC}"; }

# 打印警告 / Print warning message
warn() { echo -e "${YELLOW}WARNING: $*${NC}"; }

# 检测 jq 是否可用 / Check if jq is available
HAS_JQ=false
if command -v jq &>/dev/null; then
    HAS_JQ=true
fi

# 确保目录存在 / Ensure required directories exist
ensure_dirs() {
    mkdir -p "$PARTITIONS_DIR" "$ARCHIVE_DIR"
}

# 确保索引文件存在 / Ensure index file exists
# 如果不存在则从模板创建 / Creates from template if missing
ensure_index() {
    if [[ ! -f "$INDEX_FILE" ]]; then
        info "索引文件不存在，正在初始化... / Index file not found, initializing..."
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
        ok "索引文件已初始化 / Index file initialized: $INDEX_FILE"
    fi
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

# 获取当前时间戳 / Get current UTC timestamp
now_ts() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# 读取索引中的分区数量 / Read partition count from index
partition_count() {
    if $HAS_JQ; then
        jq '.partitions | length' "$INDEX_FILE"
    else
        grep -c '"id"' "$INDEX_FILE" 2>/dev/null || echo 0
    fi
}

# 读取索引中最大分区数 / Read max partitions from index settings
max_partitions() {
    if $HAS_JQ; then
        jq '.settings.max_partitions // 20' "$INDEX_FILE"
    else
        grep -o '"max_partitions":[[:space:]]*[0-9]*' "$INDEX_FILE" | grep -o '[0-9]*' || echo 20
    fi
}

# 读取默认最大大小 / Read default max size
default_max_size_kb() {
    if $HAS_JQ; then
        jq '.settings.default_max_size_kb // 20' "$INDEX_FILE"
    else
        grep -o '"default_max_size_kb":[[:space:]]*[0-9]*' "$INDEX_FILE" | grep -o '[0-9]*' || echo 20
    fi
}

# 检查分区 ID 是否已存在 / Check if partition ID already exists
partition_exists() {
    local id="$1"
    if $HAS_JQ; then
        local count
        count=$(jq --arg id "$id" '[.partitions[] | select(.id == $id)] | length' "$INDEX_FILE")
        [[ "$count" -gt 0 ]]
    else
        grep -q "\"id\":[[:space:]]*\"${id}\"" "$INDEX_FILE"
    fi
}

# --- 命令实现 / Command Implementations --------------------------------------

# 创建新分区 / Create a new partition
# 用法 / Usage: cmd_create <id> <name> <keywords_comma_separated>
cmd_create() {
    local id="${1:-}"
    local name="${2:-}"
    local keywords="${3:-}"

    if [[ -z "$id" || -z "$name" ]]; then
        err "用法 / Usage: partition_manager.sh create <id> <name> [keywords]"
        err "  示例 / Example: partition_manager.sh create my-project \"My Project\" \"项目,决策,project\""
        exit 1
    fi

    ensure_dirs
    ensure_index

    # 检查 ID 格式 / Validate ID format (alphanumeric + hyphens)
    if [[ ! "$id" =~ ^[a-zA-Z0-9][a-zA-Z0-9_-]*$ ]]; then
        err "无效的分区 ID: '$id' (仅允许字母、数字、连字符、下划线)"
        err "Invalid partition ID: '$id' (only alphanumeric, hyphens, underscores)"
        exit 1
    fi

    # 检查是否已存在 / Check for duplicates
    if partition_exists "$id"; then
        err "分区 '$id' 已存在 / Partition '$id' already exists"
        exit 1
    fi

    # 检查分区数量上限 / Check partition count limit
    local current_count max_count
    current_count=$(partition_count)
    max_count=$(max_partitions)
    if [[ "$current_count" -ge "$max_count" ]]; then
        err "已达分区上限 ($max_count)，请先删除或归档旧分区"
        err "Partition limit reached ($max_count). Delete or archive old partitions first."
        exit 1
    fi

    # 创建分区文件 / Create partition file
    local partition_file="${PARTITIONS_DIR}/${id}.md"
    local default_max
    default_max=$(default_max_size_kb)

    cat > "$partition_file" << EOF
# ${name}
<!-- Partition: ${id} -->
<!-- Keywords: ${keywords} -->
<!-- Max Size: ${default_max}KB -->
<!-- Description: ${name} -->

## 📝 Notes

(在此记录 ${name} 相关内容 / Record ${name} related content here)

---
*Last updated: $(date +%Y-%m-%d)*
EOF

    # 更新索引 / Update index
    local ts file_size_val
    ts=$(now_ts)
    file_size_val=$(file_size_kb "$partition_file")

    # 将 keywords 字符串转为 JSON 数组 / Convert keywords string to JSON array
    if $HAS_JQ; then
        local kw_json
        kw_json=$(echo "$keywords" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | jq -R . | jq -s .)

        local tmp_file="${INDEX_FILE}.tmp.$$"
        jq --arg id "$id" \
           --arg name "$name" \
           --argjson kw "$kw_json" \
           --arg file "partitions/${id}.md" \
           --arg ts "$ts" \
           --argjson size "$file_size_val" \
           --argjson max_size "$default_max" \
           '.partitions += [{
               id: $id,
               name: $name,
               keywords: $kw,
               file: $file,
               size_kb: $size,
               max_size_kb: $max_size,
               created_at: $ts,
               updated_at: $ts
           }] | .updated_at = $ts' \
           "$INDEX_FILE" > "$tmp_file" && mv "$tmp_file" "$INDEX_FILE"
    else
        # 降级方案：直接用 sed 在 partitions 数组末尾插入
        # Fallback: use sed to insert at end of partitions array
        local kw_json_str=""
        IFS=',' read -ra kw_arr <<< "$keywords"
        for i in "${!kw_arr[@]}"; do
            local kw
            kw=$(echo "${kw_arr[$i]}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            [[ $i -gt 0 ]] && kw_json_str+=", "
            kw_json_str+="\"${kw}\""
        done
        
        local new_entry="    {\"id\": \"${id}\", \"name\": \"${name}\", \"keywords\": [${kw_json_str}], \"file\": \"partitions/${id}.md\", \"size_kb\": ${file_size_val}, \"max_size_kb\": ${default_max}, \"created_at\": \"${ts}\", \"updated_at\": \"${ts}\"}"
        
        # 检查 partitions 数组是否为空 / Check if partitions array is empty
        if grep -q '"partitions":[[:space:]]*\[\]' "$INDEX_FILE"; then
            sed -i "s|\"partitions\":[[:space:]]*\[\]|\"partitions\": [\n${new_entry}\n  ]|" "$INDEX_FILE"
        else
            # 在最后一个 } 或 ] 之前插入 / Insert before last closing bracket
            sed -i "/\"partitions\":/,/\]/ s|\]|,\n${new_entry}\n  ]|" "$INDEX_FILE"
        fi
        # 更新 updated_at / Update timestamp
        sed -i "s|\"updated_at\":[[:space:]]*\"[^\"]*\"|\"updated_at\": \"${ts}\"|" "$INDEX_FILE"
    fi

    ok "分区已创建 / Partition created: ${id}"
    info "  文件 / File: ${partition_file}"
    info "  名称 / Name: ${name}"
    info "  关键词 / Keywords: ${keywords}"
}

# 删除（归档）分区 / Delete (archive) a partition
# 用法 / Usage: cmd_delete <id>
cmd_delete() {
    local id="${1:-}"

    if [[ -z "$id" ]]; then
        err "用法 / Usage: partition_manager.sh delete <id>"
        exit 1
    fi

    ensure_dirs
    ensure_index

    # 检查分区是否存在 / Check if partition exists
    if ! partition_exists "$id"; then
        err "分区 '$id' 不存在 / Partition '$id' not found"
        exit 1
    fi

    local partition_file="${PARTITIONS_DIR}/${id}.md"

    # 移动文件到归档目录 / Move file to archive
    if [[ -f "$partition_file" ]]; then
        local archive_name="${id}_$(date +%Y%m%d_%H%M%S).md"
        mv "$partition_file" "${ARCHIVE_DIR}/${archive_name}"
        ok "文件已归档 / File archived: ${ARCHIVE_DIR}/${archive_name}"
    else
        warn "分区文件不存在 / Partition file not found: ${partition_file}"
    fi

    # 从索引中移除 / Remove from index
    local ts
    ts=$(now_ts)
    if $HAS_JQ; then
        local tmp_file="${INDEX_FILE}.tmp.$$"
        jq --arg id "$id" --arg ts "$ts" \
           '.partitions = [.partitions[] | select(.id != $id)] | .updated_at = $ts' \
           "$INDEX_FILE" > "$tmp_file" && mv "$tmp_file" "$INDEX_FILE"
    else
        # 降级方案（有局限性） / Fallback (limited)
        warn "无 jq 环境，使用 grep 降级方案删除（可能需要手动验证索引文件）"
        warn "No jq available, using grep fallback (may need manual index verification)"
        local tmp_file="${INDEX_FILE}.tmp.$$"
        # 简单方案：逐行过滤掉包含该 id 的条目
        grep -v "\"id\":[[:space:]]*\"${id}\"" "$INDEX_FILE" > "$tmp_file" || true
        mv "$tmp_file" "$INDEX_FILE"
        sed -i "s|\"updated_at\":[[:space:]]*\"[^\"]*\"|\"updated_at\": \"${ts}\"|" "$INDEX_FILE"
    fi

    ok "分区已删除 / Partition deleted: ${id}"
}

# 列出所有分区 / List all partitions
# 用法 / Usage: cmd_list
cmd_list() {
    ensure_dirs
    ensure_index

    local count
    count=$(partition_count)

    if [[ "$count" -eq 0 ]]; then
        info "暂无分区 / No partitions found"
        info "  使用 'partition_manager.sh create <id> <name> <keywords>' 创建"
        info "  Use 'partition_manager.sh create <id> <name> <keywords>' to create one"
        return
    fi

    echo ""
    echo -e "${BOLD}📦 分区列表 / Partition List${NC}"
    echo -e "${BOLD}$(printf '%.0s─' {1..60})${NC}"

    if $HAS_JQ; then
        jq -r '.partitions[] | "  \(.id)\t\(.name)\t\(.size_kb)KB/\(.max_size_kb)KB\t[\(.keywords | join(", "))]"' "$INDEX_FILE" | \
        while IFS=$'\t' read -r id name size kw; do
            printf "  ${CYAN}%-20s${NC} %-20s ${GREEN}%s${NC}  %s\n" "$id" "$name" "$size" "$kw"
        done
    else
        # 降级方案 / Fallback: scan partition files
        for f in "${PARTITIONS_DIR}"/*.md; do
            [[ -f "$f" ]] || continue
            local fname
            fname=$(basename "$f" .md)
            local size
            size=$(file_size_kb "$f")
            local kw
            kw=$(grep -oP '(?<=<!-- Keywords: ).*(?= -->)' "$f" 2>/dev/null || echo "")
            printf "  ${CYAN}%-20s${NC} %sKB  [%s]\n" "$fname" "$size" "$kw"
        done
    fi

    echo ""
    echo -e "  共 ${BOLD}${count}${NC} 个分区 / Total: ${count} partition(s)"
    echo ""
}

# 更新索引 / Update index metadata (sizes, timestamps)
# 用法 / Usage: cmd_update_index
cmd_update_index() {
    ensure_dirs
    ensure_index

    if ! $HAS_JQ; then
        err "update-index 需要 jq / update-index requires jq"
        err "请安装: sudo apt install jq / Install: sudo apt install jq"
        exit 1
    fi

    local updated=0
    local ts
    ts=$(now_ts)

    # 遍历索引中的分区 / Iterate partitions in index
    local ids
    ids=$(jq -r '.partitions[].id' "$INDEX_FILE")

    for id in $ids; do
        local file_path="${PARTITIONS_DIR}/${id}.md"
        if [[ -f "$file_path" ]]; then
            local size
            size=$(file_size_kb "$file_path")
            local file_mtime
            file_mtime=$(date -u -r "$file_path" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "$ts")

            local tmp_file="${INDEX_FILE}.tmp.$$"
            jq --arg id "$id" \
               --argjson size "$size" \
               --arg mtime "$file_mtime" \
               '(.partitions[] | select(.id == $id)) |= (.size_kb = $size | .updated_at = $mtime)' \
               "$INDEX_FILE" > "$tmp_file" && mv "$tmp_file" "$INDEX_FILE"
            ((updated++))
        else
            warn "分区文件缺失 / Partition file missing: ${file_path}"
        fi
    done

    # 扫描未注册的分区文件 / Scan for unregistered partition files
    local unregistered=0
    for f in "${PARTITIONS_DIR}"/*.md; do
        [[ -f "$f" ]] || continue
        local fname
        fname=$(basename "$f" .md)
        if ! partition_exists "$fname"; then
            warn "发现未注册的分区文件 / Found unregistered partition file: ${fname}.md"
            ((unregistered++))
        fi
    done

    # 更新索引时间戳 / Update index timestamp
    local tmp_file="${INDEX_FILE}.tmp.$$"
    jq --arg ts "$ts" '.updated_at = $ts' "$INDEX_FILE" > "$tmp_file" && mv "$tmp_file" "$INDEX_FILE"

    ok "索引已更新 / Index updated: ${updated} partition(s) refreshed"
    [[ "$unregistered" -gt 0 ]] && warn "${unregistered} 个未注册文件，使用 create 命令注册 / ${unregistered} unregistered file(s), use create to register"
}

# 检查容量 / Check partition capacity
# 用法 / Usage: cmd_check_capacity
cmd_check_capacity() {
    ensure_dirs
    ensure_index

    echo ""
    echo -e "${BOLD}📊 容量检查 / Capacity Check${NC}"
    echo -e "${BOLD}$(printf '%.0s─' {1..60})${NC}"

    local warning_count=0
    local critical_count=0

    if $HAS_JQ; then
        # 使用 jq 遍历 / Iterate with jq
        jq -r '.partitions[] | "\(.id)\t\(.size_kb)\t\(.max_size_kb)"' "$INDEX_FILE" | \
        while IFS=$'\t' read -r id size max_size; do
            local pct=0
            if [[ "$max_size" -gt 0 ]]; then
                pct=$(( size * 100 / max_size ))
            fi

            local status_icon status_color
            if [[ "$pct" -ge 90 ]]; then
                status_icon="🔴"
                status_color="$RED"
                ((critical_count++)) || true
            elif [[ "$pct" -ge 70 ]]; then
                status_icon="🟡"
                status_color="$YELLOW"
                ((warning_count++)) || true
            else
                status_icon="🟢"
                status_color="$GREEN"
            fi

            printf "  %s ${CYAN}%-20s${NC} ${status_color}%3dKB / %3dKB (%d%%)${NC}\n" \
                "$status_icon" "$id" "$size" "$max_size" "$pct"
        done
    else
        # 降级方案 / Fallback: scan files
        for f in "${PARTITIONS_DIR}"/*.md; do
            [[ -f "$f" ]] || continue
            local fname size default_max pct
            fname=$(basename "$f" .md)
            size=$(file_size_kb "$f")
            default_max=$(default_max_size_kb)
            pct=$(( size * 100 / default_max ))

            local status_icon
            if [[ "$pct" -ge 90 ]]; then
                status_icon="🔴"
            elif [[ "$pct" -ge 70 ]]; then
                status_icon="🟡"
            else
                status_icon="🟢"
            fi

            printf "  %s %-20s %3dKB / %3dKB (%d%%)\n" "$status_icon" "$fname" "$size" "$default_max" "$pct"
        done
    fi

    echo ""
    echo -e "  🟢 正常 / OK  🟡 ≥70% 注意 / Warning  🔴 ≥90% 危险 / Critical"
    echo ""
}

# 搜索分区 / Search partitions by keyword
# 用法 / Usage: cmd_search <keyword>
cmd_search() {
    local keyword="${1:-}"

    if [[ -z "$keyword" ]]; then
        err "用法 / Usage: partition_manager.sh search <keyword>"
        exit 1
    fi

    ensure_dirs
    ensure_index

    echo ""
    echo -e "${BOLD}🔍 搜索: '${keyword}' / Search: '${keyword}'${NC}"
    echo -e "${BOLD}$(printf '%.0s─' {1..60})${NC}"

    local found=0

    if $HAS_JQ; then
        # 在关键词中搜索 / Search in keywords
        jq -r --arg kw "$keyword" \
            '.partitions[] | select(.keywords[] | ascii_downcase | contains($kw | ascii_downcase)) | "\(.id)\t\(.name)\t\(.keywords | join(", "))"' \
            "$INDEX_FILE" 2>/dev/null | \
        while IFS=$'\t' read -r id name kw; do
            printf "  ${CYAN}%-20s${NC} %-20s [%s]\n" "$id" "$name" "$kw"
            ((found++)) || true
        done

        # 也搜索分区名 / Also search in partition names
        jq -r --arg kw "$keyword" \
            '.partitions[] | select(.name | ascii_downcase | contains($kw | ascii_downcase)) | "\(.id)\t\(.name)"' \
            "$INDEX_FILE" 2>/dev/null | \
        while IFS=$'\t' read -r id name; do
            printf "  ${CYAN}%-20s${NC} %-20s ${YELLOW}(名称匹配/name match)${NC}\n" "$id" "$name"
            ((found++)) || true
        done
    else
        # 降级方案：搜索分区文件内容 / Fallback: search file contents
        for f in "${PARTITIONS_DIR}"/*.md; do
            [[ -f "$f" ]] || continue
            if grep -qi "$keyword" "$f" 2>/dev/null; then
                local fname
                fname=$(basename "$f" .md)
                local match_lines
                match_lines=$(grep -ci "$keyword" "$f" 2>/dev/null || echo 0)
                printf "  ${CYAN}%-20s${NC} (%d 处匹配 / %d matches)\n" "$fname" "$match_lines" "$match_lines"
                ((found++)) || true
            fi
        done
    fi

    if [[ "$found" -eq 0 ]]; then
        # 当 jq 搜索在子 shell 中运行时，found 不会被更新
        # 用另一种方式检查 / Re-check since subshell won't propagate
        local actual_found=0
        if $HAS_JQ; then
            actual_found=$(jq --arg kw "$keyword" \
                '[.partitions[] | select(
                    (.keywords[] | ascii_downcase | contains($kw | ascii_downcase)) or
                    (.name | ascii_downcase | contains($kw | ascii_downcase))
                )] | length' "$INDEX_FILE" 2>/dev/null || echo 0)
        fi
        if [[ "$actual_found" -eq 0 ]]; then
            info "  未找到匹配的分区 / No matching partitions found"
        fi
    fi

    echo ""
}

# --- 帮助信息 / Help --------------------------------------------------------

show_help() {
    cat << 'EOF'
📦 Mjolnir Brain — 分区管理器 / Partition Manager

用法 / Usage:
  partition_manager.sh <command> [args...]

命令 / Commands:
  create <id> <name> [keywords]   创建新分区 / Create partition
                                  keywords: 逗号分隔 / comma-separated
  delete <id>                     归档并删除分区 / Archive and remove
  list                            列出所有分区 / List all partitions
  update-index                    更新索引元数据 / Refresh index metadata
  check-capacity                  检查容量使用 / Check capacity usage
  search <keyword>                按关键词搜索 / Search by keyword
  help                            显示帮助 / Show this help

示例 / Examples:
  partition_manager.sh create my-project "My Project" "项目,决策,project"
  partition_manager.sh list
  partition_manager.sh search "运维"
  partition_manager.sh delete old-notes
  partition_manager.sh check-capacity

环境变量 / Environment Variables:
  MJOLNIR_BRAIN_WORKSPACE    工作空间路径 / Workspace path
                             默认 / Default: $HOME/.openclaw/workspace
EOF
}

# --- 主入口 / Main Entry Point -----------------------------------------------

main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true

    case "$cmd" in
        create)         cmd_create "$@" ;;
        delete)         cmd_delete "$@" ;;
        list)           cmd_list ;;
        update-index)   cmd_update_index ;;
        check-capacity) cmd_check_capacity ;;
        search)         cmd_search "$@" ;;
        help|--help|-h) show_help ;;
        *)
            err "未知命令 / Unknown command: ${cmd}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
