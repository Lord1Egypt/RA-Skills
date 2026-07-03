#!/bin/bash
# =============================================================================
# 鸿蒙代码工坊 — 单源→多工具构建脚本
# 将 SKILL.md 自动分发到 Cursor / Claude Code / Trae / Copilot 等 AI 工具
# =============================================================================
# 用法: bash scripts/build-dist.sh
# 输出: dist/ 目录，包含各工具的配置文件
# =============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$SKILL_DIR/SKILL.md"
DIST="$SKILL_DIR/dist"
DIST_CLAUDE="$DIST/claude"
DIST_CURSOR="$DIST/cursor"
DIST_TRAE="$DIST/trae"
DIST_COPILOT="$DIST/copilot"
DIST_WINDSURF="$DIST/windsurf"
DIST_CONTINUE="$DIST/continue"
DIST_GEMINI="$DIST/gemini"
DIST_CHATGPT="$DIST/chatgpt"

echo "🔨 鸿蒙代码工坊 — 多工具构建脚本"
echo "==================================="
echo "源文件: $SOURCE"
echo "输出目录: $DIST"
echo ""

# 检查源文件存在
if [ ! -f "$SOURCE" ]; then
    echo "❌ 错误: 找不到 SKILL.md"
    exit 1
fi

# 清理并重建 dist
rm -rf "$DIST"
mkdir -p "$DIST"

# ===== 1. Claude Code =====
echo "[1/8] 📦 Claude Code..."
mkdir -p "$DIST_CLAUDE"
# Claude Code 原生支持 SKILL.md 格式，直接复制
cp "$SOURCE" "$DIST_CLAUDE/SKILL.md"
echo "  → $DIST_CLAUDE/SKILL.md"

# ===== 2. Cursor =====
echo "[2/8] 🔵 Cursor (.cursor/rules/*.mdc)..."
mkdir -p "$DIST_CURSOR/.cursor/rules"
# Cursor 使用 mdc 格式，需要 YAML frontmatter 描述 + glob 匹配
# 从源文件中提取 description 和 triggers
DESC="HarmonyOS (鸿蒙) 全流程编码助手 — ArkTS/ArkUI/API 26/AGC上架"
# 生成 Cursor 格式的 .mdc 文件
{
  echo "---"
  echo "description: HarmonyOS (鸿蒙) 全流程编码助手 — ArkTS/ArkUI/API 26/AGC上架"
  echo "globs: \"**/*.ets, **/*.ts, **/*.json5, **/module.json5, **/build-profile.json5\""
  echo "---"
  echo ""
  cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d'
} > "$DIST_CURSOR/.cursor/rules/harmonyos-code-workshop.mdc"
echo "  → $DIST_CURSOR/.cursor/rules/harmonyos-code-workshop.mdc"

# ===== 3. Trae (字节跳动 AI IDE) =====
echo "[3/8] 🟡 Trae..."
mkdir -p "$DIST_TRAE/.trae/rules"
# Trae 基于 VS Code，支持类似 Cursor 的 rules 机制
{
  echo "---"
  echo "description: HarmonyOS (鸿蒙) 全流程编码助手，覆盖 ArkTS/ArkUI/API 26/AGC上架"
  echo "globs: \"**/*.ets, **/*.ts, **/*.json5\""
  echo "---"
  echo ""
  cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d'
} > "$DIST_TRAE/.trae/rules/harmonyos-code-workshop.mdc"
echo "  → $DIST_TRAE/.trae/rules/harmonyos-code-workshop.mdc"

# ===== 4. GitHub Copilot =====
echo "[4/8] 🟣 GitHub Copilot..."
mkdir -p "$DIST_COPILOT/.github"
# Copilot 使用 copilot-instructions.md，纯 Markdown 无 frontmatter
cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d' > "$DIST_COPILOT/.github/copilot-instructions.md"
echo "  → $DIST_COPILOT/.github/copilot-instructions.md"

# ===== 5. Windsurf / Codeium =====
echo "[5/8] 🟠 Windsurf..."
mkdir -p "$DIST_WINDSURF"
cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d' > "$DIST_WINDSURF/.windsurfrules"
echo "  → $DIST_WINDSURF/.windsurfrules"

# ===== 6. Continue.dev =====
echo "[6/8] 🟢 Continue.dev..."
mkdir -p "$DIST_CONTINUE/.continue/rules"
cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d' > "$DIST_CONTINUE/.continue/rules/harmonyos.md"
echo "  → $DIST_CONTINUE/.continue/rules/harmonyos.md"

# ===== 7. Gemini CLI =====
echo "[7/8] 🔶 Gemini CLI..."
mkdir -p "$DIST_GEMINI"
cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d' > "$DIST_GEMINI/GEMINI.md"
echo "  → $DIST_GEMINI/GEMINI.md"

# ===== 8. ChatGPT / 通用 LLM 系统提示 =====
echo "[8/8] 🤖 ChatGPT / 通用系统提示..."
mkdir -p "$DIST_CHATGPT"
{
  echo "# 鸿蒙代码工坊 — AI 系统提示"
  echo ""
  echo "你是鸿蒙（HarmonyOS）全流程编码助手，精通 ArkTS 语法、ArkUI 组件、API 26 新能力和 AGC 上架流程。"
  echo "当用户提出鸿蒙开发问题时，按以下知识体系回答："
  echo ""
  cat "$SOURCE" | sed '1,/^---$/d' | sed '1,/^---$/d'
} > "$DIST_CHATGPT/system-prompt.txt"
echo "  → $DIST_CHATGPT/system-prompt.txt"

# ===== 摘要 =====
echo ""
echo "==================================="
echo "✅ 构建完成！共生成 8 个工具配置"
echo "==================================="
echo ""
echo "📋 各工具安装方式："
echo ""
echo "┌──────────────┬────────────────────────────────────────────┐"
echo "│ Claude Code  │ cp dist/claude/SKILL.md ~/.claude/skills/  │"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ Cursor       │ 将 dist/cursor/.cursor 复制到项目根目录   │"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ Trae         │ 将 dist/trae/.trae 复制到项目根目录       │"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ Copilot      │ 将 dist/copilot/.github 复制到项目根目录  │"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ Windsurf     │ 将 dist/windsurf/.windsurfrules 复制到项目 │"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ Continue.dev │ 将 dist/continue/.continue 复制到项目根目录│"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ Gemini CLI   │ cp dist/gemini/GEMINI.md ./ (项目根目录)   │"
echo "├──────────────┼────────────────────────────────────────────┤"
echo "│ ChatGPT      │ 将 dist/chatgpt/system-prompt.txt 粘贴作为 │"
echo "│              │ ChatGPT 的自定义指令或系统提示              │"
echo "└──────────────┴────────────────────────────────────────────┘"
echo ""
echo "💡 小贴士: 运行 bash scripts/install.sh 可一键安装到当前项目"
