#!/usr/bin/env bash
#
# Meeting Assistant - 交互式安装脚本
# Usage: bash meeting-assistant/scripts/setup.sh
#

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd "$SKILL_DIR/.." && pwd)"
CONFIG_DIR="$HOME/.config/meeting-assistant"
GCP_DIR="$HOME/.config/gcp"
RECORDING_DIR="$REPO_DIR/meeting-recordings"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PYTHON_BIN="$(command -v python3 || echo /usr/bin/python3)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}ℹ️${NC} $1"; }
ok()    { echo -e "${GREEN}✅${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠️${NC} $1"; }
err()   { echo -e "${RED}❌${NC} $1"; }
header(){ echo; echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "${BLUE}  $1${NC}"; echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; }
prompt(){ echo -ne "${YELLOW}➡️${NC} $1 "; }

check_repo_layout() {
    if [[ ! -f "$SCRIPT_DIR/record_audio.py" || ! -f "$SCRIPT_DIR/audio_daemon.swift" ]]; then
        err "setup.sh 必须在完整仓库中运行，不能直接 curl | bash。"
        echo "请使用："
        echo "  git clone https://github.com/Nowhitestar/meeting-assistant.git"
        echo "  cd meeting-assistant"
        echo "  bash meeting-assistant/scripts/setup.sh"
        exit 1
    fi
}

# ─── Step 0: Check system ────────────────────────────

check_system() {
    header "系统检查"

    if [[ "$(uname)" != "Darwin" ]]; then
        err "此脚本仅支持 macOS"
        exit 1
    fi
    ok "macOS $(sw_vers -productVersion)"

    if ! command -v brew &>/dev/null; then
        warn "Homebrew 未安装，正在安装..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ok "Homebrew 已安装"
    else
        ok "Homebrew $(brew --version | head -1)"
    fi

    if command -v python3 &>/dev/null; then
        ok "Python $(python3 --version)"
    else
        err "Python 3 未安装，请先安装: brew install python@3.14"
        exit 1
    fi
}

# ─── Step 1: Install system deps ─────────────────────

install_deps() {
    header "安装系统依赖"

    local pkgs=()
    local optional=()

    echo "  将安装以下软件包："
    echo "    - ffmpeg / sox       (音频检查与备用处理)"
    echo "    - whisper-cpp        (本地转录 whisper-cli)"
    echo "    - terminal-notifier  (系统通知)"
    echo "    - steipete/tap/gogcli (Google 日历 CLI)"
    echo "    - cloudflared        (日历 webhook 隧道)"
    echo

    prompt "继续安装？[Y/n]"
    read -r ans
    if [[ "$ans" =~ ^[nN] ]]; then
        warn "跳过依赖安装"
        return
    fi

    brew install sox ffmpeg whisper-cpp terminal-notifier 2>&1 | tail -1
    ok "音频/转录/通知工具安装完成"

    brew install steipete/tap/gogcli 2>&1 | tail -1
    ok "gog CLI 安装完成"

    brew install cloudflared 2>&1 | tail -1
    ok "cloudflared 安装完成"
}

# ─── Step 2: Audio setup ─────────────────────────────

setup_audio() {
    header "音频配置"

    echo "  Meeting Assistant 默认使用原生 macOS ScreenCaptureKit + AVFoundation。"
    echo "  不需要 BlackHole、多输出设备或虚拟声卡。"
    echo
    echo "  首次使用 AudioDaemon.app 时，请授权："
    echo "    - 麦克风"
    echo "    - 屏幕与系统音频录制"
    echo

    MIC_DEVICE=":0"
    SYS_DEVICE=":1"  # 仅 SoX fallback 使用；daemon 后端会忽略

    ok "音频后端: daemon (ScreenCaptureKit 系统音频 + AVFoundation 麦克风)"
}

# ─── Step 3: Create config ───────────────────────────

