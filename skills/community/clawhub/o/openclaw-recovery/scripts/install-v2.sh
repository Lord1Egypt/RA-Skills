#!/bin/bash
# OpenClaw 自救系统 v2.3.0 安装脚本
# 自动检测操作系统，生成适配版本

set -e

echo "=== OpenClaw 自救系统 v2.3.0 安装 ==="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.openclaw/workspace/skills/openclaw-recovery"

# ==================== 检测操作系统 ====================
detect_os() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)        echo "unknown" ;;
    esac
}

OS=$(detect_os)
echo "[系统] 检测到操作系统: $OS"

# ==================== 平台特定配置 ====================
case "$OS" in
    macos)
        NOTIFY_CMD="osascript -e 'display notification \"\$2\" with title \"\$1\" sound name \"Glass\"'"
        MEMORY_CHECK="vm_stat 2>/dev/null | grep 'Pages free' | awk '{print \$3}' | sed 's/\.//'"
        DATE_FORMAT="date '+%Y-%m-%d %H:%M:%S'"
        PACKAGE_MANAGER="brew"
        ;;
    linux)
        NOTIFY_CMD="notify-send \"\$1\" \"\$2\" 2>/dev/null"
        MEMORY_CHECK="free | awk '/Mem:/ {printf \"%.0f\", \$7/\$2*100}'"
        DATE_FORMAT="date '+%Y-%m-%d %H:%M:%S'"
        PACKAGE_MANAGER="apt"
        ;;
    windows)
        # Windows 下建议用 Git Bash 或 WSL，这里提供 PowerShell 命令
        NOTIFY_CMD="powershell -Command \"& {[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > \$null; \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); \$text = \$template.GetElementsByTagName('text'); \$text.Item(0).AppendChild(\$template.CreateTextNode('\$1: \$2')) > \$null; [Windows.UI.Notifications.ToastNotification]::new(\$template) > \$null}\""
        DATE_FORMAT="date '+%Y-%m-%d %H:%M:%S'"
        PACKAGE_MANAGER="winget"
        ;;
    *)
        echo "❌ 不支持的操作系统: $(uname -s)"
        exit 1
        ;;
esac

# ==================== 创建目录 ====================
echo "[1/5] 创建目录..."
mkdir -p "$INSTALL_DIR/scripts/generated"
mkdir -p "$HOME/.openclaw/backups"
mkdir -p "$HOME/.openclaw/logs"

# ==================== 生成平台适配的恢复脚本 ====================
echo "[2/5] 生成 $OS 适配脚本..."

cat > "$INSTALL_DIR/scripts/generated/recover.sh" << RECOVER_EOF
#!/bin/bash
# OpenClaw 健康监控与自动恢复 - $OS 适配版
# 由 install-v2.sh 自动生成，不要手动编辑

CONFIG_FILE="\$HOME/.openclaw/openclaw.json"
BACKUP_DIR="\$HOME/.openclaw/backups"
LOG_FILE="\$HOME/.openclaw/logs/recovery.log"
HISTORY_FILE="\$HOME/.openclaw/logs/recovery-history.log"
SAFE_CONFIG="\$HOME/.openclaw/safe-mode.json"
MAX_RETRIES=10
MAX_LOG_LINES=1000

mkdir -p "\$HOME/.openclaw/logs"

# ==================== 通知（$OS 适配） ====================
send_notification() {
    local title="\$1"
    local message="\$2"
    echo "[\$date] [通知] \$title: \$message" >> "\$LOG_FILE"
    $NOTIFY_CMD
}

# ==================== 日志轮转 ====================
rotate_log() {
    local logfile="\$1"
    local max_lines="\$2"
    if [ -f "\$logfile" ] && [ \$(wc -l < "\$logfile") -gt \$max_lines ]; then
        tail -n \$max_lines "\$logfile" > "\${logfile}.tmp"
        mv "\${logfile}.tmp" "\$logfile"
    fi
}

# ==================== 获取端口 ====================
get_gateway_port() {
    if [ -f "\$CONFIG_FILE" ]; then
        python3 -c "
import json
try:
    c = json.load(open('\$CONFIG_FILE'))
    print(c.get('gateway', {}).get('port', 18789))
except:
    print(18789)
" 2>/dev/null
    else
        echo 18789
    fi
}

