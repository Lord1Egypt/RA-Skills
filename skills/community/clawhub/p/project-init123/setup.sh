#!/bin/bash
# =============================================
# project-init Skill 环境初始化脚本
# =============================================

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/project-init"
ENV_FILE="$CONFIG_DIR/.env"

echo "========================================"
echo "  project-init Skill 初始化配置"
echo "========================================"

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 安装 Python 依赖
echo ""
echo "[1/3] 安装 Python 依赖..."
pip3 install -r "$SKILL_DIR/requirements.txt" --break-system-packages -q
echo "✅ Python 依赖安装完成"

# 检查 Node.js
echo ""
echo "[2/3] 检查 Node.js 环境..."
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装 Node.js"
    exit 1
fi
echo "✅ Node.js $(node --version) 已就绪"

# 配置环境变量
echo ""
echo "[3/3] 配置环境变量..."

if [ -f "$ENV_FILE" ]; then
    echo "检测到已有配置文件：$ENV_FILE"
    read -p "是否重新配置？(y/N): " RECONFIG
    if [[ ! "$RECONFIG" =~ ^[Yy]$ ]]; then
        echo "跳过配置，使用现有配置。"
        echo ""
        echo "✅ 初始化完成！"
        exit 0
    fi
fi

echo ""
read -p "Gitea 服务器地址 (默认: http://43.156.243.152:3000): " GITEA_URL
GITEA_URL="${GITEA_URL:-http://43.156.243.152:3000}"

read -p "AIFusionBot Personal Access Token: " GITEA_TOKEN
if [ -z "$GITEA_TOKEN" ]; then
    echo "❌ Token 不能为空"
    exit 1
fi

read -p "Gitea 组织名 (默认: HKU-AIFusion): " GITEA_ORG
GITEA_ORG="${GITEA_ORG:-HKU-AIFusion}"

read -p "imap-smtp-email Skill 的绝对路径: " EMAIL_SKILL_PATH

read -p "发件邮箱账号名称（留空使用默认账号）: " EMAIL_ACCOUNT

# 写入配置文件
cat > "$ENV_FILE" << EOF
GITEA_URL=${GITEA_URL}
GITEA_TOKEN=${GITEA_TOKEN}
GITEA_ORG=${GITEA_ORG}
EMAIL_SKILL_PATH=${EMAIL_SKILL_PATH}
EMAIL_ACCOUNT=${EMAIL_ACCOUNT}
EOF

chmod 600 "$ENV_FILE"

echo ""
echo "✅ 配置已保存至 $ENV_FILE"
echo ""

# 测试 Gitea 连接
echo "测试 Gitea 连接..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token ${GITEA_TOKEN}" \
    "${GITEA_URL}/api/v1/user")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Gitea 连接成功"
else
    echo "⚠️  Gitea 连接返回 HTTP ${HTTP_CODE}，请检查 URL 和 Token"
fi

echo ""
echo "========================================"
echo "  初始化完成！"
echo "========================================"