create_config() {
    header "创建配置文件"

    if [[ -f "$CONFIG_DIR/config.json" ]]; then
        warn "配置文件已存在: $CONFIG_DIR/config.json"
        prompt "覆盖？[y/N]"
        read -r ans
        if [[ ! "$ans" =~ ^[yY] ]]; then
            info "保留现有配置"
            return
        fi
    fi

    mkdir -p "$CONFIG_DIR"

    cat > "$CONFIG_DIR/config.json" <<CONFIG
{
  "calendars": [
    {
      "type": "google",
      "enabled": false,
      "gog_account": "",
      "watch_calendars": ["primary"]
    }
  ],
  "audio": {
    "backend": "daemon",
    "mic_device": "$MIC_DEVICE",
    "system_audio_device": "$SYS_DEVICE",
    "output_dir": "$RECORDING_DIR",
    "format": "wav",
    "silence_threshold": 0.01,
    "silence_duration_sec": 300,
    "half_duplex": true
  },
  "transcription": {
    "mode": "local",
    "language": "zh",
    "local_model_path": "",
    "whisper_cli": "whisper-cli"
  },
  "llm": {
    "enabled": false
  },
  "output": {
    "channel": "file"
  },
  "meeting_detection": {
    "enabled": true,
    "interval_sec": 10,
    "stable_sec": 15,
    "prompt_cooldown_sec": 1800
  }
}
CONFIG

    mkdir -p "$RECORDING_DIR"
    ok "配置文件已创建: $CONFIG_DIR/config.json"
    ok "录制目录已创建: $RECORDING_DIR"
}

# ─── Step 4: Compile native helpers ──────────────────

compile_scanner() {
    header "编译窗口扫描工具"

    info "window_scanner 用于在无需辅助功能权限的情况下读取窗口标题"
    echo

    if command -v swiftc &>/dev/null; then
        swiftc -o "$SCRIPT_DIR/window_scanner" \
               "$SCRIPT_DIR/window_scanner.swift" \
               -framework Cocoa 2>&1 | tail -1
        chmod +x "$SCRIPT_DIR/window_scanner"
        ok "window_scanner 编译成功"

        echo
        echo "  首次使用需要授权辅助功能权限。即将打开 window_scanner..."
        echo "  当系统弹出对话框时，请点击「允许」或「好」。"
        echo
        prompt "准备好了吗？按回车继续..."
        read -r

        open "$SCRIPT_DIR/window_scanner"
        sleep 2
        ok "权限对话框已弹出，请点击允许"
        prompt "点完允许后按回车继续..."
        read -r

        # Verify
        local result
        result=$("$SCRIPT_DIR/window_scanner" 2>&1)
        if [[ "$result" == "[]" ]]; then
            warn "window_scanner 未检测到窗口，可能权限未授权"
            warn "请手动添加: 系统设置 → 隐私与安全性 → 辅助功能"
            warn "路径: $SCRIPT_DIR/window_scanner"
            prompt "继续？[Y/n]"
            read -r ans
            if [[ "$ans" =~ ^[nN] ]]; then exit 1; fi
        else
            local count
            count=$(echo "$result" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null)
            ok "window_scanner 工作正常，检测到 $count 个窗口"
        fi
    else
        warn "Swift 编译器未安装（swiftc 不可用），跳过编译"
        warn "后续可以手动编译: xcode-select --install"
    fi
}

compile_audio_daemon() {
    header "编译并签名 AudioDaemon"

    local build_script="$SCRIPT_DIR/build_audio_daemon.sh"
    if [[ ! -x "$build_script" ]]; then
        warn "AudioDaemon build script 不存在或不可执行，跳过"
        return
    fi

    "$build_script"
    ok "AudioDaemon.app 已使用固定 codesign identity 签名"

    echo
    echo "  AudioDaemon 负责捕获系统音频和麦克风。"
    echo "  首次使用需要授权：系统设置 → 隐私与安全性 → 屏幕与系统音频录制 / 麦克风。"
    echo "  如果系统弹出权限对话框，请点击「允许」。"

    open "$SCRIPT_DIR/AudioDaemon.app"
    sleep 4
    local status
    status=$(echo '{"action":"status"}' | nc -w 2 -U "$HOME/.config/meeting-assistant/audio_daemon.sock" 2>/dev/null || true)
    if echo "$status" | grep -q '"sysReady":true' && echo "$status" | grep -q '"micReady":true'; then
        ok "AudioDaemon 捕获权限正常"
    else
        warn "AudioDaemon 尚未 ready: $status"
        warn "请在系统设置中授权 AudioDaemon.app，然后重新运行测试"
    fi
}

# ─── Step 5: Google Calendar setup ───────────────────