# ==================== 健康检查 ====================
health_check() {
    local port=\$(get_gateway_port)

    # HTTP 检查
    if command -v curl >/dev/null 2>&1; then
        local code=\$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://127.0.0.1:\$port/" 2>/dev/null)
        echo "\$code" | grep -q "200\\|301\\|302" && return 0
    fi

    # TCP 检查
    if command -v nc >/dev/null 2>&1; then
        nc -z -w 1 127.0.0.1 \$port 2>/dev/null && return 0
    fi

    # 进程检查
    pgrep -f "openclaw.*gateway" >/dev/null 2>&1 && return 0

    return 1
}

# ==================== 配置验证 ====================
validate_config() {
    local config="\$1"
    python3 -c "import json; json.load(open('\$config'))" 2>/dev/null || return 1
    return 0
}

# ==================== 修复配置 ====================
fix_config() {
    local config="\$1"
    local timestamp=\$(date +%Y%m%d_%H%M%S)
    cp "\$config" "\$BACKUP_DIR/openclaw.json.invalid.\$timestamp"

    python3 << 'PYEOF' "\$config" 2>/dev/null
import json, sys
config_file = sys.argv[1]
with open(config_file, 'r') as f:
    config = json.load(f)
try:
    mode = config['agents']['defaults']['compaction']['mode']
    if mode not in ['default', 'safeguard']:
        config['agents']['defaults']['compaction']['mode'] = 'safeguard'
except: pass
try:
    bs = config['agents']['defaults']['blockStreamingDefault']
    if bs not in ['on', 'off']:
        config['agents']['defaults']['blockStreamingDefault'] = 'off'
except: pass
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
PYEOF
}

# ==================== 主流程 ====================
rotate_log "\$LOG_FILE" \$MAX_LOG_LINES
rotate_log "\$HISTORY_FILE" 5000

echo "[\$(date)] === 开始健康检查 (v2.3.0, $OS) ===" >> "\$LOG_FILE"

if health_check; then
    echo "[\$(date)] 健康检查通过" >> "\$LOG_FILE"
    exit 0
fi

echo "[\$(date)] 健康检查失败，开始恢复" >> "\$LOG_FILE"
send_notification "OpenClaw 恢复" "检测到服务异常，开始自动恢复..."

# 验证并尝试重启
if [ -f "\$CONFIG_FILE" ]; then
    if validate_config "\$CONFIG_FILE"; then
        openclaw gateway restart 2>&1 >> "\$LOG_FILE"
        sleep 5
        if health_check; then
            echo "[\$(date)] 重启成功" >> "\$LOG_FILE"
            send_notification "OpenClaw 恢复成功" "服务已正常启动"
            exit 0
        fi
    else
        fix_config "\$CONFIG_FILE"
        openclaw gateway restart 2>&1 >> "\$LOG_FILE"
        sleep 5
        if health_check; then
            echo "[\$(date)] 修复并重启成功" >> "\$LOG_FILE"
            send_notification "OpenClaw 恢复成功" "配置已自动修复"
            exit 0
        fi
    fi
fi

