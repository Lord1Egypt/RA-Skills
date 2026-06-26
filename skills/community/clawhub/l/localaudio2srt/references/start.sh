#!/bin/bash
# MLX Whisper 转录 + 翻译工具 — 一键启动脚本

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODELS_DIR="$PROJECT_DIR/models"
SERVER_PID=""
FRONTEND_PID=""

# ─── 模型配置 ─────────────────────────────────────────────
# ModelScope 模型 ID 与本地目录
WHISPER_MODEL_ID="mlx-community/whisper-large-v3-turbo-4bit"
WHISPER_MODEL_DIR="$MODELS_DIR/whisper-large-v3-turbo"

QWEN_MODEL_ID="mlx-community/Qwen2.5-3B-Instruct-4bit"
QWEN_MODEL_DIR="$MODELS_DIR/Qwen2.5-3B-Instruct-4bit"

# ─── 清理函数 ─────────────────────────────────────────────
cleanup() {
    echo ""
    echo "[停止] 正在关闭服务..."
    [ -n "$SERVER_PID" ] && kill $SERVER_PID 2>/dev/null
    [ -n "$FRONTEND_PID" ] && kill $FRONTEND_PID 2>/dev/null
    echo "[完成] 已停止"
    exit 0
}

trap cleanup INT TERM

# ─── 模型检测与下载 ─────────────────────────────────────
# 检查目录是否存在且有模型文件（不止 README）
model_dir_has_files() {
    local dir="$1"
    # 目录存在且至少有 2 个文件（排除只有 README 的情况）
    [ -d "$dir" ] && [ "$(ls -1 "$dir" 2>/dev/null | wc -l)" -ge 2 ]
}

# 确保 modelscope 可用（安装或使用 python -m）
ensure_modelscope() {
    if python3 -c "import modelscope" 2>/dev/null; then
        echo "  ✓ modelscope 已安装"
        return 0
    fi
    echo "  [安装] modelscope（模型下载工具）..."
    pip3 install modelscope -q 2>&1 | tail -3
    if python3 -c "import modelscope" 2>/dev/null; then
        echo "  ✓ modelscope 安装成功"
        return 0
    fi
    echo "  ✗ modelscope 安装失败，将尝试手动下载"
    return 1
}

# 用 modelscope CLI 下载模型
download_model() {
    local model_id="$1"
    local local_dir="$2"
    local model_name="$(basename "$local_dir")"

    echo ""
    echo "[下载] $model_name"
    echo "  来源: ModelScope ($model_id)"
    echo "  目标: $local_dir"
    echo "  （首次下载约需 5~10 分钟，请耐心等待）"
    echo ""

    mkdir -p "$local_dir"
    python3 -m modelscope.cli.download \
        --model "$model_id" \
        --local_dir "$local_dir" \
        2>&1 | grep -v "^$" | tail -20

    if model_dir_has_files "$local_dir"; then
        echo "  ✓ $model_name 下载完成"
        return 0
    else
        echo "  ✗ $model_name 下载失败"
        return 1
    fi
}

# 主：检测并下载缺失模型
check_and_download_models() {
    local need_download=false

    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  检测模型文件                                ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    # 检查 Whisper 模型
    if model_dir_has_files "$WHISPER_MODEL_DIR"; then
        echo "  ✓ Whisper 模型: $WHISPER_MODEL_DIR"
    else
        echo "  ✗ Whisper 模型缺失: $WHISPER_MODEL_DIR"
        need_download=true
    fi

    # 检查 Qwen 模型
    if model_dir_has_files "$QWEN_MODEL_DIR"; then
        echo "  ✓ Qwen 翻译模型: $QWEN_MODEL_DIR"
    else
        echo "  ✗ Qwen 翻译模型缺失: $QWEN_MODEL_DIR"
        need_download=true
    fi

    if [ "$need_download" = false ]; then
        echo ""
        echo "  所有模型已就绪，跳过下载"
        return 0
    fi

    # 需要下载 → 确保 modelscope 可用
    echo ""
    ensure_modelscope || {
        echo ""
        echo "╔══════════════════════════════════════════════╗"
        echo "║  无法自动下载模型，请手动操作                  ║"
        echo "╚══════════════════════════════════════════════╝"
        echo ""
        echo "  手动下载命令（在 $PROJECT_DIR 目录下执行）："
        echo ""
        echo "  pip3 install modelscope"
        echo "  python3 -m modelscope.cli.download --model $WHISPER_MODEL_ID --local_dir $WHISPER_MODEL_DIR"
        echo "  python3 -m modelscope.cli.download --model $QWEN_MODEL_ID --local_dir $QWEN_MODEL_DIR"
        echo ""
        echo "  或访问 ModelScope 网页手动下载："
        echo "  https://www.modelscope.cn/models/$WHISPER_MODEL_ID"
        echo "  https://www.modelscope.cn/models/$QWEN_MODEL_ID"
        echo ""
        read -p "  按 Enter 退出，完成手动下载后重新运行 start.sh..." DUMMY
        exit 1
    }

    # 下载缺失的模型
    if ! model_dir_has_files "$WHISPER_MODEL_DIR"; then
        download_model "$WHISPER_MODEL_ID" "$WHISPER_MODEL_DIR" || {
            echo "  Whisper 模型下载失败，请手动操作（见上方提示）"
            exit 1
        }
    fi

    if ! model_dir_has_files "$QWEN_MODEL_DIR"; then
        download_model "$QWEN_MODEL_ID" "$QWEN_MODEL_DIR" || {
            echo "  Qwen 模型下载失败，请手动操作（见上方提示）"
            exit 1
        }
    fi

    echo ""
    echo "  所有模型下载完成！"
}

# ─── 主流程 ─────────────────────────────────────────────
echo "╔══════════════════════════════════════════════╗"
echo "║  MLX Whisper 转录 + 翻译工具                ║"
echo "║  后端: http://localhost:8765                 ║"
echo "║  前端: http://localhost:3000                  ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Step 1: 检测并下载模型
check_and_download_models

# Step 2: 启动后端
echo ""
echo "[启动] Python 后端服务..."
python3 "$PROJECT_DIR/server/transcribe_server.py" 8765 &
SERVER_PID=$!
echo "  后端 PID: $SERVER_PID"

# 等待后端启动
sleep 2

# 检查后端是否启动成功
if curl -s http://localhost:8765/api/health > /dev/null 2>&1; then
    echo "  ✓ 后端启动成功"
else
    echo "  ⚠ 后端可能还在初始化中..."
fi

# Step 3: 启动前端
echo ""
echo "[启动] 前端开发服务器..."
cd "$PROJECT_DIR"
npm run dev -- --port 3000 &
FRONTEND_PID=$!
echo "  前端 PID: $FRONTEND_PID"

echo ""
echo "================================================================"
echo "  服务已启动！"
echo "  前端: http://localhost:3000"
echo "  后端: http://localhost:8765"
echo "  按 Ctrl+C 停止所有服务"
echo "================================================================"
echo ""

# 等待任意进程退出
wait
