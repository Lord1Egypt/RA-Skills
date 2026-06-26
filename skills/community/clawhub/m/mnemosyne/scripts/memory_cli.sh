#!/usr/bin/env bash
# ============================================================
# Auto Memory CLI - 智能记忆系统核心工具 v2.0
# 支持：capture / search / recent / stats / auto_analyze / auto_session
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$BASE_DIR/memory"
CONFIG_DIR="$BASE_DIR/config"
INDEX_FILE="$MEMORY_DIR/index.json"
CONFIG_FILE="$CONFIG_DIR/user_config.json"

init_dirs() {
    mkdir -p "$MEMORY_DIR/permanent" "$MEMORY_DIR/current" "$MEMORY_DIR/temporary" "$MEMORY_DIR/conflict" "$CONFIG_DIR"
    [[ -f "$INDEX_FILE" ]] || echo '{"version":1,"lastUpdate":0,"memories":[]}' > "$INDEX_FILE"
    [[ -f "$CONFIG_FILE" ]] || cat > "$CONFIG_FILE" << 'EOFCONFIG'
{
  "custom_types": {},
  "auto_trigger": true,
  "tier_rules": {
    "boss_decision": "permanent",
    "boss_preference": "permanent",
    "boss_preference_change": "permanent",
    "boss_info": "permanent",
    "boss_emotion": "current",
    "boss_negative": "current",
    "work_context": "current",
    "learning": "current",
    "insight": "current",
    "error_recovery": "permanent",
    "default": "current"
  }
}
EOFCONFIG
}

generate_id() {
    echo "mem_$(date +%Y%m%d_%H%M%S)"
}

cmd_capture() {
    local type="learning" importance=7 content="" tags="" context=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --type) type="$2"; shift 2 ;;
            --importance) importance="$2"; shift 2 ;;
            --tags) tags="$2"; shift 2 ;;
            --context) context="$2"; shift 2 ;;
            *) content="$1"; shift ;;
        esac
    done
    [[ -z "$content" ]] && echo "Error: content required" && exit 1
    init_dirs

    local tier
    tier=$(python3 "$SCRIPT_DIR/config_manager.py" get_tier "$type" 2>/dev/null || echo "current")

    local id timestamp date
    id=$(generate_id)
    timestamp=$(date +%s)
    date=$(date +%Y-%m-%d)

    local target_dir="$MEMORY_DIR/current"
    [[ "$tier" == "permanent" ]] && target_dir="$MEMORY_DIR/permanent"
    [[ "$tier" == "temporary" ]] && target_dir="$MEMORY_DIR/temporary"

    local memory_file="$target_dir/${date}.md"

    {
        echo ""
        echo "## $id"
        echo "- **类型**: $type"
        echo "- **重要度**: $importance"
        echo "- **内容**: $content"
        echo "- **标签**: ${tags:-无}"
        echo "- **上下文**: ${context:-无}"
        echo "- **时间**: $date"
    } >> "$memory_file"

    python3 "$SCRIPT_DIR/capture_memory.py" \
        "$content" "$type" "$importance" "$tags" "$context" "$tier" "$memory_file" "$INDEX_FILE"

    echo "✅ 记忆已保存: [$type] $content"
}

cmd_search() {
    init_dirs
    local query="${1:-}"
    [[ -z "$query" ]] && echo "Usage: search <keyword>" && exit 1
    python3 "$SCRIPT_DIR/search_memory.py" "$INDEX_FILE" "$query"
}

cmd_recent() {
    init_dirs
    local limit="${1:-10}"
    python3 "$SCRIPT_DIR/recent_memory.py" "$INDEX_FILE" "$limit"
}

cmd_stats() {
    init_dirs
    python3 "$SCRIPT_DIR/stats_memory.py" "$INDEX_FILE"
}

cmd_config() {
    init_dirs
    case "${1:-show}" in
        show) cat "$CONFIG_FILE" ;;
        add_type) python3 "$SCRIPT_DIR/config_manager.py" add_type "${2:-}" "${3:-}" ;;
        set_tier) python3 "$SCRIPT_DIR/config_manager.py" set_tier "${2:-}" "${3:-}" ;;
        *) echo "Usage: config show|add_type|set_tier" ;;
    esac
}

cmd_auto_analyze() {
    init_dirs
    python3 "$SCRIPT_DIR/auto_analyze.py" "$*" "$INDEX_FILE" "$SCRIPT_DIR/config_manager.py"
}

