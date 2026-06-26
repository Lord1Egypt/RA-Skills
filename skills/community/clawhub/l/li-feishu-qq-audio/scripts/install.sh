#!/bin/bash
# Li_Feishu_Audio 技能安装脚本
# 用法：./install.sh [--force]
# 选项：--force 强制重新安装

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 加载公共库
source "$SCRIPT_DIR/common.sh"

# 设置目录变量
set_skill_dirs

# 加载已有配置（如果存在）
load_env_config 2>/dev/null || true

# 解析参数
FORCE_MODE=false
if [ "$1" == "--force" ]; then
    FORCE_MODE=true
    log_warn "强制重新安装模式"
fi

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║       Li_Feishu_Audio 技能安装脚本                 ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# 1. 检查系统依赖
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📋 1. 系统依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

dependencies_ok=true

# Python 检查
log_info "检查 Python 3.9+..."
if ! check_python_version "3.9"; then
    log_error "Python 3.9+ 未安装"
    echo "   安装命令: sudo apt install python3 python3-venv python3-pip"
    dependencies_ok=false
else
    log_ok "Python: $(python3 --version 2>&1)"
fi

# pip 检查
log_info "检查 pip3..."
if ! check_command pip3; then
    log_warn "pip3 未安装，尝试安装..."
    if command -v apt &>/dev/null; then
        sudo apt update && sudo apt install -y python3-pip || dependencies_ok=false
    elif command -v yum &>/dev/null; then
        sudo yum install -y python3-pip || dependencies_ok=false
    else
        dependencies_ok=false
    fi
else
    log_ok "pip3: $(pip3 --version 2>&1 | head -1)"
fi

# ffmpeg 检查
log_info "检查 ffmpeg..."
if ! check_command ffmpeg; then
    log_warn "ffmpeg 未安装，尝试安装..."
    if command -v apt &>/dev/null; then
        sudo apt update && sudo apt install -y ffmpeg || dependencies_ok=false
    elif command -v yum &>/dev/null; then
        sudo yum install -y ffmpeg || dependencies_ok=false
    else
        dependencies_ok=false
    fi
else
    log_ok "ffmpeg: $(ffmpeg -version 2>&1 | head -1)"
fi

# ffprobe 检查（用于音频验证）
log_info "检查 ffprobe..."
if ! check_command ffprobe; then
    log_warn "ffprobe 未安装，尝试安装..."
    if command -v apt &>/dev/null; then
        sudo apt install -y ffmpeg || true
    fi
else
    log_ok "ffprobe: 已安装"
fi

# jq 检查
log_info "检查 jq..."
if ! check_command jq; then
    log_warn "jq 未安装，尝试安装..."
    if command -v apt &>/dev/null; then
        sudo apt install -y jq || dependencies_ok=false
    elif command -v yum &>/dev/null; then
        sudo yum install -y jq || dependencies_ok=false
    else
        dependencies_ok=false
    fi
else
    log_ok "jq: $(jq --version 2>&1)"
fi

if [ "$dependencies_ok" = false ]; then
    log_error "依赖检查失败，请安装上述缺失的依赖后重试"
    exit 1
fi

# 2. 检查 uv
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📦 2. 检查 uv 包管理器"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

UV_DIR="$HOME/.local/bin"
UV_BIN="$UV_DIR/uv"

if check_command uv; then
    log_ok "uv: $(uv --version 2>&1)"
elif [ -f "$UV_BIN" ]; then
    log_ok "uv: $UV_BIN"
    export PATH="$UV_DIR:$PATH"
else
    log_info "安装 uv..."
    # 安全安装：下载到临时文件后执行，避免直接 curl|sh
    UV_INSTALL_SCRIPT="/tmp/uv-install-$$.sh"
    if curl -LsSf https://astral.sh/uv/install.sh -o "$UV_INSTALL_SCRIPT"; then
        # 基础安全检查：确保是 shell 脚本
        if head -1 "$UV_INSTALL_SCRIPT" | grep -qE '^#!(/bin/sh|/bin/bash|/usr/bin/env)'; then
            chmod +x "$UV_INSTALL_SCRIPT"
            if sh "$UV_INSTALL_SCRIPT"; then
                rm -f "$UV_INSTALL_SCRIPT"
                export PATH="$UV_DIR:$PATH"
                if check_command uv; then
                    log_ok "uv 安装成功: $(uv --version 2>&1)"
                else
                    log_error "uv 安装后仍无法找到"
                    exit 1
                fi
            else
                rm -f "$UV_INSTALL_SCRIPT"
                log_error "uv 安装失败"
                exit 1
            fi
        else
            rm -f "$UV_INSTALL_SCRIPT"
            log_error "下载的安装脚本无效"
            exit 1
        fi
    else
        log_error "uv 安装脚本下载失败"
        exit 1
    fi
fi

# 3. 创建虚拟环境
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🐍 3. 创建 Python 虚拟环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

VENV_DIR="${VENV_DIR:-${SKILL_DIR}/.venv}"
log_info "虚拟环境目录: $VENV_DIR"

if [ "$FORCE_MODE" = true ] && [ -d "$VENV_DIR" ]; then
    log_warn "强制模式：删除现有虚拟环境"
    rm -rf "$VENV_DIR"
