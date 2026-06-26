#!/bin/bash
# =============================================================================
# obsidian-llm-wiki 初始化脚本（macOS / Linux）
# =============================================================================
# 用法:
#   ./init-wiki.sh /path/to/vault "我的知识库"
#
# 或不带参数运行，会交互式询问：
#   ./init-wiki.sh
# =============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 模板目录查找策略（优先级从高到低）
# 1. $SCRIPT_DIR/../templates/                   — skill 结构：$SKILL/scripts/init-wiki.sh
# 2. $SCRIPT_DIR/templates/                      — 脚本独立运行：./templates/
# 3. ~/.workbuddy/skills/<skill>/templates/     — ClawHub 标准安装路径
SKILL_NAME="obsidian-llm-wiki"

# 模板目录查找（兼容 WSL / 非标准 HOME 等情况）
# 优先检查可能的 skill 安装路径
declare -a TEMPLATE_PATHS=(
    "$SCRIPT_DIR/../templates"                  # skill 结构
    "$SCRIPT_DIR/templates"                     # 脚本同级 templates/
    "/root/.workbuddy/skills/$SKILL_NAME/templates"
    "$HOME/.workbuddy/skills/$SKILL_NAME/templates"
)

TEMPLATES_DIR=""
for p in "${TEMPLATE_PATHS[@]}"; do
    if [[ -d "$p" ]]; then
        TEMPLATES_DIR="$p"
        break
    fi
done

if [[ -z "$TEMPLATES_DIR" ]]; then
    echo -e "${RED}[ERROR] 找不到模板目录。确认 skill 已正确安装。${NC}"
    echo "[DEBUG] 已检查：${TEMPLATE_PATHS[*]}"
    exit 1
fi

# -----------------------------------------------------------------------------
# 帮助信息
# -----------------------------------------------------------------------------
show_help() {
    cat << EOF
用法：$(basename "$0") [VAULT_PATH] [TOPIC]

初始化一个新的 obsidian-llm-wiki 知识库 vault。

参数:
  VAULT_PATH    vault 根目录路径（可选，不提供则交互式询问）
  TOPIC        知识库主题名称（可选，默认 "我的知识库"）

示例:
  $(basename "$0") ~/Documents/MyWiki "AI 学习"
  $(basename "$0")                    # 交互式模式

EOF
}