# 回滚
for BACKUP in \$(ls -t "\$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | head -\$MAX_RETRIES); do
    validate_config "\$BACKUP" || continue
    cp "\$BACKUP" "\$CONFIG_FILE"
    openclaw gateway restart 2>&1 >> "\$LOG_FILE"
    sleep 5
    if health_check; then
        echo "[\$(date)] 回滚成功: \$BACKUP" >> "\$LOG_FILE"
        send_notification "OpenClaw 恢复成功" "已回滚到备份"
        exit 0
    fi
done

# 保底配置
if [ -f "\$SAFE_CONFIG" ] && validate_config "\$SAFE_CONFIG"; then
    cp "\$SAFE_CONFIG" "\$CONFIG_FILE"
    openclaw gateway restart 2>&1 >> "\$LOG_FILE"
    sleep 5
    if health_check; then
        echo "[\$(date)] 保底配置启动成功" >> "\$LOG_FILE"
        send_notification "OpenClaw 恢复成功" "使用保底配置启动"
        exit 0
    fi
fi

echo "[\$(date)] 恢复失败，需要人工干预" >> "\$LOG_FILE"
send_notification "OpenClaw 恢复失败" "自动恢复失败，请手动检查"
exit 1
RECOVER_EOF

chmod +x "$INSTALL_DIR/scripts/generated/recover.sh"

# ==================== 生成平台适配的备份脚本 ====================
cat > "$INSTALL_DIR/scripts/generated/backup.sh" << BACKUP_EOF
#!/bin/bash
# OpenClaw 智能备份 - $OS 适配版

CONFIG_FILE="\$HOME/.openclaw/openclaw.json"
AUTH_FILE="\$HOME/.openclaw/agents/main/agent/auth-profiles.json"
AUTH_STATE="\$HOME/.openclaw/agents/main/agent/auth-state.json"
BACKUP_DIR="\$HOME/.openclaw/backups"
LOG_FILE="\$HOME/.openclaw/logs/backup.log"

mkdir -p "\$BACKUP_DIR" "\$HOME/.openclaw/logs"

backup_config() {
    local reason="\$1"
    local timestamp=\$(date +%Y%m%d_%H%M%S)

    [ -f "\$CONFIG_FILE" ] && cp "\$CONFIG_FILE" "\$BACKUP_DIR/openclaw.json.bak.\$timestamp"
    [ -f "\$AUTH_FILE" ] && cp "\$AUTH_FILE" "\$BACKUP_DIR/auth-profiles.json.bak.\$timestamp"
    [ -f "\$AUTH_STATE" ] && cp "\$AUTH_STATE" "\$BACKUP_DIR/auth-state.json.bak.\$timestamp"

    echo "[\$(date)] 备份完成 - 原因: \$reason" >> "\$LOG_FILE"

    # 清理：保留最近20个 + 7天历史
    ls -t "\$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
    ls -t "\$BACKUP_DIR"/auth-profiles.json.bak.* 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
    find "\$BACKUP_DIR" -name "*.bak.*" -mtime +7 -type f -delete 2>/dev/null
}

if [ "\$1" == "daily" ]; then
    today=\$(date +%Y%m%d)
    ls -t "\$BACKUP_DIR"/openclaw.json.bak.\${today}_* 2>/dev/null | head -1 | grep -q . || backup_config "每日自动备份"
else
    backup_config "手动备份"
    echo "备份完成！"
fi
BACKUP_EOF

chmod +x "$INSTALL_DIR/scripts/generated/backup.sh"

# ==================== 安装保底配置 ====================
echo "[3/5] 安装保底配置..."
if [ -f "$HOME/.openclaw/safe-mode.json" ]; then
    echo "  保底配置已存在，跳过"
else
    cp "$SCRIPT_DIR/../safe-mode.json" "$HOME/.openclaw/safe-mode.json"
    echo "  已创建"
fi

# ==================== 首次备份 ====================
echo "[4/5] 创建首次备份..."
bash "$INSTALL_DIR/scripts/generated/backup.sh"

# ==================== 定时任务 ====================
echo "[5/5] 设置定时任务..."
case "$OS" in
    macos|linux)
        CRON_RECOVER="*/5 * * * * bash $INSTALL_DIR/scripts/generated/recover.sh"
        CRON_DAILY="0 2 * * * bash $INSTALL_DIR/scripts/generated/backup.sh daily"
        (crontab -l 2>/dev/null | grep -v "openclaw-recovery"; echo "$CRON_RECOVER"; echo "$CRON_DAILY") | crontab -
        echo "  cron 定时任务已设置"
        ;;
    windows)
        echo ""
        echo "  ⚠️  Windows 请手动设置定时任务："
        echo "  1. 打开「任务计划程序」"
        echo "  2. 创建任务 → 触发器 → 每 5 分钟"
        echo "  3. 操作 → 启动程序: bash $INSTALL_DIR/scripts/generated/recover.sh"
        echo ""
        echo "  或使用 PowerShell（管理员）："
        echo "  \$action = New-ScheduledTaskAction -Execute 'bash' -Argument '$INSTALL_DIR/scripts/generated/recover.sh'"
        echo "  \$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)"
        echo "  Register-ScheduledTask -TaskName 'OpenClaw-Recovery' -Action \$action -Trigger \$trigger"
        ;;
esac

echo ""
echo "=== 安装完成 ✅ ==="
echo ""
echo "系统: $OS"
echo "日志: ~/.openclaw/logs/"
echo "备份: ~/.openclaw/backups/"
echo ""
echo "手动操作:"
echo "  备份: bash $INSTALL_DIR/scripts/generated/backup.sh"
echo "  检查: bash $INSTALL_DIR/scripts/generated/recover.sh"
echo "  卸载: bash $INSTALL_DIR/scripts/uninstall.sh"
