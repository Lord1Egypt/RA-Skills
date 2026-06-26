#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_NAME="openviking-context"
SOURCE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo -e "${BOLD}══════════════════════════════════════════════${NC}"
echo -e "${BOLD}  OpenViking Skill → OpenClaw 安装${NC}"
echo -e "${BOLD}══════════════════════════════════════════════${NC}"
echo ""

# ─── 检测 OpenClaw skills 目录 ───────────────────────────────────────

detect_skills_dir() {
    # 优先使用用户指定的环境变量
    if [ -n "${OPENCLAW_SKILLS_DIR:-}" ]; then
        echo "$OPENCLAW_SKILLS_DIR"
        return
    fi

    # 1) 本机安装：homebrew (Apple Silicon)
    local d="/opt/homebrew/lib/node_modules/openclaw/skills"
    [ -d "$d" ] && echo "$d" && return

    # 2) 本机安装：homebrew (Intel Mac) / Linux npm global
    d="/usr/local/lib/node_modules/openclaw/skills"
    [ -d "$d" ] && echo "$d" && return

    # 3) 本机安装：npm root -g
    local npm_root
    npm_root="$(npm root -g 2>/dev/null || true)"
    if [ -n "$npm_root" ] && [ -d "$npm_root/openclaw/skills" ]; then
        echo "$npm_root/openclaw/skills"
        return
    fi

    # 4) Docker：当前目录下的 skills/ (docker-compose 挂载)
    if [ -d "./skills" ] && [ -f "./docker-compose.yml" ] || [ -f "./docker-compose.yaml" ]; then
        echo "$(pwd)/skills"
        return
    fi

    # 5) Docker：常见 docker-compose 项目位置
    for p in "$HOME/openclaw/skills" "$HOME/.openclaw/skills" "$HOME/docker/openclaw/skills"; do
        [ -d "$p" ] && echo "$p" && return
    done

    # 未找到
    echo ""
}

TARGET_BASE=$(detect_skills_dir)

if [ -z "$TARGET_BASE" ]; then
    echo -e "${YELLOW}[!] 未自动检测到 OpenClaw skills 目录${NC}"
    echo ""
    echo "  请选择你的安装方式："
    echo ""
    echo "  1) 本机安装 (npm global) — 手动输入路径"
    echo "  2) Docker 安装 — 输入 docker-compose 项目中的 skills 目录"
    echo "  3) 自定义路径"
    echo ""
    echo -en "${CYAN}  请选择 [1-3]: ${NC}"
    read -r CHOICE

    case "$CHOICE" in
        1)
            echo -en "${CYAN}  npm global skills 路径: ${NC}"
            read -r TARGET_BASE
            ;;
        2)
            echo -en "${CYAN}  docker-compose 项目中的 skills 目录路径: ${NC}"
            read -r TARGET_BASE
            ;;
        3)
            echo -en "${CYAN}  自定义路径: ${NC}"
            read -r TARGET_BASE
            ;;
        *)
            echo -e "${RED}[✗] 无效选择${NC}"
            exit 1
            ;;
    esac

    if [ -z "$TARGET_BASE" ]; then
        echo -e "${RED}[✗] 未提供路径${NC}"
        exit 1
    fi
fi

TARGET_DIR="$TARGET_BASE/$SKILL_NAME"

echo -e "  检测到 skills 目录: ${BOLD}$TARGET_BASE${NC}"
echo -e "  安装到: ${BOLD}$TARGET_DIR${NC}"
echo ""

# ─── 安装 ────────────────────────────────────────────────────────────

if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}[!] 已存在: $TARGET_DIR${NC}"
    echo -en "    覆盖安装? [y/N]: "
    read -r OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo -e "${RED}[✗] 已取消${NC}"
        exit 0
    fi
    rm -rf "$TARGET_DIR"
fi

mkdir -p "$TARGET_DIR/scripts"

cp "$SOURCE_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
cp "$SOURCE_DIR/scripts/install.sh" "$TARGET_DIR/scripts/install.sh"
cp "$SOURCE_DIR/scripts/setup-config.sh" "$TARGET_DIR/scripts/setup-config.sh"
cp "$SOURCE_DIR/scripts/viking.py" "$TARGET_DIR/scripts/viking.py"
cp "$SOURCE_DIR/scripts/demo-token-compare.py" "$TARGET_DIR/scripts/demo-token-compare.py"

chmod +x "$TARGET_DIR/scripts/"*.sh 2>/dev/null || true

echo ""
echo -e "${GREEN}[✓] Skill 已安装到: $TARGET_DIR${NC}"
echo ""
echo -e "  目录结构:"
echo -e "  $TARGET_DIR/"
echo -e "  ├── SKILL.md"
echo -e "  └── scripts/"
echo -e "      ├── install.sh"
echo -e "      ├── setup-config.sh"
echo -e "      ├── viking.py"
echo -e "      └── demo-token-compare.py"
echo ""
echo -e "${BOLD}下一步：${NC}"
echo -e "  1. 在 OpenClaw 中说 ${BOLD}\"refresh skills\"${NC}"
echo -e "  2. 然后说 ${BOLD}\"帮我安装 openviking\"${NC}"
echo -e "  3. 或手动:  bash $TARGET_DIR/scripts/install.sh"
echo ""
echo -e "${YELLOW}提示：${NC}Docker 用户安装后需要重启容器让 OpenClaw 发现新 skill："
echo -e "  docker compose restart openclaw"
echo ""
echo -e "也可以通过环境变量跳过自动检测："
echo -e "  OPENCLAW_SKILLS_DIR=/your/path bash scripts/install-skill.sh"
echo ""
