#!/usr/bin/env bash
# backup_manager.sh — 备份管理脚本
# 支持：备份状态检查、备份执行、备份验证、备份清理
# 用法:
#   bash scripts/backup_manager.sh status     — 检查备份状态
#   bash scripts/backup_manager.sh run        — 执行备份
#   bash scripts/backup_manager.sh verify     — 验证最新备份
#   bash scripts/backup_manager.sh cleanup    — 清理旧备份

# 配置（可通过环境变量覆盖）
BACKUP_TOOL="${BACKUP_TOOL:-auto}"          # auto/borg/restic/rsync
BACKUP_SRC="${BACKUP_SRC:-/etc /home /opt}" # 备份源目录
BACKUP_DST="${BACKUP_DST:-/backup}"         # 备份目标
BACKUP_KEEP_DAILY="${BACKUP_KEEP_DAILY:-7}"
BACKUP_KEEP_WEEKLY="${BACKUP_KEEP_WEEKLY:-4}"
BACKUP_KEEP_MONTHLY="${BACKUP_KEEP_MONTHLY:-6}"
BORG_ENCRYPTION="${BORG_ENCRYPTION:-repokey}"

# 参数解析（优先处理 --help/--version）
case "${1:-}" in
    --help|-h)
        echo "用法: bash $0 {status|run|verify|cleanup}"
        echo ""
        echo "备份管理：状态检查、备份执行、验证、清理，支持 borg/restic/rsync。"
        echo ""
        echo "命令:"
        echo "  status   — 检查备份状态"
        echo "  run      — 执行备份"
        echo "  verify   — 验证最新备份"
        echo "  cleanup  — 清理旧备份"
        echo ""
        echo "环境变量:"
        echo "  BACKUP_TOOL=auto|borg|restic|rsync"
        echo "  BACKUP_SRC=\"/etc /home /opt\""
        echo "  BACKUP_DST=/backup"
        echo "  BACKUP_KEEP_DAILY=7"
        echo "  BACKUP_KEEP_WEEKLY=4"
        echo "  BACKUP_KEEP_MONTHLY=6"
        echo "  BORG_ENCRYPTION=repokey  (可选: none/repokey/repokey-blake2/keyfile)"
        echo ""
        echo "选项:"
        echo "  --help, -h      显示此帮助信息"
        echo "  --version       显示版本信息"
        exit 0
        ;;
    --version)
        echo "backup_manager.sh v3.0.2"
        exit 0
        ;;
esac

ACTION="${1:-status}"

# 颜色输出（非终端环境自动禁用，避免转义码泄露）
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' NC=''
fi

pass()  { echo -e "  ${GREEN}✅ PASS${NC}: $1"; }
warn()  { echo -e "  ${YELLOW}⚠️  WARN${NC}: $1"; }
fail()  { echo -e "  ${RED}❌ FAIL${NC}: $1"; }
info()  { echo -e "  ℹ️  INFO: $1"; }

divider() {
    echo ""
    echo "================================================================"
    echo "  $1"
    echo "================================================================"
}

# 自动检测备份工具
detect_tool() {
    if [ "$BACKUP_TOOL" != "auto" ]; then
        echo "$BACKUP_TOOL"
        return
    fi
    if command -v borg &>/dev/null; then
        echo "borg"
    elif command -v restic &>/dev/null; then
        echo "restic"
    elif command -v rsync &>/dev/null; then
        echo "rsync"
    else
        echo "none"
    fi
}

