#!/bin/bash
# ============================================================
# Project Daily Recap - 安装配置脚本
# 自动检测环境、写入配置、设置 cron
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config"

echo "============================================"
echo "  📋 Project Daily Recap - 安装程序"
echo "  项目进度定时复盘提醒"
echo "============================================"
echo ""

# ---------- 1. 检测 Node.js ----------
echo "🔍 [1/4] 检测 Node.js 环境..."
NODE_CMD=""
if command -v node &>/dev/null; then
    NODE_VER=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
    echo "  发现 Node.js v$(node --version 2>/dev/null | sed 's/v//')"
    if [ "$NODE_VER" -ge 20 ] 2>/dev/null; then
        NODE_CMD=$(command -v node)
    fi
fi

# 尝试 nvm 中的 v22
if [ -z "$NODE_CMD" ] && [ -s "$HOME/.nvm/nvm.sh" ]; then
    . "$HOME/.nvm/nvm.sh" 2>/dev/null
    if nvm which 22 &>/dev/null; then
        NODE_CMD=$(nvm which 22)
        echo "  使用 nvm Node.js $(nvm which 22 | xargs $NODE_CMD --version 2>/dev/null)"
    fi
fi

if [ -z "$NODE_CMD" ]; then
    echo "  ⚠️ 未找到 Node.js v22+，将使用 PATH 中的 node"
    NODE_CMD=$(command -v node || echo "/usr/bin/node")
fi
echo "  ✅ Node.js 路径: $NODE_CMD"
echo ""

# ---------- 2. 检测 OpenClaw ----------
echo "🔍 [2/4] 检测 OpenClaw..."
OC_CMD=""
if command -v openclaw &>/dev/null; then
    OC_CMD=$(command -v openclaw)
elif [ -x "$HOME/.local/share/pnpm/openclaw" ]; then
    OC_CMD="$HOME/.local/share/pnpm/openclaw"
else
    echo "  ❌ 未找到 OpenClaw 命令！请先部署 OpenClaw。"
    exit 1
fi
echo "  ✅ OpenClaw 路径: $OC_CMD"

# 检测登录状态
OC_STATUS=$("$NODE_CMD" "$OC_CMD" status 2>&1 | head -5)
if echo "$OC_STATUS" | grep -qi "not.*logged\|login\|credential"; then
    echo "  ⚠️ OpenClaw 未登录或凭证过期，请运行 openclaw status 检查"
    echo "  ⚠️ 你可以继续安装，但需要自行配置微信目标"
    HAS_CREDS=false
else
    echo "  ✅ OpenClaw 状态正常"
    HAS_CREDS=true
fi
echo ""

# ---------- 3. 配置微信接收人 ----------
echo "🔧 [3/4] 配置微信接收人..."

# 检测当前会话信息
CURRENT_TARGET=""
CURRENT_ACCOUNT=""
CURRENT_CHANNEL="openclaw-weixin"

if [ "$HAS_CREDS" = true ]; then
    # 尝试从 .openclaw/config 读取当前微信配置
    CONFIG_DIR="$HOME/.openclaw"
    if [ -f "$CONFIG_DIR/config.yaml" ]; then
        echo "  发现 OpenClaw 配置文件，正在读取微信通道信息..."
        # 简单读取（正式用更智能的方式）
    fi
    
    # 询问用户
    read -r -p "  请输入微信接收人ID（直接回车用当前会话默认）: " input_target
    if [ -n "$input_target" ]; then
        CURRENT_TARGET="$input_target"
    fi
    
    read -r -p "  请输入 Account ID（直接回车用默认）: " input_account
    if [ -n "$input_account" ]; then
        CURRENT_ACCOUNT="$input_account"
    fi
fi

if [ -z "$CURRENT_TARGET" ]; then
    CURRENT_TARGET="o9cq80yTg9YA6Y1jSYCcUpInWNbI@im.wechat"
    echo "  ⚠️ 使用默认目标（安装后可修改 config 文件）"
fi
if [ -z "$CURRENT_ACCOUNT" ]; then
    CURRENT_ACCOUNT="51fdf6380286-im-bot"
fi

echo "  📱 目标: $CURRENT_TARGET"
echo "  📱 账号: $CURRENT_ACCOUNT"
echo "  📱 通道: $CURRENT_CHANNEL"

# 读取推送时间
read -r -p "  输入推送小时（0-23，默认20）: " input_hour
PUSH_HOUR=${input_hour:-20}
read -r -p "  输入推送分钟（0-59，默认0）: " input_min
PUSH_MINUTE=${input_min:-0}

# 写入配置
sed -i "s|^WEIXIN_TARGET=.*|WEIXIN_TARGET=\"${CURRENT_TARGET}\"|" "$CONFIG_FILE"
sed -i "s|^WEIXIN_ACCOUNT=.*|WEIXIN_ACCOUNT=\"${CURRENT_ACCOUNT}\"|" "$CONFIG_FILE"
sed -i "s|^PUSH_HOUR=.*|PUSH_HOUR=${PUSH_HOUR}|" "$CONFIG_FILE"
sed -i "s|^PUSH_MINUTE=.*|PUSH_MINUTE=${PUSH_MINUTE}|" "$CONFIG_FILE"
echo "  ✅ 配置已写入 $CONFIG_FILE"
echo ""

# ---------- 4. 设置 cron ----------
echo "⏰ [4/4] 设置定时任务..."

CRON_EXPR="${PUSH_MINUTE} ${PUSH_HOUR} * * *"
CRON_CMD="/bin/bash ${SCRIPT_DIR}/reminder.sh"
CRON_LINE="${CRON_EXPR} ${CRON_CMD}"

# 读取现有 crontab
CURRENT_CRON=$(crontab -l 2>/dev/null || true)

# 检查是否已有同一条目
if echo "$CURRENT_CRON" | grep -qF "$CRON_CMD"; then
    echo "  ⚠️ 该脚本已在 cron 中，跳过添加"
else
    # 检查是否有旧的项目提醒条目
    CLEANED_CRON=$(echo "$CURRENT_CRON" | grep -v "project-reminder\|reminder.sh" || true)
    # 追加新条目
    (echo "$CLEANED_CRON"; echo "$CRON_LINE") | crontab -
    echo "  ✅ cron 已添加: $CRON_EXPR"
fi

echo ""
echo "============================================"
echo "  ✅ 安装完成！"
echo "============================================"
echo ""
echo "  ⏰ 每晚 ${PUSH_HOUR}:${PUSH_MINUTE} 自动推送"
echo "  📱 快去检查微信是否收到消息"
echo ""
echo "  手动测试: bash ${SCRIPT_DIR}/reminder.sh"
echo "  修改配置: vi ${SCRIPT_DIR}/config"
echo "  查看日志: cat ${SCRIPT_DIR}/reminder.log"
echo "  编辑 cron: crontab -e"
echo ""

# 询问是否立即测试
read -r -p "  是否立即发送测试消息？(y/N): " test_now
if [ "$test_now" = "y" ] || [ "$test_now" = "Y" ]; then
    echo ""
    echo "📤 发送测试消息..."
    bash "${SCRIPT_DIR}/reminder.sh" || {
        echo "  ⚠️ 发送失败，请检查配置后重试"
    }
    echo ""
    echo "  查看日志: cat ${SCRIPT_DIR}/reminder.log"
fi

echo ""
echo "🎉 安装完毕，祝你项目顺利！"
