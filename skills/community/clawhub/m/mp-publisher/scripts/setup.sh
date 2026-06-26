#!/bin/bash
# ============================================================================
# 公众号发布环境初始化脚本
# ============================================================================

set -e

echo "=== 公众号发布环境初始化 ==="

# 创建工作目录
mkdir -p ~/.openclaw/workspace-work
mkdir -p ~/.openclaw/workspace-designer/images
mkdir -p ~/.openclaw/workspace-mp-editor

# 检查 Python 依赖
echo "[1/4] 检查 Python 依赖..."
pip3 install -q requests wechatpy 2>/dev/null || pip install -q requests wechatpy 2>/dev/null || true

# 创建配置文件模板
echo "[2/4] 创建配置文件模板..."

# 微信公众号配置
if [ ! -f ~/.openclaw/workspace-mp-editor/.env ]; then
    cat > ~/.openclaw/workspace-mp-editor/.env << 'EOF'
# 微信公众号配置
WECHAT_APP_ID=your_app_id_here
WECHAT_APP_SECRET=your_app_secret_here
EOF
    echo "     已创建 ~/.openclaw/workspace-mp-editor/.env (请填写配置)"
else
    echo "     ~/.openclaw/workspace-mp-editor/.env 已存在"
fi

# 配图API配置
if [ ! -f ~/.openclaw/workspace-designer/.env ]; then
    cat > ~/.openclaw/workspace-designer/.env << 'EOF'
# DMX API 配置（用于图片生成）
DMX_API_KEY=your_api_key_here
EOF
    echo "     已创建 ~/.openclaw/workspace-designer/.env (请填写配置)"
else
    echo "     ~/.openclaw/workspace-designer/.env 已存在"
fi

# 复制脚本到工作位置
echo "[3/4] 安装脚本..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 安装流程监控脚本
cp "$SCRIPT_DIR/workflow-monitor.py" ~/.openclaw/workspace/scripts/ 2>/dev/null || true
chmod +x ~/.openclaw/workspace/scripts/workflow-monitor.py 2>/dev/null || true

# 安装配图生成脚本
cp "$SCRIPT_DIR/../lib/image_generator.py" ~/.openclaw/workspace-designer/generate_images_dmxapi.py 2>/dev/null || true
chmod +x ~/.openclaw/workspace-designer/generate_images_dmxapi.py 2>/dev/null || true

# 安装草稿发布脚本
cp "$SCRIPT_DIR/../lib/draft_publisher.py" ~/.openclaw/workspace-mp-editor/tools/create_draft.py 2>/dev/null || true
chmod +x ~/.openclaw/workspace-mp-editor/tools/create_draft.py 2>/dev/null || true

echo "[4/4] 检查配置状态..."

# 检查微信配置
if grep -q "your_app_id_here" ~/.openclaw/workspace-mp-editor/.env 2>/dev/null; then
    echo "     ⚠️  微信公众号配置未完成，请编辑 ~/.openclaw/workspace-mp-editor/.env"
else
    echo "     ✅ 微信公众号配置已完成"
fi

# 检查配图API配置
if grep -q "your_api_key_here" ~/.openclaw/workspace-designer/.env 2>/dev/null; then
    echo "     ⚠️  配图API配置未完成，请编辑 ~/.openclaw/workspace-designer/.env"
else
    echo "     ✅ 配图API配置已完成"
fi

echo ""
echo "=== 初始化完成 ==="
echo ""
echo "下一步："
echo "1. 编辑 ~/.openclaw/workspace-mp-editor/.env 填写微信公众号配置"
echo "2. 编辑 ~/.openclaw/workspace-designer/.env 填写配图API配置"
echo "3. 在微信公众号后台添加本机IP到白名单"
echo ""
