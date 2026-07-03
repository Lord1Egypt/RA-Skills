#!/bin/bash
# =============================================================================
# install.sh — 一键安装 preflight 工作流技能包
# 安装内容:
#   - preflight.sh (自检脚本)
#   - SKILL.md (技能文档 - 复制到 ~/.local/share/agent-skills/ 或项目目录)
#   - LEARNINGS.md (学习记录模板)
# =============================================================================

set -e

# ── 确定安装路径 ────────────────────────────────────────
# 如果传了 --path 参数，安装到指定目录
# 否则默认装到当前用户的 HOME 下的 .preflight/

INSTALL_DIR="${HOME}/.preflight"
AGENT_SKILLS_DIR="${HOME}/.local/share/agent-skills"

# 解析参数
while [ "$#" -gt 0 ]; do
    case "$1" in
        --path)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --agent-skills)
            AGENT_SKILLS_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: ./install.sh [OPTIONS]"
            echo ""
            echo "选项:"
            echo "  --path DIR          安装到指定目录 (默认: ~/.preflight)"
            echo "  --agent-skills DIR  复制 SKILL.md 到指定 agent skills 目录"
            echo "  --help, -h          显示帮助"
            echo ""
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            echo "用法: ./install.sh [--path DIR] [--agent-skills DIR]"
            exit 1
            ;;
    esac
done

# ── 安装 ─────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════"
echo "  📦 安装 preflight 工作流技能包"
echo "═══════════════════════════════════════════════════════"

# 创建目录
mkdir -p "$INSTALL_DIR"
echo "  📁 安装目录: $INSTALL_DIR"

# 复制文件
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/preflight.sh" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/SKILL.md" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/LEARNINGS.md" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/preflight.sh"

echo "  ✅ preflight.sh → $INSTALL_DIR/preflight.sh"
echo "  ✅ SKILL.md    → $INSTALL_DIR/SKILL.md"
echo "  ✅ LEARNINGS.md → $INSTALL_DIR/LEARNINGS.md"

# 如果指定了 agent skills 目录，复制 SKILL.md
if [ -d "$AGENT_SKILLS_DIR" ]; then
    mkdir -p "$AGENT_SKILLS_DIR"
    cp "$SCRIPT_DIR/SKILL.md" "$AGENT_SKILLS_DIR/preflight-workflow.skill.md"
    echo "  ✅ 已复制到 agent skills 目录: $AGENT_SKILLS_DIR"
fi

# 添加到 PATH（通过 .bashrc/.zshrc）
SHELL_RC="${HOME}/.bashrc"
if [ -f "${HOME}/.zshrc" ]; then
    SHELL_RC="${HOME}/.zshrc"
fi

if ! grep -q "preflight" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# preflight 工作流技能包" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_RC"
    echo "  ✅ 已添加到 PATH（$SHELL_RC）"
    echo "     请运行: source $SHELL_RC"
else
    echo "  ℹ️  PATH 已包含 preflight，跳过"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✅ 安装完成！"
echo ""
echo "  用法:"
echo "    preflight.sh \"你的任务描述\""
echo ""
echo "  或者让 AI agent 加载 SKILL.md:"
echo "    /preflight-workflow 部署新功能"
echo "═══════════════════════════════════════════════════════"
