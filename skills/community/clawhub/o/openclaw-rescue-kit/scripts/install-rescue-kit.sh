#!/bin/bash
# OpenClaw 自救套件一键安装脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_DIR="$OPENCLAW_HOME/logs"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

print_step() { echo -e "\n${CYAN}${BOLD}━━━ $1 ━━━${NC}"; }
print_info() { echo -e "  ${BLUE}ℹ${NC}  $1"; }
print_success() { echo -e "  ${GREEN}✅${NC} $1"; }
print_warn() { echo -e "  ${YELLOW}⚠️${NC}  $1"; }
print_error() { echo -e "  ${RED}❌${NC} $1"; }
print_todo() { echo -e "  ${YELLOW}➜${NC}  $1"; }

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "linux"
    fi
}

OS=$(detect_os)

# 检查依赖
check_dependencies() {
    print_step "步骤 1/7 · 检查依赖"
    local missing=()
    for cmd in bash jq curl; do
        if command -v "$cmd" >/dev/null 2>&1; then
            print_success "$cmd"
        else
            print_error "$cmd 未安装"
            missing+=("$cmd")
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        echo ""
        print_error "缺少依赖，请先安装:"
        if [ "$OS" = "macos" ]; then
            print_todo "brew install ${missing[*]}"
        else
            print_todo "sudo apt install ${missing[*]}"
        fi
        return 1
    fi
    command -v lsof >/dev/null 2>&1 || print_warn "建议安装 lsof (brew/apt install lsof)"
}

# 创建目录
create_directories() {
    print_step "步骤 2/7 · 创建目录"
    mkdir -p "$OPENCLAW_HOME/scripts"
    mkdir -p "$LOG_DIR"
    mkdir -p "$OPENCLAW_HOME/backups"
    print_success "$OPENCLAW_HOME/scripts/"
    print_success "$LOG_DIR"
    print_success "$OPENCLAW_HOME/backups/"
}

# 安装脚本
install_scripts() {
    print_step "步骤 3/7 · 安装脚本"
    local scripts=(
        "core.sh"
        "gateway-watchdog.sh"
        "gateway-start.sh"
        "health-check.sh"
        "security-hardening.sh"
        "notify.sh"
        "log-cleaner.sh"
        "git-tag.sh"
        "safe-config-modify.sh"
    )
    local installed=0
    local skipped=0
    for script in "${scripts[@]}"; do
        if [ ! -f "$SCRIPT_DIR/$script" ]; then
            print_warn "$script (源文件不存在)"
            ((skipped++)) || true
            continue
        fi
        local target="$OPENCLAW_HOME/scripts/$script"
        if [ "$SCRIPT_DIR/$script" = "$target" ]; then
            print_info "$script (已在目标位置)"
            ((skipped++)) || true
            continue
        fi
        if [ -f "$target" ] && cmp -s "$SCRIPT_DIR/$script" "$target" 2>/dev/null; then
            print_info "$script (已是最新)"
            ((skipped++)) || true
            continue
        fi
        cp "$SCRIPT_DIR/$script" "$target"
        chmod +x "$target"
        print_success "$script"
        ((installed++)) || true
    done
    echo ""
    print_info "总计: 安装 $installed 个, 跳过 $skipped 个"
}

# 生成配置文件
generate_config() {
    print_step "步骤 4/7 · 生成配置"
    local notify_conf="$OPENCLAW_HOME/notify.conf"
    if [ ! -f "$notify_conf" ]; then
        cat > "$notify_conf" <<'EOF'
# OpenClaw 告警通知配置
# 请填入您的 webhook 地址

# 飞书机器人 Webhook
FEISHU_WEBHOOK_URL=""

# Telegram 机器人
# TELEGRAM_BOT_TOKEN=""
# TELEGRAM_CHAT_ID=""

# 企业微信机器人
# WECHAT_WEBHOOK_URL=""

# 钉钉机器人
# DINGTALK_WEBHOOK_URL=""
EOF
        print_success "notify.conf (请编辑填入 Webhook)"
    else
        print_info "notify.conf (已存在，跳过)"
    fi
}

