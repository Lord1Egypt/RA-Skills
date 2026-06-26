# ========== harness-core.sh ==========
# 公共函数库：日志/配置/ID生成/安全检查

HARNESS_VERSION="1.0.0"
HARNESS_DIR="${HARNESS_DIR:-.harness}"
HARNESS_DEBUG="${HARNESS_DEBUG:-0}"

# 安全文件清单（永不删除）
SAFE_FILES=("SOUL.md" "IDENTITY.md" "USER.md" "MEMORY.md" "AGENTS.md" "TOOLS.md" "TASKS.md")

# ========== 日志 ==========
log_info() { echo "[INFO]  $*"; }
log_warn() { echo "[WARN]  $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }
log_debug() { [[ "$HARNESS_DEBUG" == "1" ]] && echo "[DEBUG] $*" || true; }
log_ok() { echo "[OK]    $*"; }

# ========== ID生成 ==========
generate_id() {
    if command -v openssl &>/dev/null; then
        openssl rand -hex 8
    else
        date +%s%N
    fi
}

# ========== 安全检查 ==========
is_safe_file() {
    local path="$1"
    for f in "${SAFE_FILES[@]}"; do
        [[ "$path" == *"$f" ]] && return 0
    done
    return 1
}

require_init() {
    if [[ ! -f "$HARNESS_DIR/.initialized" ]]; then
        log_error "Harness not initialized. Run 'harness init' first."
        exit 1
    fi
}

require_command() {
    local cmd="$1"
    if ! command -v "$cmd" &>/dev/null; then
        log_error "Required command '$cmd' not found."
        exit 1
    fi
}

# ========== JSON解析（降级） ==========
# 优先用jq，否则降级
has_jq() { command -v jq &>/dev/null; }

json_get() {
    local file="$1"
    local key="$2"
    if has_jq; then
        jq -r ".$key // empty" "$file" 2>/dev/null
    else
        # 降级：简单grep（不完美但能跑）
        grep "\"$key\"" "$file" 2>/dev/null | sed 's/.*"\([^"]*\)".*/\1/' | head -1
    fi
}

json_set() {
    local file="$1"
    local key="$2"
    local val="$3"
    if has_jq; then
        local tmp=$(mktemp)
        jq --arg v "$val" ".$key = \$v" "$file" > "$tmp" && mv "$tmp" "$file"
    else
        # 降级：sed替换（对特殊字符做转义）
        local escaped_val
        escaped_val="${val//\\/\\\\}"        # escape backslashes
        escaped_val="${escaped_val//\"/\\\"}"  # escape double quotes
        escaped_val="${escaped_val//\$/\\\$}" # escape dollar signs
        escaped_val="${escaped_val//\`/\\\`}" # escape backticks
        sed -i "s/\"$key\":[^,]*/\"$key\": \"$escaped_val\"/" "$file" 2>/dev/null
    fi
}

# ========== 目录创建 ==========
ensure_harness_dir() {
    mkdir -p "$HARNESS_DIR"/{tasks,checkpoints,reports,tmp}
}

# ========== 配置加载 ==========
load_config() {
    local config_file="${HARNESS_DIR}/config.json"
    if [[ -f "$config_file" ]]; then
        if has_jq; then
            echo "$(jq '.' "$config_file" 2>/dev/null)"
        fi
    fi
}

get_config() {
    local key="$1"
    local default="${3:-}"
    local config_file="${HARNESS_DIR}/config.json"
    if [[ -f "$config_file" ]] && has_jq; then
        local val=$(jq -r ".$key // \"$default\"" "$config_file" 2>/dev/null)
        echo "${val:-$default}"
    else
        echo "$default"
    fi
}

# ========== GC日志 ==========
gc_log() {
    local action="$1"
    local target="$2"
    local reason="${3:-}"
    local ts=$(date +%Y-%m-%dT%H:%M:%S%z)
    echo "[$ts] $action | $target | $reason" >> "${HARNESS_DIR}/gc.log"
}

# ========== 校验和 ==========
file_checksum() {
    local path="$1"
    if command -v sha256sum &>/dev/null; then
        sha256sum "$path" | cut -d' ' -f1
    elif command -v shasum &>/dev/null; then
        shasum -a 256 "$path" | cut -d' ' -f1
    else
        # 降级
        stat -c%s "$path" 2>/dev/null || echo "unknown"
    fi
}