# ============================================================
# 会话级自动记忆（核心新功能）
# 分析整段对话，自动识别并记忆所有重要内容
# ============================================================
cmd_auto_session() {
    init_dirs
    local conversation="$*"
    [[ -z "$conversation" ]] && echo "Usage: auto_session <本会话所有对话内容>" && exit 1

    echo "[SESSION] 开始会话级自动记忆..."
    echo "[SESSION] 分析对话长度: ${#conversation} 字符"

    # 调用 Python 自动分析
    local analysis
    analysis=$(python3 "$SCRIPT_DIR/auto_analyze.py" "$conversation" "$INDEX_FILE" "$SCRIPT_DIR/config_manager.py" 2>&1)
    echo "$analysis"

    # 从分析结果中提取内容，自动记忆
    local count=0
    local lines
    lines=$(python3 -c "
import re, sys

text = '''$conversation'''

# 偏好
for m in re.finditer(r'(?:喜欢|爱|偏好|偏向|更?喜欢|中意)[是]?([^。，,\n]{1,100})', text):
    c = m.group(0).strip()
    if len(c) > 3:
        print(f'PREF|8|{c[:100]}')
        break

for m in re.finditer(r'(?:不喜欢|讨厌|厌恶|排斥|不想|不要)[是]?([^。，,\n]{1,100})', text):
    c = m.group(0).strip()
    if len(c) > 3:
        print(f'PREF|8|{c[:100]}')
        break

# 偏好变化
for m in re.finditer(r'之前(?:喜欢|觉得|认为)(.+?)，(?:但|不过|可是|现在)(.+)', text):
    c = f\"偏好变化：之前「{m.group(1).strip()}」现在「{m.group(2).strip()}」\"
    print(f'CHANGE|9|{c[:100]}')

# 决策
for p in [r'(?:决定|定了|就这样|就定)[了是]?(.+)', r'最后选了?(.+)', r'目标[是为](.+)']:
    for m in re.finditer(p, text):
        c = m.group(1).strip() if m.lastindex else m.group(0).strip()
        if len(c) > 2:
            print(f'DEC|9|{c[:100]}')
            break

# 情绪
for p in [r'(?:心情|情绪|感觉)([^。，\n]{1,50})', r'(?:累|疲惫|困)([^。，\n]{0,30})', r'(?:焦虑|担心|压力大)([^。，\n]{0,30})']:
    for m in re.finditer(p, text):
        c = m.group(0).strip()
        if len(c) > 3:
            print(f'EMOT|6|{c[:80]}')

# 学到/发现
for m in re.finditer(r'(?:学会|学到|发现?|原来|才知)[道了]?(.+)', text):
    c = m.group(1).strip()
    if len(c) > 2:
        print(f'LEARN|8|{c[:100]}')

# 任务完成
for m in re.finditer(r'(?:完成了?|搞定了?|做好了?)(.+)', text):
    c = m.group(1).strip()
    if len(c) > 2:
        print(f'WORK|7|{c[:100]}')

# 数字/日期/金额（只记重要数字）
for m in re.finditer(r'\d+[人个只台件条]', text):
    c = m.group(0).strip()
    print(f'NUM|6|{c}')
" 2>/dev/null)

    # 去重并记忆
    local seen_types=""
    while IFS='|' read -r mtype imp content; do
        [[ -z "$content" ]] && continue
        # 去重：同类只记第一条
        local type_key="${mtype}"
        if echo "$seen_types" | grep -q "$type_key"; then
            continue
        fi
        seen_types="$seen_types $type_key"

        local tier
        tier=$(python3 "$SCRIPT_DIR/config_manager.py" get_tier "$mtype" 2>/dev/null || echo "current")

        bash "$SCRIPT_DIR/memory_cli.sh" capture "$content" --type "$mtype" --importance "$imp" 2>/dev/null || true
        count=$((count + 1))
    done <<< "$lines"

    echo ""
    echo "[SESSION] ✅ 会话级自动记忆完成，共记忆 $count 条"
}

# ============================================================
# 主入口
# ============================================================
init_dirs

COMMAND="${1:-}"
shift 2>/dev/null || true

case "$COMMAND" in
    capture)      cmd_capture "$@" ;;
    search)      cmd_search "$@" ;;
    recent)      cmd_recent "$@" ;;
    stats)       cmd_stats ;;
    config)      cmd_config "$@" ;;
    auto_analyze) cmd_auto_analyze "$@" ;;
    auto_session) cmd_auto_session "$@" ;;
    help|--help) cat << 'EOF'
Auto Memory CLI v2.0 - 智能记忆系统

  capture <content> [--type TYPE] [--importance N]   捕获记忆
  search <keyword>                                    搜索记忆
  recent [N]                                          最近N条记忆
  stats                                               记忆统计
  config show|add_type|set_tier                        配置管理
  auto_analyze <对话内容>                              分析对话（AI自动分析）
  auto_session <整段对话>                              会话级自动记忆（推荐）
  help                                                显示本帮助
EOF
            ;;
    *)          cmd_capture "$COMMAND" "$@" ;;
esac
