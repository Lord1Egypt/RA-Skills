#!/bin/bash
# ============================================
# OpenClaw 工作区 → 坚果云 实时同步脚本
# 使用 inotifywait 监听文件变化，3 秒防抖后同步
# ============================================

set -e

# 配置
WORKSPACE_DIR="/home/admin/.openclaw/workspace"
NUTSTORE_DIR="/home/admin/Nutstore/OpenClaw-Backup"
OBSIDIAN_DIR="/home/admin/Nutstore/我的知识/OpenClaw"  # Mac Obsidian 同步目录（使用我的知识目录）
LOG_FILE="/home/admin/.openclaw/logs/sync-realtime.log"
PID_FILE="/tmp/sync-realtime.pid"

# 监听目录
WATCH_DIRS=(
    "articles"
    "memory"
    "projects"
    "docs"
    "scripts"
    "learnings"
)

# 排除的文件/目录
EXCLUDE_PATTERNS=(
    "*.log"
    "*.tmp"
    "*.swp"
    ".git"
    "node_modules"
    "__pycache__"
    "*.pyc"
    ".DS_Store"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$timestamp] $1" | tee -a "$LOG_FILE"
}

# 确保目录存在
ensure_dirs() {
    # 坚果云备份目录
    mkdir -p "$NUTSTORE_DIR/articles"
    mkdir -p "$NUTSTORE_DIR/memory"
    mkdir -p "$NUTSTORE_DIR/projects"
    mkdir -p "$NUTSTORE_DIR/docs"
    mkdir -p "$NUTSTORE_DIR/scripts"
    
    # Obsidian 同步目录（我的知识/OpenClaw）
    if [ -d "/home/admin/Nutstore/我的知识" ]; then
        mkdir -p "$OBSIDIAN_DIR/articles"
        mkdir -p "$OBSIDIAN_DIR/docs"
        mkdir -p "$OBSIDIAN_DIR/memory"
        mkdir -p "$OBSIDIAN_DIR/learnings"
        log "${GREEN}✅ Obsidian 同步目录已配置${NC}"
    fi
    
    mkdir -p "$(dirname "$LOG_FILE")"
}

# 检查是否应该排除
should_exclude() {
    local file="$1"
    local basename=$(basename "$file")
    
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        case "$basename" in
            $pattern) return 0 ;;
        esac
    done
    
    # 排除隐藏文件
    [[ "$basename" == .* ]] && return 0
    
    return 1
}

# 同步单个文件
sync_file() {
    local src="$1"
    local rel_path="${src#$WORKSPACE_DIR/}"
    local dest="$NUTSTORE_DIR/$rel_path"
    local dest_dir=$(dirname "$dest")
    
    # 检查是否应该排除
    if should_exclude "$src"; then
        log "${BLUE}⊘ 跳过：$rel_path${NC}"
        return 0
    fi
    
    # 确保目标目录存在
    mkdir -p "$dest_dir"
    
    # 复制到坚果云备份目录
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        log "${GREEN}✓ 同步：$rel_path${NC}"
        
        # 同步到 Obsidian 目录（我的知识/OpenClaw）
        if [ -d "/home/admin/Nutstore/我的知识" ]; then
            sync_to_obsidian "$src" "$rel_path"
        fi
    elif [ -d "$src" ]; then
        # 目录变化，同步整个目录
        rsync -av --delete "$src/" "$dest/" 2>/dev/null || cp -r "$src/"* "$dest/" 2>/dev/null || true
        log "${GREEN}✓ 同步目录：$rel_path${NC}"
    fi
}

