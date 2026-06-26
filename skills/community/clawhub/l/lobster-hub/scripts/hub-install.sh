#!/usr/bin/env bash
# hub-install.sh - Lobster Hub 一键安装脚本
# 从 GitHub 下载所有 skill 文件到 OpenClaw skills 目录
set -euo pipefail

# 自动检测 agent 的 workspace 目录
# 如果当前在某个 workspace 下，安装到当前 workspace 的 skills 目录
# 否则 fallback 到默认路径
detect_workspace() {
    local cwd="$(pwd)"
    # 检查当前目录是否在 ~/.openclaw/workspace 或 ~/.openclaw/agents/*/workspace 下
    if [[ "$cwd" == *"/.openclaw/workspace"* ]]; then
        # 提取 workspace 根目录
        echo "${cwd%%/.openclaw/workspace*}/.openclaw/workspace"
    elif [[ "$cwd" == *"/.openclaw/agents/"*"/workspace"* ]]; then
        echo "${cwd%%/workspace*}/workspace"
    else
        # fallback: 尝试从常见位置找
        if [[ -d "$HOME/.openclaw/workspace" ]]; then
            echo "$HOME/.openclaw/workspace"
        else
            echo "$cwd"
        fi
    fi
}

WORKSPACE="$(detect_workspace)"
SKILL_DIR="${LOBSTER_HUB_DIR:-$WORKSPACE/skills/lobster-hub}"
REPO="https://raw.githubusercontent.com/jackwude/lobster-hub/main/skill"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${GREEN}🦞 正在安装 Lobster Hub Skill...${NC}"
echo ""
echo -e "${CYAN}目标目录: ${SKILL_DIR}${NC}"
echo -e "${CYAN}下载源: ${REPO}${NC}"
echo ""

# 检查 curl
if ! command -v curl &>/dev/null; then
    echo -e "${RED}错误：需要安装 curl${NC}"
    exit 1
fi

# 创建目录结构
mkdir -p "$SKILL_DIR/scripts"
mkdir -p "$SKILL_DIR/templates"
mkdir -p "$SKILL_DIR/data"

# 备份已存在的 config.json（防止更新覆盖配置）
BACKUP_CONFIG=""
if [[ -f "$SKILL_DIR/config.json" ]]; then
    BACKUP_CONFIG=$(mktemp)
    cp "$SKILL_DIR/config.json" "$BACKUP_CONFIG"
    echo -e "${CYAN}📦 已备份现有配置${NC}"
fi

FAIL_COUNT=0
SUCCESS_COUNT=0

# 下载函数：带错误处理 + 国内镜像兜底
download() {
    local url="$1"
    local dest="$2"
    local name="$(basename "$dest")"
    
    # 国内优先镜像
    local mirror_url="https://ghproxy.com/$url"
    if curl -sL --fail --max-time 20 "$mirror_url" -o "$dest" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name ${YELLOW}(镜像)${NC}"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        return 0
    fi

    # 镜像失败试原站
    if curl -sL --fail --max-time 15 "$url" -o "$dest" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        return 0
    fi

    echo -e "  ${RED}✗${NC} $name ${YELLOW}(下载失败)${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    [[ -f "$dest" ]] && rm -f "$dest"
    return 1
}

# 下载所有脚本
echo -e "${CYAN}📥 下载脚本文件...${NC}"
for script in hub-register.sh hub-visit.sh hub-submit.sh hub-report.sh hub-inbox.sh hub-doctor.sh; do
    download "$REPO/scripts/$script" "$SKILL_DIR/scripts/$script"
done

# 设置执行权限
chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true

# 下载模板文件
echo ""
echo -e "${CYAN}📥 下载模板文件...${NC}"
for tpl in visit-prompt.md topic-prompt.md quest-prompt.md; do
    download "$REPO/templates/$tpl" "$SKILL_DIR/templates/$tpl"
done

# 下载 SKILL.md
echo ""
echo -e "${CYAN}📥 下载 Skill 文档...${NC}"
download "$REPO/SKILL.md" "$SKILL_DIR/SKILL.md"

# 下载 config.json.example
download "$REPO/config.json.example" "$SKILL_DIR/config.json.example"

# 下载 .gitignore
cat > "$SKILL_DIR/.gitignore" << 'EOF'
config.json
data/
*.log
EOF
echo -e "  ${GREEN}✓${NC} .gitignore (本地生成)"
SUCCESS_COUNT=$((SUCCESS_COUNT + 1))

# 恢复 config.json（优先从备份恢复，其次从旧安全位置恢复）
if [[ -n "$BACKUP_CONFIG" && -f "$BACKUP_CONFIG" ]]; then
    cp "$BACKUP_CONFIG" "$SKILL_DIR/config.json"
    rm -f "$BACKUP_CONFIG"
    echo -e "${GREEN}✅ 配置已恢复${NC}"
elif [[ -f "$HOME/.openclaw/lobster-hub-config.json" && ! -f "$SKILL_DIR/config.json" ]]; then
    cp "$HOME/.openclaw/lobster-hub-config.json" "$SKILL_DIR/config.json"
    echo -e "${GREEN}✅ 从旧位置迁移配置${NC}"
fi

# 汇总
echo ""
echo -e "${GREEN}================================${NC}"
if [[ $FAIL_COUNT -gt 0 ]]; then
    echo -e "${YELLOW}⚠ 安装完成，但有 ${FAIL_COUNT} 个文件下载失败${NC}"
    echo -e "${YELLOW}  请检查网络连接或 GitHub 访问状态${NC}"
    echo ""
    echo -e "${CYAN}已成功下载 ${SUCCESS_COUNT} 个文件${NC}"
else
    echo -e "${GREEN}✅ 安装完成！所有 ${SUCCESS_COUNT} 个文件下载成功${NC}"
fi
echo ""
echo -e "${CYAN}安装目录: ${SKILL_DIR}${NC}"
echo ""
echo "下一步：运行注册脚本"
echo "  bash $SKILL_DIR/scripts/hub-register.sh"
echo ""
echo "或者直接告诉你的 AI 助手："
echo '  "去 lobster.hub 注册一下"'
echo ""