setup_calendar() {
    header "Google 日历配置（可选）"

    echo "  Meeting Assistant 可以读取 Google 日历来自动提醒和录制会议。"
    echo "  跳过此步骤也可以使用，只是不会有日历自动同步功能。"
    echo

    prompt "配置 Google 日历？[y/N]"
    read -r ans
    if [[ ! "$ans" =~ ^[yY] ]]; then
        warn "跳过日历配置"
        return
    fi

    # Check gog
    if ! command -v gog &>/dev/null; then
        err "gog 未安装，请先运行安装步骤"
        return
    fi

    # OAuth credentials
    echo
    echo "  需要 Google Cloud OAuth 凭据："
    echo "    1. 打开 https://console.cloud.google.com/"
    echo "    2. 创建项目或选择已有项目"
    echo "    3. 启用 Google Calendar API"
    echo "    4. 凭据 → 创建凭据 → OAuth 客户端 ID → 桌面应用"
    echo "    5. 下载 JSON 文件"
    echo

    prompt "请输入 client_secret.json 的路径（或拖入终端）:"
    read -r cred_path
    cred_path="${cred_path/#\~/$HOME}"
    cred_path="$(eval echo "$cred_path")"

    if [[ ! -f "$cred_path" ]]; then
        err "文件不存在: $cred_path"
        return
    fi

    mkdir -p "$GCP_DIR"
    cp "$cred_path" "$GCP_DIR/client_secret.json"
    ok "凭据已保存到 $GCP_DIR/client_secret.json"

    # gog auth
    echo
    gog auth credentials "$GCP_DIR/client_secret.json"
    ok "gog 凭据已注册"

    prompt "请输入你的 Google 邮箱 (如 user@example.com):"
    read -r email

    echo
    info "即将打开浏览器进行 OAuth 授权..."
    echo "  授权后浏览器可能会显示「无法连接」，这是正常的。"
    echo "  切换到终端，gog 会自动完成授权。"
    echo

    gog auth add "$email" --services calendar

    # Verify
    info "验证日历访问..."
    gog auth list
    ok "gog 授权完成"

    # Update config
    local tmp
    tmp=$(mktemp)
    python3 -c "
import json
cfg = json.load(open('$CONFIG_DIR/config.json'))
for cal in cfg.get('calendars', []):
    if cal.get('type') == 'google':
        cal['enabled'] = True
        cal['gog_account'] = '$email'
json.dump(cfg, open('$tmp', 'w'), indent=2, ensure_ascii=False)
" 2>/dev/null
    mv "$tmp" "$CONFIG_DIR/config.json"
    ok "配置文件已更新"

    # Test
    echo
    info "测试日历读取..."
    gog calendar events "$email" --from "$(date -u +%Y-%m-%dT00:00:00Z)" --to "$(date -u -v+1d +%Y-%m-%dT00:00:00Z)" 2>&1
    ok "日历读取成功"
}

# ─── Step 6: Install LaunchAgents ────────────────────

install_launchagents() {
    header "安装 LaunchAgent 常驻服务"

    mkdir -p "$LAUNCH_AGENTS_DIR"

    # Helper function to fix paths in plist
    install_plist() {
        local src="$1"
        local name="$2"
        local dest="$LAUNCH_AGENTS_DIR/$name"

        if [[ -f "$dest" ]]; then
            launchctl unload "$dest" 2>/dev/null || true
        fi

        cp "$src" "$dest"

        # Replace placeholder paths with real paths
        sed -i '' \
            -e "s|__PYTHON__|$PYTHON_BIN|g" \
            -e "s|__HOME__|$HOME|g" \
            -e "s|__SCRIPT_DIR__|$SCRIPT_DIR|g" \
            -e "s|__PATH__|/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin|g" \
            "$dest" 2>/dev/null || true

        # If plist has hardcoded paths, update if needed
        if grep -q "$HOME" "$dest"; then
            ok "$name: 已复制"
        else
            # For plists with absolute paths, just copy
            ok "$name: 已复制"
        fi
    }

    local plist_dir="$SCRIPT_DIR"

    # AudioDaemon (native system audio + mic capture)
    if [[ -f "$plist_dir/com.meetingassistant.audiodaemon.plist" ]]; then
        install_plist "$plist_dir/com.meetingassistant.audiodaemon.plist" "com.meetingassistant.audiodaemon.plist"
        launchctl load "$LAUNCH_AGENTS_DIR/com.meetingassistant.audiodaemon.plist" 2>/dev/null || true
        ok "audiodaemon 已加载"
    fi

    # Scheduler
    if [[ -f "$plist_dir/com.meetingassistant.scheduler.plist" ]]; then
        install_plist "$plist_dir/com.meetingassistant.scheduler.plist" "com.meetingassistant.scheduler.plist"
        launchctl load "$LAUNCH_AGENTS_DIR/com.meetingassistant.scheduler.plist" 2>/dev/null || true
        ok "scheduler 已加载"
    fi

    # Detector
    if [[ -f "$plist_dir/com.meetingassistant.detector.plist" ]]; then
        install_plist "$plist_dir/com.meetingassistant.detector.plist" "com.meetingassistant.detector.plist"
        launchctl load "$LAUNCH_AGENTS_DIR/com.meetingassistant.detector.plist" 2>/dev/null || true
        ok "detector 已加载"
    fi

    # Calendar service (optional, only if gog configured)
    if [[ -f "$plist_dir/com.meetingassistant.calendar.plist" ]]; then
        prompt "安装日历推送服务（需要 Google 日历）？[y/N]"
        read -r ans
        if [[ "$ans" =~ ^[yY] ]]; then
            install_plist "$plist_dir/com.meetingassistant.calendar.plist" "com.meetingassistant.calendar.plist"
            launchctl load "$LAUNCH_AGENTS_DIR/com.meetingassistant.calendar.plist" 2>/dev/null || true
            ok "calendar 已加载"
        fi
    fi

    echo
    info "正在等待服务启动..."
    sleep 3
    launchctl list | grep com.meetingassistant
    ok "服务已安装"
}