# ==================== 状态检查 ====================
cmd_status() {
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║          备份状态检查报告                                   ║"
    echo "║          检查时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"

    divider "1. 备份工具检测"
    local tool
    tool=$(detect_tool)
    case "$tool" in
        borg)   pass "检测到 borgbackup $(borg --version 2>/dev/null)" ;;
        restic) pass "检测到 restic $(restic version 2>/dev/null | awk '{print $2}')" ;;
        rsync)  pass "检测到 rsync $(rsync --version 2>/dev/null | head -1 | awk '{print $3}')" ;;
        none)   fail "未检测到备份工具（borg/restic/rsync）" ;;
    esac

    # 检查其他备份工具
    for cmd in mysqldump pg_dump xtrabackup; do
        if command -v "$cmd" &>/dev/null; then
            info "数据库备份工具: $cmd 可用"
        fi
    done

    divider "2. 备份存储"
    if [ -d "$BACKUP_DST" ]; then
        local used avail pct
        used=$(du -sh "$BACKUP_DST" 2>/dev/null | awk '{print $1}')
        avail=$(df -h "$BACKUP_DST" 2>/dev/null | awk 'NR==2{print $4}')
        pct=$(df "$BACKUP_DST" 2>/dev/null | awk 'NR==2{print $5}' | tr -d '%')
        info "备份目录: $BACKUP_DST"
        info "已用空间: $used"
        info "可用空间: $avail"
        if [ -n "$pct" ] && [ "$pct" -gt 85 ] 2>/dev/null; then
            warn "备份分区使用率 ${pct}%（>85%）"
        else
            pass "备份分区使用率 ${pct}%"
        fi
    else
        warn "备份目录 $BACKUP_DST 不存在"
    fi

    divider "3. 最新备份"
    case "$tool" in
        borg)
            if [ -d "$BACKUP_DST" ]; then
                latest=$(borg list --last 1 --format '{archive} {time}' "$BACKUP_DST" 2>/dev/null)
                if [ -n "$latest" ]; then
                    info "最新备份: $latest"
                    # 检查备份年龄
                    latest_time=$(borg list --last 1 --format '{time}' "$BACKUP_DST" 2>/dev/null)
                    if [ -n "$latest_time" ]; then
                        latest_ts=$(date -d "$latest_time" +%s 2>/dev/null)
                        now_ts=$(date +%s)
                        age_hours=$(( (now_ts - latest_ts) / 3600 ))
                        if [ "$age_hours" -gt 26 ]; then
                            warn "最新备份已 ${age_hours} 小时前（超过 26 小时）"
                        else
                            pass "最新备份 ${age_hours} 小时前"
                        fi
                    fi
                    # 备份数量
                    count=$(borg list "$BACKUP_DST" 2>/dev/null | wc -l)
                    info "备份总数: $count"
                else
                    warn "无备份记录"
                fi
            fi
            ;;
        restic)
            latest=$(restic snapshots --latest 1 --json 2>/dev/null | python3 -c "import sys,json; s=json.load(sys.stdin); print(s[0]['time'][:19] if s else 'none')" 2>/dev/null)
            if [ "$latest" != "none" ] && [ -n "$latest" ]; then
                info "最新快照: $latest"
                count=$(restic snapshots --json 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null)
                info "快照总数: $count"
            else
                warn "无快照记录"
            fi
            ;;
        rsync)
            if [ -L "$BACKUP_DST/latest" ]; then
                latest=$(readlink "$BACKUP_DST/latest")
                info "最新备份: $(basename "$latest")"
            else
                warn "未找到 latest 链接"
            fi
            # 统计备份目录数
            count=$(find "$BACKUP_DST" -maxdepth 1 -type d -name "2*" 2>/dev/null | wc -l)
            info "备份目录数: $count"
            ;;
    esac

    divider "4. 定时任务"
    # 检查 cron
    cron_backup=$(crontab -l 2>/dev/null | grep -i "backup\|borg\|restic\|rsync" | grep -v "^#")
    if [ -n "$cron_backup" ]; then
        pass "检测到备份 cron 任务:"
        echo "$cron_backup" | while read -r line; do
            echo "    $line"
        done
    fi

    # 检查 systemd timer
    timer_backup=$(systemctl list-timers --no-pager 2>/dev/null | grep -i "backup")
    if [ -n "$timer_backup" ]; then
        pass "检测到备份 systemd timer:"
        echo "    $timer_backup"
    fi

    if [ -z "$cron_backup" ] && [ -z "$timer_backup" ]; then
        warn "未检测到备份定时任务"
    fi

    divider "5. 数据库备份"
    # MySQL
    if command -v mysql &>/dev/null; then
        mysql_backup=$(find "$BACKUP_DST" -name "*.sql*" -mtime -1 2>/dev/null | head -3)
        if [ -n "$mysql_backup" ]; then
            pass "检测到 24 小时内的 MySQL 备份"
            echo "$mysql_backup" | while read -r f; do
                echo "    $(ls -lh "$f" 2>/dev/null | awk '{print $5, $9}')"
            done
        else
            warn "未检测到近期 MySQL 备份"
        fi
    fi

    # PostgreSQL
    if command -v psql &>/dev/null; then
        pg_backup=$(find "$BACKUP_DST" -name "*pg*dump*" -mtime -1 2>/dev/null | head -3)
        if [ -n "$pg_backup" ]; then
            pass "检测到 24 小时内的 PostgreSQL 备份"
        else
            warn "未检测到近期 PostgreSQL 备份"
        fi
    fi

    echo ""
    divider "检查完成"
    echo "报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
}