# macOS LaunchAgent 安装
install_launchagents() {
    print_step "步骤 7/7 · 定时任务 (LaunchAgent)"
    local plist_dir="$HOME/Library/LaunchAgents"
    local src_dir="$SKILL_DIR/launchagents"
    local tmp_dir="$OPENCLAW_HOME/launchagents-ready"

    if [ ! -d "$src_dir" ]; then
        print_warn "LaunchAgent 配置目录不存在，跳过"
        return 0
    fi

    # 生成已替换占位符的 plist
    mkdir -p "$tmp_dir"
    for src in "$src_dir"/*.plist; do
        [ -f "$src" ] || continue
        local fname=$(basename "$src")
        sed "s|__USER_HOME__|$HOME|g" "$src" > "$tmp_dir/$fname"
    done
    print_success "plist 已生成到: $tmp_dir"

    mkdir -p "$plist_dir"

    local services=("watchdog" "healthcheck" "logcleaner" "gittag")
    local need_manual=false
    local manual_cmds=""

    for svc in "${services[@]}"; do
        local plist="ai.openclaw.${svc}.plist"
        local src_tmp="$tmp_dir/$plist"
        local dst="$plist_dir/$plist"

        [ -f "$src_tmp" ] || continue

        if cp "$src_tmp" "$dst" 2>/dev/null; then
            print_success "$plist"
            if launchctl load "$dst" 2>/dev/null; then
                print_success "已加载: ai.openclaw.${svc}"
            elif launchctl list 2>/dev/null | grep -q "ai.openclaw.${svc}"; then
                print_info "已加载: ai.openclaw.${svc} (跳过)"
            else
                print_warn "加载失败: ai.openclaw.${svc}"
            fi
        else
            need_manual=true
            manual_cmds+="cp $src_tmp $dst"$'\n'
        fi
    done

    if [ "$need_manual" = true ]; then
        echo ""
        print_warn "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        print_warn "  macOS 安全策略限制，需要在终端手动执行以下命令"
        print_warn "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo -e "${BOLD}${manual_cmds}${NC}"
        echo -e "${BOLD}launchctl load ~/Library/LaunchAgents/ai.openclaw.*.plist${NC}"
        echo ""
        print_info "plist 文件已准备好，路径已正确替换，直接复制即可"
    fi
}

# Linux crontab 安装
install_crontab() {
    print_step "步骤 7/7 · 定时任务 (crontab)"
    if ! command -v crontab >/dev/null 2>&1; then
        print_warn "crontab 命令不可用，跳过"
        return 0
    fi

    local current_crontab
    current_crontab=$(crontab -l 2>/dev/null || echo "")

    if echo "$current_crontab" | grep -q "gateway-watchdog.sh"; then
        print_info "定时任务已配置，跳过"
        return 0
    fi

    local cron_entries="
# OpenClaw 自救套件定时任务
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# 每分钟检查网关（看门狗）
* * * * * /bin/bash $OPENCLAW_HOME/scripts/gateway-watchdog.sh >> $LOG_DIR/cron.log 2>&1

# 每小时健康检查
0 * * * * /bin/bash $OPENCLAW_HOME/scripts/health-check.sh >> $LOG_DIR/cron.log 2>&1

# 每天凌晨3点日志清理
0 3 * * * /bin/bash $OPENCLAW_HOME/scripts/log-cleaner.sh >> $LOG_DIR/cron.log 2>&1

# 每天凌晨2:30 Git 基线版本
30 2 * * * /bin/bash $OPENCLAW_HOME/scripts/git-tag.sh save-baseline >> $LOG_DIR/cron.log 2>&1
"
    (echo "$current_crontab"; echo "$cron_entries") | crontab -
    print_success "crontab 定时任务已配置"
}

# ==================== 修复网关 plist（端口冲突防护） ====================
patch_gateway_plist() {
    print_step "步骤 6/7 · 修复网关启动脚本（端口冲突防护）"
    local plist="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
    local start_script="$OPENCLAW_HOME/scripts/gateway-start.sh"

    if [ ! -f "$plist" ]; then
        print_warn "网关 plist 不存在: $plist"
        print_todo "请先运行: openclaw gateway install"
        return 0
    fi

    # 检查是否已经 patch 过
    if grep -q "gateway-start.sh" "$plist" 2>/dev/null; then
        print_info "网关 plist 已使用 gateway-start.sh，无需修改"
        return 0
    fi

    # 备份原 plist
    local backup="${plist}.backup.$(date +%Y%m%d%H%M%S)"
    cp "$plist" "$backup"
    print_success "已备份: $(basename "$backup")"

    # 读取原端口
    local port="18789"
    if grep -q "OPENCLAW_GATEWAY_PORT" "$plist"; then
        port=$(grep -A1 "OPENCLAW_GATEWAY_PORT" "$plist" | grep "<string>" | sed 's/.*<string>//;s/<\/string>.*//' | tr -d ' ')
    fi

    # 生成新的 ProgramArguments
    local tmp_plist="${plist}.tmp"
    /usr/libexec/PlistBuddy -c "Delete :ProgramArguments" "$plist" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Add :ProgramArguments array" "$plist" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Add :ProgramArguments:0 string /bin/bash" "$plist" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Add :ProgramArguments:1 string -c" "$plist" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Add :ProgramArguments:2 string sleep 5; exec bash $start_script" "$plist" 2>/dev/null || true

    # 设置端口环境变量
    /usr/libexec/PlistBuddy -c "Delete :EnvironmentVariables:OPENCLAW_GATEWAY_PORT" "$plist" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables:OPENCLAW_GATEWAY_PORT string $port" "$plist" 2>/dev/null || true

    print_success "网关 plist 已修复，使用 gateway-start.sh 启动"
    print_info "端口: $port"
    print_todo "重启网关生效: launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway"

    return 0
}