# -----------------------------------------------------------------------------
# 主初始化函数
# -----------------------------------------------------------------------------
init_wiki() {
    local VAULT_PATH="$1"
    local TOPIC="$2"

    echo -e "${CYAN}=== 初始化 obsidian-llm-wiki 知识库 ===${NC}"
    echo -e "Vault: $VAULT_PATH"
    echo -e "主题：$TOPIC"
    echo ""

    # 检查模板目录
    if [[ ! -d "$TEMPLATES_DIR" ]]; then
        echo -e "${RED}[ERROR] 模板目录不存在：$TEMPLATES_DIR${NC}"
        exit 1
    fi

    # 创建目录结构
    local DIRS=(
        "raw/articles"
        "raw/tweets"
        "raw/wechat"
        "raw/xiaohongshu"
        "raw/zhihu"
        "raw/pdfs"
        "raw/notes/learning"
        "raw/notes/projects"
        "raw/notes/testing"
        "wiki/entities"
        "wiki/topics"
        "wiki/sources"
        "wiki/comparisons"
        "wiki/synthesis"
        "templates"
    )

    for dir in "${DIRS[@]}"; do
        local FULL_PATH="$VAULT_PATH/$dir"
        if [[ -d "$FULL_PATH" ]]; then
            echo -e "${YELLOW}[SKIP] $dir (已存在)${NC}"
        else
            mkdir -p "$FULL_PATH"
            echo -e "${GREEN}[CREATE] $dir${NC}"
        fi
    done

    # 复制模板文件
    echo ""
    echo -e "${CYAN}=== 复制模板文件 ===${NC}"
    for tpl in entity-template.md topic-template.md source-template.md; do
        local SRC="$TEMPLATES_DIR/$tpl"
        local DST="$VAULT_PATH/templates/$tpl"
        if [[ -f "$SRC" ]]; then
            cp "$SRC" "$DST"
            echo -e "${GREEN}[COPY ] templates/$tpl${NC}"
        fi
    done

    # 获取当前日期
    local DATE=$(date "+%Y-%m-%d")

    # 创建 README.md
    echo ""
    echo -e "${CYAN}=== 创建 README.md ===${NC}"
    cat > "$VAULT_PATH/README.md" << EOF
# $TOPIC

> 知识库主题：$TOPIC

## 关于

这是一个基于 [obsidian-llm-wiki](https://github.com/clawhub/obsidian-llm-wiki) 方法论构建的个人知识库。

## 目录结构

- \`raw/\` — 原始素材（不可变）
- \`wiki/\` — 编译后的知识（AI 维护）
- \`templates/\` — 页面模板

## 工作流

- **ingest**：消化素材 → 创建 wiki 页面
- **query**：查询知识库
- **lint**：健康检查
- **digest**：深度综合报告

## 快速开始

1. 把素材文件放入 \`raw/\` 对应目录
2. 告诉 AI "帮我消化这篇"
3. AI 自动整理知识到 \`wiki/\`

_Last updated: $DATE_
EOF
    echo -e "${GREEN}[CREATE] README.md${NC}"

    # 创建 index.md
    echo ""
    echo -e "${CYAN}=== 创建 index.md ===${NC}"
    cat > "$VAULT_PATH/index.md" << EOF
# 知识库索引

_Last updated: $DATE_

---

## 实体页

> 人物、组织、概念、工具等

| Page | Summary | Updated |
|------|---------|---------|

---

## 主题页

> 研究主题，知识领域

| Page | Summary | Updated |
|------|---------|---------|

---

## 素材摘要

> 每个消化过的素材都有一篇摘要

| Page | Summary | Updated |
|------|---------|---------|

---

## 对比分析

| Page | Summary | Updated |
|------|---------|---------|

---

## 综合分析

| Page | Summary | Updated |
|------|---------|---------|
EOF
    echo -e "${GREEN}[CREATE] index.md${NC}"

    # 创建 log.md
    echo ""
    echo -e "${CYAN}=== 创建 log.md ===${NC}"
    cat > "$VAULT_PATH/log.md" << EOF
# 操作日志

> 记录知识库的所有变更历史。只追加，不编辑历史条目。

---

## [$DATE] init | 初始化知识库

Source: init-wiki.sh
Pages affected: README.md (new), index.md (new), log.md (new), templates/ (created)
EOF
    echo -e "${GREEN}[CREATE] log.md${NC}"

    echo ""
    echo -e "${CYAN}=== 初始化完成 ===${NC}"
    echo -e "Vault 路径：$VAULT_PATH"
    echo ""
    echo -e "${YELLOW}下一步：${NC}"
    echo "  1. 用 Obsidian 打开这个文件夹"
    echo "  2. 告诉 AI '帮我消化这篇素材'"
    echo "  3. AI 自动整理知识到 wiki/"
}

# -----------------------------------------------------------------------------
# 入口
# -----------------------------------------------------------------------------
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

if [[ -n "$1" ]]; then
    # 命令行参数模式
    VAULT_PATH="$1"
    TOPIC="${2:-我的知识库}"
else
    # 交互式模式
    echo -n "请输入 vault 路径（如 ~/Documents/MyWiki）："
    read -r VAULT_PATH
    echo -n "请输入知识库主题（如 AI 学习，默认 '我的知识库'）："
    read -r TOPIC
    TOPIC="${TOPIC:-我的知识库}"
fi

# 安全地展开 ~ 为 $HOME（不使用 eval，避免 shell 注入）
if [[ "$VAULT_PATH" == "~"* ]]; then
    VAULT_PATH="${VAULT_PATH/#\~/$HOME}"
fi

# 转换为绝对路径（使用 realpath，不使用 eval）
if [[ -d "$VAULT_PATH" ]]; then
    VAULT_PATH="$(realpath "$VAULT_PATH")"
elif [[ "$VAULT_PATH" != /* ]]; then
    # 相对路径：拼接到当前目录
    VAULT_PATH="$(pwd)/$VAULT_PATH"
fi

# 安全验证：路径不能以 - 开头（防止选项注入）
if [[ "$VAULT_PATH" == -* ]]; then
    echo -e "${RED}[ERROR] Vault 路径不能以 '-' 开头${NC}"
    exit 1
fi

# 创建 vault 根目录（如果不存在）
if [[ ! -d "$VAULT_PATH" ]]; then
    echo -e "${YELLOW}[CREATE] vault 根目录：$VAULT_PATH${NC}"
    mkdir -p "$VAULT_PATH"
fi

init_wiki "$VAULT_PATH" "$TOPIC"