# ==================== 执行备份 ====================
cmd_run() {
    local tool
    tool=$(detect_tool)

    echo "=== 开始备份: $(date) ==="
    echo "工具: $tool"
    echo "源: $BACKUP_SRC"
    echo "目标: $BACKUP_DST"

    case "$tool" in
        borg)
            if [ ! -d "$BACKUP_DST/data" ]; then
                info "初始化 borg 仓库..."
                borg init --encryption="$BORG_ENCRYPTION" "$BACKUP_DST" 2>/dev/null
            fi
            local name
            name="$(hostname)-$(date +%Y%m%d-%H%M%S)"
            # shellcheck disable=SC2086
            borg create --stats --compression lz4 \
                "$BACKUP_DST::$name" \
                $BACKUP_SRC \
                --exclude '*.log.gz' \
                --exclude '*.tmp' \
                --exclude '*/.cache'
            if [ $? -eq 0 ]; then
                pass "Borg 备份完成: $name"
            else
                fail "Borg 备份失败"
                return 1
            fi
            ;;
        restic)
            # shellcheck disable=SC2086
            restic backup $BACKUP_SRC \
                --repo "$BACKUP_DST" \
                --exclude='*.log.gz' \
                --exclude='*.tmp' \
                --tag "$(hostname)" \
                --verbose
            ;;
        rsync)
            local date_dir
            date_dir="$BACKUP_DST/$(date +%Y%m%d_%H%M%S)"
            local latest_link="$BACKUP_DST/latest"
            local link_dest_opt=""
            [ -L "$latest_link" ] && link_dest_opt="--link-dest=$latest_link"
            # shellcheck disable=SC2086
            rsync -avz --delete $link_dest_opt \
                $BACKUP_SRC \
                "$date_dir/"
            rm -f "$latest_link"
            ln -s "$date_dir" "$latest_link"
            pass "rsync 备份完成: $date_dir"
            ;;
        *)
            fail "无可用备份工具"
            return 1
            ;;
    esac

    echo "=== 备份结束: $(date) ==="
}

# ==================== 验证备份 ====================
cmd_verify() {
    local tool
    tool=$(detect_tool)

    echo "=== 验证备份完整性 ==="

    case "$tool" in
        borg)
            borg check "$BACKUP_DST"
            if [ $? -eq 0 ]; then
                pass "Borg 仓库完整性验证通过"
            else
                fail "Borg 仓库完整性验证失败"
            fi
            # 列出最新备份内容
            latest=$(borg list --last 1 --format '{archive}' "$BACKUP_DST" 2>/dev/null)
            if [ -n "$latest" ]; then
                info "最新备份 ($latest) 文件数:"
                borg list "$BACKUP_DST::$latest" 2>/dev/null | wc -l
            fi
            ;;
        restic)
            restic check --repo "$BACKUP_DST"
            if [ $? -eq 0 ]; then
                pass "Restic 仓库验证通过"
            else
                fail "Restic 仓库验证失败"
            fi
            ;;
        rsync)
            if [ -L "$BACKUP_DST/latest" ]; then
                local latest_dir
                latest_dir=$(readlink -f "$BACKUP_DST/latest")
                local file_count
                file_count=$(find "$latest_dir" -type f 2>/dev/null | wc -l)
                pass "最新备份包含 $file_count 个文件"
            else
                fail "未找到最新备份"
            fi
            ;;
    esac
}

# ==================== 清理旧备份 ====================
cmd_cleanup() {
    local tool
    tool=$(detect_tool)

    echo "=== 清理旧备份 ==="

    case "$tool" in
        borg)
            borg prune --stats \
                --keep-daily="$BACKUP_KEEP_DAILY" \
                --keep-weekly="$BACKUP_KEEP_WEEKLY" \
                --keep-monthly="$BACKUP_KEEP_MONTHLY" \
                "$BACKUP_DST"
            borg compact "$BACKUP_DST"
            pass "Borg 清理完成"
            ;;
        restic)
            restic forget \
                --keep-daily "$BACKUP_KEEP_DAILY" \
                --keep-weekly "$BACKUP_KEEP_WEEKLY" \
                --keep-monthly "$BACKUP_KEEP_MONTHLY" \
                --prune \
                --repo "$BACKUP_DST"
            pass "Restic 清理完成"
            ;;
        rsync)
            local count
            count=$(find "$BACKUP_DST" -maxdepth 1 -type d -name "2*" -mtime +30 2>/dev/null | wc -l)
            if [ "$count" -gt 0 ]; then
                find "$BACKUP_DST" -maxdepth 1 -type d -name "2*" -mtime +30 -exec rm -rf {} +
                pass "清理了 $count 个超过 30 天的备份"
            else
                info "无需清理"
            fi
            ;;
    esac
}

# ==================== 主入口 ====================
case "$ACTION" in
    status)  cmd_status ;;
    run)     cmd_run ;;
    verify)  cmd_verify ;;
    cleanup) cmd_cleanup ;;
    *)
        echo "用法: $0 {status|run|verify|cleanup}"
        echo ""
        echo "  status   — 检查备份状态"
        echo "  run      — 执行备份"
        echo "  verify   — 验证最新备份"
        echo "  cleanup  — 清理旧备份"
        echo ""
        echo "环境变量:"
        echo "  BACKUP_TOOL=auto|borg|restic|rsync"
        echo "  BACKUP_SRC=\"/etc /home /opt\""
        echo "  BACKUP_DST=/backup"
        echo "  BACKUP_KEEP_DAILY=7"
        echo "  BACKUP_KEEP_WEEKLY=4"
        echo "  BACKUP_KEEP_MONTHLY=6"
        echo "  BORG_ENCRYPTION=repokey  (可选: none/repokey/repokey-blake2/keyfile)"
        exit 1
        ;;
esac
