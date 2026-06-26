#!/bin/bash
# ============================================================
# 南昌嘉宝莉（Nanchang Carpoly）Skill · Linux/macOS 安装
# ============================================================
# 用法：
#   curl -sSL https://raw.githubusercontent.com/Liubuq-sys/nanchang-jbl-skill/main/install.sh | bash
# ============================================================

REPO="https://github.com/Liubuq-sys/nanchang-jbl-skill.git"
SKILL_NAME="nanchang-jbl"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.openclaw/workspace/skills}"
SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

echo "=== 南昌嘉宝莉 Skill · 安装 ==="

mkdir -p "$SKILLS_DIR"

if [ -d "$SKILL_PATH/.git" ]; then
    echo "已安装，正在更新..."
    cd "$SKILL_PATH" && git pull --ff-only origin main 2>/dev/null || git pull --ff-only origin master 2>/dev/null
    echo "更新完成！"
else
    echo "正在下载 skill..."
    TMP_DIR=$(mktemp -d)
    git clone --depth 1 "$REPO" "$TMP_DIR" 2>/dev/null

    if [ -d "$SKILL_PATH" ]; then
        rm -rf "$SKILL_PATH"
    fi

    if [ -d "$TMP_DIR/$SKILL_NAME" ]; then
        cp -r "$TMP_DIR/$SKILL_NAME" "$SKILL_PATH"
    else
        cp -r "$TMP_DIR" "$SKILL_PATH"
    fi
    rm -rf "$TMP_DIR"
    echo "安装完成！"
fi

# 配置 crontab 自动更新（每天 3:07）
CRON_JOB="7 3 * * * cd $SKILL_PATH && git pull --ff-only origin main 2>/dev/null || git pull --ff-only origin master 2>/dev/null"
(crontab -l 2>/dev/null | grep -v "$SKILL_NAME"; echo "$CRON_JOB") | crontab - 2>/dev/null && echo "自动更新已配置（每天 3:07）" || echo "提示：无法配置 crontab，可手动更新"

echo ""
echo "Skill 路径: $SKILL_PATH"
echo "现在对 AI 说「南昌嘉宝莉」即可触发！"