fi

if check_venv "$VENV_DIR"; then
    log_ok "虚拟环境已存在"
else
    log_info "创建虚拟环境..."
    if uv venv --python 3.11 "$VENV_DIR" 2>/dev/null || uv venv "$VENV_DIR"; then
        log_ok "虚拟环境已创建"
    else
        log_error "虚拟环境创建失败"
        exit 1
    fi
fi

# 4. 安装 Python 依赖
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📚 4. 安装 Python 依赖"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

export HF_ENDPOINT=https://hf-mirror.com
log_info "使用 HuggingFace 镜像: $HF_ENDPOINT"

# 检查依赖
log_info "检查 faster-whisper..."
if "$VENV_DIR/bin/python" -c "import faster_whisper" 2>/dev/null && [ "$FORCE_MODE" = false ]; then
    log_ok "faster-whisper 已安装"
else
    log_info "安装 faster-whisper..."
    run_with_retry 3 "uv pip install faster-whisper -p $VENV_DIR" 3 || {
        log_warn "主源失败，尝试清华镜像..."
        uv pip install faster-whisper -p "$VENV_DIR" --index-url https://pypi.tuna.tsinghua.edu.cn/simple
    }
    log_ok "faster-whisper 安装完成"
fi

log_info "检查 edge-tts..."
if "$VENV_DIR/bin/python" -c "import edge_tts" 2>/dev/null && [ "$FORCE_MODE" = false ]; then
    log_ok "edge-tts 已安装"
else
    log_info "安装 edge-tts..."
    run_with_retry 3 "uv pip install edge-tts -p $VENV_DIR" 3 || {
        log_warn "主源失败，尝试清华镜像..."
        uv pip install edge-tts -p "$VENV_DIR" --index-url https://pypi.tuna.tsinghua.edu.cn/simple
    }
    log_ok "edge-tts 安装完成"
fi

# 5. 下载模型
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🤖 5. 下载语音识别模型"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

MODEL_DIR="${FAST_WHISPER_MODEL_DIR:-${HOME}/.fast-whisper-models}"
mkdir -p "$MODEL_DIR"
log_info "模型目录: $MODEL_DIR"

log_info "检查 tiny 模型..."
if "$VENV_DIR/bin/python" -c "
from faster_whisper import WhisperModel
try:
    model = WhisperModel('tiny', device='cpu', compute_type='int8', download_root='$MODEL_DIR', local_files_only=True)
    print('EXISTS')
except:
    exit(1)
" 2>/dev/null | grep -q "EXISTS" && [ "$FORCE_MODE" = false ]; then
    log_ok "tiny 模型已存在"
else
    log_info "下载 tiny 模型 (约 75MB)..."
    log_info "首次下载可能需要几分钟，请耐心等待..."
    
    run_with_retry 3 "$VENV_DIR/bin/python -c \"from faster_whisper import WhisperModel; print('开始下载...'); model = WhisperModel('tiny', device='cpu', compute_type='int8', download_root='$MODEL_DIR'); print('下载完成')\"" 5 || {
        log_error "模型下载失败，请检查网络或手动下载"
        exit 1
    }
    log_ok "tiny 模型下载完成"
fi

# 6. 创建配置文件
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ⚙️  6. 创建配置文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f "${SCRIPT_DIR}/.env.example" ]; then
    cat > "${SCRIPT_DIR}/.env.example" << 'EOF'
# Li_Feishu_Audio 配置文件
# 复制此文件为 .env 并填入实际值

# 飞书应用凭证 (必填)
# 从飞书开放平台获取：https://open.feishu.cn/app
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 可选配置
# VENV_DIR=/root/.openclaw/workspace/skills/li-feishu-audio/.venv
# FAST_WHISPER_MODEL_DIR=/root/.fast-whisper-models
# LOG_LEVEL=INFO
EOF
    log_ok "已创建 .env.example"
fi

if [ ! -f "${SCRIPT_DIR}/.env" ]; then
    cp "${SCRIPT_DIR}/.env.example" "${SCRIPT_DIR}/.env"
    log_ok "已创建 .env 配置文件"
    log_warn "⚠️  请编辑 scripts/.env 填入实际配置"
else
    log_ok "配置文件已存在"
fi

# 7. 设置脚本权限
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔧 7. 设置脚本权限"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

chmod +x "$SCRIPT_DIR"/*.sh
log_ok "脚本权限已设置"

# 8. 清理旧临时文件
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧹 8. 清理旧临时文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cleanup_old_temp_files "/tmp/tts-output-*.mp3" 24
log_ok "临时文件已清理"

# 9. 运行健康检查
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ 9. 运行健康检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if "$SCRIPT_DIR/healthcheck.sh" 2>/dev/null; then
    echo ""
    log_ok "安装完成并通过健康检查！"
else
    log_warn "安装完成，但健康检查发现问题，请查看上方输出"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  🎉 安装完成！"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  使用方法:"
echo "    TTS 测试:  ./scripts/tts-voice.sh \"你好世界\""
echo "    健康检查: ./scripts/healthcheck.sh"
echo ""
echo "  配置文件:"
echo "    ${SCRIPT_DIR}/.env"
echo ""