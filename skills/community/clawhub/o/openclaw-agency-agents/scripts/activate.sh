#!/bin/bash
# activate.sh - 激活指定的智能体

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REPO_DIR="$SKILL_DIR/repo"
WORKSPACE_DIR="$SKILL_DIR/../.."
BACKUP_DIR="$SKILL_DIR/backups"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

info() { echo -e "${GREEN}[OK]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!!]${RESET} $*"; }
error() { echo -e "${RED}[ERR]${RESET} $*" >&2; }

# 检查仓库是否存在
if [ ! -d "$REPO_DIR" ]; then
    error "仓库未找到！请先运行：cd $SKILL_DIR && git clone https://github.com/jnMetaCode/agency-agents-zh.git repo"
    exit 1
fi

# 检查参数
if [ $# -eq 0 ]; then
    error "用法: $0 <智能体名称>"
    echo ""
    echo "示例："
    echo "  $0 小红书运营"
    echo "  $0 前端开发者"
    echo "  $0 AI 工程师"
    exit 1
fi

AGENT_QUERY="$1"

# 查找智能体文件
echo -e "${CYAN}正在搜索智能体: $AGENT_QUERY${RESET}"

# 搜索所有智能体目录
AGENT_DIRS="academic design engineering finance game-development hr legal marketing paid-media sales product project-management supply-chain testing support spatial-computing specialized"

FOUND_DIR=""
FOUND_FILE=""
FOUND_NAME=""

for dir in $AGENT_DIRS; do
    if [ -d "$REPO_DIR/$dir" ]; then
        # 遍历该目录所有 md 文件
        while IFS= read -r file; do
            # 提取 name 字段（排除 description）
            file_name=$(grep "^name:" "$file" | head -1 | sed 's/name: //' | xargs)

            # 比较 name 字段（不区分大小写，支持部分匹配）
            if [[ "${file_name,,}" == *"${AGENT_QUERY,,}"* ]] || [[ "${file_name,,}" == "${AGENT_QUERY,,}" ]]; then
                FOUND_DIR="$dir"
                FOUND_FILE="$file"
                FOUND_NAME="$file_name"
                break 2  # 退出两层循环
            fi
        done < <(find "$REPO_DIR/$dir" -maxdepth 1 -name "*.md" 2>/dev/null)
    fi
done

if [ -z "$FOUND_FILE" ]; then
    error "未找到智能体: $AGENT_QUERY"
    echo ""
    echo "提示：使用 '列出所有智能体' 查看可用智能体"
    echo "提示：使用 '搜索智能体 <关键词>' 搜索智能体"
    exit 1
fi

info "找到智能体: $FOUND_NAME"

# 创建备份目录
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_SUBDIR="$BACKUP_DIR/$TIMESTAMP"

# 备份当前配置
info "备份当前配置到 $BACKUP_SUBDIR"
mkdir -p "$BACKUP_SUBDIR"

for file in SOUL.md IDENTITY.md AGENTS.md; do
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        cp "$WORKSPACE_DIR/$file" "$BACKUP_SUBDIR/"
        info "已备份 $file"
    fi
done

# 提取 YAML frontmatter 中的 description
AGENT_DESCRIPTION=$(grep "^description:" "$FOUND_FILE" | sed 's/description: //' | xargs)

# 生成 SOUL.md
cat > "$WORKSPACE_DIR/SOUL.md" << EOF
# SOUL.md - ${FOUND_NAME}

_当前激活的智能体：${FOUND_NAME}_

## 激活信息

- **智能体名称**：${FOUND_NAME}
- **激活时间**：$(date '+%Y-%m-%d %H:%M:%S')
- **配置来源**：openmaic-agents skill
- **原始文件**：${FOUND_FILE#$REPO_DIR/}

## 智能体描述

${AGENT_DESCRIPTION}

---

_这是从 agency-agents-zh 仓库激活的智能体配置。要恢复默认配置，请运行"恢复默认"命令。_
EOF
info "已生成 SOUL.md"

# 生成 IDENTITY.md
cat > "$WORKSPACE_DIR/IDENTITY.md" << EOF
# IDENTITY.md - ${FOUND_NAME}

- **Name**：${FOUND_NAME}
- **Creature**：AI Agent
- **Source**：agency-agents-zh
- **Category**：${FOUND_DIR}
EOF
info "已生成 IDENTITY.md"

# 生成 AGENTS.md（直接复制原始文件内容，但去除 YAML frontmatter）
# 提取 frontmatter 之后的正文内容
awk '
BEGIN { skip=1 }
/^---$/ { skip++; next }
skip==2 { next }
skip==3 { print }
' "$FOUND_FILE" > "$WORKSPACE_DIR/AGENTS.md"
info "已生成 AGENTS.md"

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}✓ 智能体已激活${RESET}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "${CYAN}智能体名称：${RESET}${FOUND_NAME}"
echo -e "${CYAN}所属分类：${RESET}${FOUND_DIR}"
echo -e "${CYAN}备份位置：${RESET}${BACKUP_SUBDIR}"
echo ""
echo -e "${YELLOW}恢复命令：恢复默认${RESET}"