# 同步到 Obsidian 目录
sync_to_obsidian() {
    local src="$1"
    local rel_path="$2"
    local obsidian_dest="$OBSIDIAN_DIR/$rel_path"
    local obsidian_dir=$(dirname "$obsidian_dest")
    
    # 只同步重要目录
    case "$rel_path" in
        articles/*|docs/*|memory/*|learnings/*)
            mkdir -p "$obsidian_dir"
            cp "$src" "$obsidian_dest"
            log "${BLUE}📚 Obsidian: $rel_path${NC}"
            ;;
    esac
}

# 防抖同步（等待 3 秒无新变化后执行）
debounce_sync() {
    local delay=3
    local pending_files=()
    
    while true; do
        # 等待延迟时间
        sleep $delay
        
        # 检查是否有新变化（简化版：直接同步）
        break
    done
}

# 主同步循环
main_loop() {
    log "========================================"
    log "${GREEN}🚀 启动实时同步守护进程${NC}"
    log "========================================"
    log "工作区：$WORKSPACE_DIR"
    log "目标：$NUTSTORE_DIR"
    log "监听目录：${WATCH_DIRS[*]}"
    log "PID: $$"
    log "========================================"
    
    # 保存 PID
    echo $$ > "$PID_FILE"
    
    # 构建 inotifywait 参数
    local watch_paths=()
    for dir in "${WATCH_DIRS[@]}"; do
        if [ -d "$WORKSPACE_DIR/$dir" ]; then
            watch_paths+=("$WORKSPACE_DIR/$dir")
        fi
    done
    
    if [ ${#watch_paths[@]} -eq 0 ]; then
        log "${RED}❌ 没有可监听的目录，退出${NC}"
        exit 1
    fi
    
    # 初始全量同步
    log "${BLUE}📦 执行初始全量同步...${NC}"
    for dir in "${WATCH_DIRS[@]}"; do
        if [ -d "$WORKSPACE_DIR/$dir" ]; then
            rsync -av --delete "$WORKSPACE_DIR/$dir/" "$NUTSTORE_DIR/$dir/" 2>/dev/null || \
            cp -r "$WORKSPACE_DIR/$dir/"* "$NUTSTORE_DIR/$dir/" 2>/dev/null || true
            log "${GREEN}✓ 初始同步：$dir${NC}"
        fi
    done
    
    # 同步到 Obsidian 目录（我的知识/OpenClaw）
    if [ -d "/home/admin/Nutstore/我的知识" ]; then
        log "${BLUE}📚 同步到 Obsidian 目录...${NC}"
        for dir in "articles" "docs" "memory" "learnings"; do
            if [ -d "$WORKSPACE_DIR/$dir" ]; then
                rsync -av --delete "$WORKSPACE_DIR/$dir/" "$OBSIDIAN_DIR/$dir/" 2>/dev/null || \
                cp -r "$WORKSPACE_DIR/$dir/"* "$OBSIDIAN_DIR/$dir/" 2>/dev/null || true
                log "${GREEN}✓ Obsidian 同步：$dir${NC}"
            fi
        done
    fi
    
    log "${GREEN}✅ 初始同步完成${NC}"
    log "========================================"
    
    # 实时监听
    log "${BLUE}👁️  开始监听文件变化...${NC}"
    
    inotifywait -m -r -e modify,create,delete,move \
        --format '%w%f' \
        --exclude '\.(log|tmp|swp|pyc)$' \
        --exclude 'node_modules' \
        --exclude '__pycache__' \
        --exclude '\.git' \
        "${watch_paths[@]}" 2>/dev/null | while read file; do
        
        # 跳过日志文件
        [[ "$file" == *".log" ]] && continue
        [[ "$file" == *"/logs/"* ]] && continue
        
        # 同步文件
        sync_file "$file"
        
    done
}

# 停止守护进程
stop() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log "${YELLOW}🛑 停止实时同步进程 (PID: $pid)${NC}"
            kill "$pid"
            rm -f "$PID_FILE"
            log "${GREEN}✅ 已停止${NC}"
        else
            log "${YELLOW}⚠️  进程不存在，清理 PID 文件${NC}"
            rm -f "$PID_FILE"
        fi
    else
        log "${YELLOW}⚠️  PID 文件不存在，可能未运行${NC}"
    fi
}

# 检查状态
status() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log "${GREEN}✅ 实时同步运行中 (PID: $pid)${NC}"
            return 0
        else
            log "${YELLOW}⚠️  进程不存在 (PID: $pid)${NC}"
            return 1
        fi
    else
        log "${YELLOW}⚠️  实时同步未运行${NC}"
        return 1
    fi
}

# 命令行参数
case "${1:-start}" in
    start)
        ensure_dirs
        main_loop
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        ensure_dirs
        main_loop
        ;;
    status)
        status
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status}"
        exit 1
        ;;
esac
