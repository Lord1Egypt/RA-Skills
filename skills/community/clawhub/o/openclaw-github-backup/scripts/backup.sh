#!/bin/bash
# OpenClaw 备份脚本
# 用途：将 OpenClaw 配置安全备份到 GitHub
# 包含: agents/, extensions/, memory/, openclaw.json
# 用法: ./backup.sh [backup|restore|auto]

set -e

OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_BRANCH="main"
REMOTE="origin"
STATE_FILE="$OPENCLAW_DIR/workspace/memory/heartbeat-state.json"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 脱敏 openclaw.json（移除 API Key）
sanitize_config() {
    local input="$1"
    local output="$2"
    
    if [[ -f "$input" ]]; then
        sed -E 's/"apiKey": "[^"]+"/"apiKey": "***SET_YOUR_API_KEY***"/g' "$input" > "$output"
        log_info "配置文件已脱敏"
    else
        log_error "配置文件不存在: $input"
        return 1
    fi
}

# 检查活跃状态
check_activity() {
    local active_threshold=3600
    
    if [[ -d "$OPENCLAW_DIR/agents" ]]; then
        recent_files=$(find "$OPENCLAW_DIR/agents" -name "*.jsonl" -type f -mmin -$((active_threshold/60)) 2>/dev/null | wc -l)
        if [[ $recent_files -gt 0 ]]; then
            echo "active"
            return 0
        fi
    fi
    
    if [[ -d "$OPENCLAW_DIR/workspace" ]]; then
        recent_files=$(find "$OPENCLAW_DIR/workspace" -type f -mmin -$((active_threshold/60)) 2>/dev/null | wc -l)
        if [[ $recent_files -gt 0 ]]; then
            echo "active"
            return 0
        fi
    fi
    
    echo "inactive"
}

# 获取上次备份时间（毫秒）
get_last_backup() {
    if [[ -f "$STATE_FILE" ]] && command -v python3 &>/dev/null; then
        python3 -c "import json; f=open('$STATE_FILE'); d=json.load(f); print(d.get('backup',{}).get('lastBackup',0) or 0)" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# 更新备份时间
update_backup_time() {
    local now=$(date +%s)000
    if [[ -f "$STATE_FILE" ]] && command -v python3 &>/dev/null; then
        python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    d = json.load(f)
if 'backup' not in d:
    d['backup'] = {}
d['backup']['lastBackup'] = $now
with open('$STATE_FILE', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null
    fi
}

# 执行备份
do_backup() {
    cd "$OPENCLAW_DIR"
    
    log_info "开始备份 OpenClaw..."
    
    if [[ -z $(git status --porcelain 2>/dev/null) ]]; then
        log_info "没有变更需要备份"
        return 0
    fi
    
    if [[ -f "openclaw.json" ]]; then
        cp openclaw.json openclaw.json.original
        sanitize_config "openclaw.json.original" "openclaw.json.staged"
        mv openclaw.json.staged openclaw.json
    fi
    
    git add -A
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "Auto backup: $timestamp"
    log_info "已提交备份: $timestamp"
    
    git push origin "$BACKUP_BRANCH" 2>/dev/null || {
        log_warn "推送失败，尝试强制推送..."
        git push origin "$BACKUP_BRANCH" --force
    }
    log_info "已推送到 GitHub"
    
    if [[ -f "openclaw.json.original" ]]; then
        mv openclaw.json.original openclaw.json
        log_info "已恢复原始配置"
    fi
    
    update_backup_time
    
    log_info "备份完成！"
}

# 自动备份（根据活跃状态）
auto_backup() {
    local activity=$(check_activity)
    local now=$(date +%s)000
    local last_backup=$(get_last_backup)
    local interval
    
    if [[ "$activity" == "active" ]]; then
        interval=3600000
        log_info "检测到活跃对话，备份间隔: 1小时"
    else
        interval=86400000
        log_info "无活跃对话，备份间隔: 24小时"
    fi
    
    local elapsed=$((now - last_backup))
    
    if [[ $elapsed -ge $interval ]]; then
        log_info "距离上次备份已超过阈值，执行备份..."
        do_backup
    else
        local remaining=$(( (interval - elapsed) / 60000 ))
        log_info "距离下次备份还有 ${remaining} 分钟"
    fi
}

# 恢复配置
restore_config() {
    log_warn "恢复功能需要手动操作："
    echo ""
    echo "1. 备份当前配置："
    echo "   mv ~/.openclaw ~/.openclaw.bak"
    echo ""
    echo "2. 克隆仓库："
    echo "   git clone <your-repo-url> ~/.openclaw"
    echo ""
    echo "3. 恢复 API Key："
    echo "   nano ~/.openclaw/openclaw.json"
    echo ""
    echo "4. 重启 Gateway："
    echo "   openclaw gateway restart"
}

# 主函数
main() {
    case "${1:-backup}" in
        backup)
            do_backup
            ;;
        auto)
            auto_backup
            ;;
        restore)
            restore_config
            ;;
        *)
            echo "用法: $0 {backup|restore|auto}"
            exit 1
            ;;
    esac
}

main "$@"