# ─── Step 7: Test ────────────────────────────────────

run_tests() {
    header "功能验证"

    echo "  1/3 检测器测试"
    local detect_result
    detect_result=$(python3 "$SCRIPT_DIR/meeting_detector.py" once 2>&1)
    if echo "$detect_result" | grep -q "active"; then
        ok "检测器运行正常"
    else
        warn "检测器异常: $detect_result"
    fi

    echo "  2/3 日历测试"
    if python3 "$SCRIPT_DIR/check_meetings.py" today 2>&1; then
        ok "日历读取正常"
    else
        warn "日历读取异常（如果未配置日历则正常）"
    fi

    echo "  3/4 AudioDaemon 测试"
    local audio_status
    audio_status=$(echo '{"action":"status"}' | nc -w 2 -U "$HOME/.config/meeting-assistant/audio_daemon.sock" 2>/dev/null || true)
    if echo "$audio_status" | grep -q '"sysReady":true' && echo "$audio_status" | grep -q '"micReady":true'; then
        ok "AudioDaemon 运行正常"
    else
        warn "AudioDaemon 异常: $audio_status"
    fi

    echo "  4/4 通知测试"
    if command -v terminal-notifier &>/dev/null; then
        terminal-notifier -title "Meeting Assistant" -message "安装完成！" -sound default 2>/dev/null || true
        ok "通知测试通过"
    fi

    echo
    ok "安装验证完成！"
}

# ─── Summary ─────────────────────────────────────────

show_summary() {
    header "安装完成 🎉"

    echo "  Meeting Assistant 已安装并运行："
    echo
    echo "  📁 配置目录: $CONFIG_DIR"
    echo "  📁 录制目录: $RECORDING_DIR"
    echo "  📁 项目路径: $REPO_DIR"
    echo
    echo "  ⚡ 已运行的服务："
    launchctl list | grep com.meetingassistant 2>/dev/null | while IFS= read -r line; do
        pid=$(echo "$line" | awk '{print $1}')
        name=$(echo "$line" | awk '{print $3}')
        if [[ "$pid" != "-" ]]; then
            echo "     ✅ $name (pid=$pid)"
        else
            echo "     ❌ $name (未运行)"
        fi
    done
    echo
    echo "  📖 使用指南："
    echo "    bash meeting-assistant/scripts/setup.sh  # 重新运行此安装脚本"
    echo "    check_meetings.py today   # 查看今天会议"
    echo "    meeting_detector.py once  # 手动检测会议"
    echo
    echo "  🛠️  管理命令："
    echo "    launchctl list | grep com.meetingassistant  # 查看服务状态"
    echo "    launchctl unload ~/Library/LaunchAgents/com.meetingassistant.XXX.plist  # 停止服务"
    echo "    launchctl load   ~/Library/LaunchAgents/com.meetingassistant.XXX.plist  # 启动服务"
    echo
    echo "  ❓ 需要帮助？"
    echo "    README.md 中有完整文档"
    echo "    https://github.com/Nowhitestar/meeting-assistant"
}

# ─── Main ────────────────────────────────────────────

clear
echo -e "${BLUE}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║         Meeting Assistant 安装脚本       ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${NC}"
echo "  本脚本将引导你完成 Meeting Assistant 的安装和配置。"
echo "  全程大约需要 10-15 分钟。"
echo

prompt "开始安装？[Y/n]"
read -r ans
if [[ "$ans" =~ ^[nN] ]]; then
    echo "安装已取消"
    exit 0
fi

check_repo_layout
check_system
install_deps
setup_audio
create_config
compile_scanner
compile_audio_daemon
setup_calendar
install_launchagents
run_tests
show_summary

echo
info "安装完成！有任何问题请查看 README.md 或提交 GitHub Issue。"
