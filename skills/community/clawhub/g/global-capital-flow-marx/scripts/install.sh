#!/usr/bin/env sh
# 安装 global-capital-flow-marx 到各 Agent Skills 客户端
# 用法: ./install.sh [目标]

set -eu

SKILL_NAME="global-capital-flow-marx"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(dirname "$SCRIPT_DIR")
SKILLS_ROOT=$(dirname "$SKILL_DIR")
REPO_ROOT=$(dirname "$SKILLS_ROOT")

usage() {
  cat <<'EOF'
用法: install.sh [目标]

目标:
  copilot    ~/.copilot/skills/<name>      GitHub Copilot CLI
  agents     ~/.agents/skills/<name>       VS Code / Codex / 通用 Agent Skills
  codex      ~/.agents/skills/<name>       OpenAI Codex CLI（文档指定的用户级位置）
  claude     ~/.claude/skills/<name>       Claude Code
  hermes     ~/.hermes/skills/<name>       Hermes Agent
  dsh        ~/.dsh/skills/<name>          DeepSeek Harness
  workbuddy  WorkBuddy 插件市场目录        检测不到时自动改为打包 ZIP
  pack       生成 dist/<name>.zip          供 WorkBuddy 等图形界面上传
  <路径>      <路径>/<name>                自定义 skills 根目录

示例:
  ./install.sh agents
  ./install.sh hermes
  ./install.sh dsh
  ./install.sh ~/my-skills
  ./install.sh pack
EOF
}

pack() {
  if ! command -v zip >/dev/null 2>&1; then
    echo "错误: 需要 zip 命令（Windows 可在 Git Bash 中运行，或手动压缩该文件夹）" >&2
    exit 1
  fi
  out_dir="$REPO_ROOT/dist"
  archive="$out_dir/$SKILL_NAME.zip"
  mkdir -p "$out_dir"
  rm -f "$archive"
  ( cd "$SKILLS_ROOT" && zip -qr "$archive" "$SKILL_NAME" -x '*/.DS_Store' )
  echo "已打包: $archive"
  echo "WorkBuddy: 「添加技能」→「上传技能」→ 选择该 ZIP。"
}

install_to() {
  dest="$1/$SKILL_NAME"
  mkdir -p "$1"
  rm -rf "$dest"
  cp -R "$SKILL_DIR" "$dest"
  echo "已安装到: $dest"
  echo "包含文件:"
  find "$dest" -type f | sed "s|$dest/|  |"
}

target="${1:-copilot}"
workbuddy_market="$HOME/.workbuddy/plugins/marketplaces/codebuddy-plugins-official/plugins"

case "$target" in
  -h|--help|help)
    usage
    exit 0
    ;;
  pack)
    pack
    exit 0
    ;;
  copilot)   root="$HOME/.copilot/skills" ;;
  agents)    root="$HOME/.agents/skills" ;;
  codex)     root="$HOME/.agents/skills" ;;
  claude)    root="$HOME/.claude/skills" ;;
  hermes)    root="$HOME/.hermes/skills" ;;
  dsh)       root="$HOME/.dsh/skills" ;;
  workbuddy)
    if [ -d "$workbuddy_market" ]; then
      root="$workbuddy_market"
    else
      echo "未检测到 WorkBuddy 插件市场目录:"
      echo "  $workbuddy_market"
      echo "改用图形界面安装："
      echo
      pack
      exit 0
    fi
    ;;
  *)         root="$target" ;;
esac

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "错误: 未找到 $SKILL_DIR/SKILL.md" >&2
  exit 1
fi

install_to "$root"

case "$target" in
  hermes)
    echo
    echo "下一步: hermes skills list   # 确认已收录；会话内用 /$SKILL_NAME 调用"
    ;;
  dsh)
    echo
    echo "下一步: 重启 dsh profile（如 npx @deepseek-ai/dsh web），再在会话中询问可用技能"
    ;;
  codex)
    echo
    echo "下一步: 在 Codex 中输入 \$ 查看候选，或 /skills；仓库内安装可改用 .agents/skills 相对路径"
    ;;
  workbuddy)
    echo
    echo "最后一步: 在 ~/.workbuddy/settings.json 的 enabledPlugins 中加入"
    echo "  \"$SKILL_NAME@codebuddy-plugins-official\": true"
    echo "然后重启 WorkBuddy。"
    ;;
esac

echo
echo "提示: 同一份 skill 可同时装到多个客户端；对照表见 README 的「客户端兼容性速查」。"