# 测试脚本
test_scripts() {
    print_step "步骤 5/7 · 验证脚本"
    local errors=0
    for script in "$OPENCLAW_HOME/scripts/"*.sh; do
        [ -f "$script" ] || continue
        if bash -n "$script" 2>/dev/null; then
            print_success "$(basename "$script")"
        else
            print_error "$(basename "$script") 语法错误"
            ((errors++)) || true
        fi
    done
    if [ "$errors" -gt 0 ]; then
        echo ""
        print_error "$errors 个脚本语法错误，请检查"
        return 1
    fi
}

# 主函数
main() {
    local auto_schedule=false
    while [ $# -gt 0 ]; do
        case "$1" in
            --auto-schedule) auto_schedule=true; shift ;;
            *) shift ;;
        esac
    done

    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║       🛡️  OpenClaw 自救套件 安装程序             ║${NC}"
    echo -e "${BOLD}║       OS: ${OS}                                  ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    check_dependencies || exit 1
    create_directories
    install_scripts
    generate_config
    test_scripts

    # 修复网关 plist（macOS）
    if [ "$OS" = "macos" ]; then
        patch_gateway_plist || true
    fi

    # 定时任务配置
    echo ""
    if [ "$OS" = "macos" ]; then
        if [ "$auto_schedule" = true ]; then
            install_launchagents
        elif [ -t 0 ]; then
            read -p "  是否配置 LaunchAgent 定时任务? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                install_launchagents
            else
                print_info "跳过定时任务，稍后运行: bash $0 --auto-schedule"
            fi
        else
            print_info "非交互模式，跳过定时任务"
            print_todo "稍后运行: bash $0 --auto-schedule"
        fi
    else
        if [ "$auto_schedule" = true ]; then
            install_crontab
        elif [ -t 0 ]; then
            read -p "  是否配置 crontab 定时任务? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                install_crontab
            else
                print_info "跳过定时任务，稍后运行: bash $0 --auto-schedule"
            fi
        else
            print_info "非交互模式，跳过定时任务"
            print_todo "稍后运行: bash $0 --auto-schedule"
        fi
    fi

    # 安装完成
    echo ""
    echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}${BOLD}║              ✅  安装完成!                        ║${NC}"
    echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${BOLD}脚本位置:${NC} $OPENCLAW_HOME/scripts/"
    echo -e "  ${BOLD}日志目录:${NC} $LOG_DIR"
    echo ""
    echo -e "  ${BOLD}下一步:${NC}"
    echo -e "  ${YELLOW}1.${NC} 编辑告警配置"
    echo -e "     vim $OPENCLAW_HOME/notify.conf"
    echo ""
    echo -e "  ${YELLOW}2.${NC} 保存安全配置"
    echo -e "     bash $OPENCLAW_HOME/scripts/security-hardening.sh --save-safe"
    echo ""
    echo -e "  ${YELLOW}3.${NC} 保存 Git 安全版本"
    echo -e "     bash $OPENCLAW_HOME/scripts/git-tag.sh save-safe"
    echo ""
    echo -e "  ${YELLOW}4.${NC} 测试告警"
    echo -e "     bash $OPENCLAW_HOME/scripts/notify.sh -l INFO '部署完成'"
    echo ""
    echo -e "  ${BOLD}快速使用:${NC}"
    echo -e "  bash $OPENCLAW_HOME/scripts/core.sh          ${CYAN}# 查看状态${NC}"
    echo -e "  bash $OPENCLAW_HOME/scripts/health-check.sh  ${CYAN}# 健康检查${NC}"
    echo -e "  bash $OPENCLAW_HOME/scripts/git-tag.sh list  ${CYAN}# 查看配置快照${NC}"
    echo ""
}

main "$@"
