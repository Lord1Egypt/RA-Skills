#!/bin/bash
# novel-creator 3.0 初始化脚本
# 支持 minimal / full 两种模式，并在 --clean 时先备份旧工作区。

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
INIT_TEMPLATE_DIR="$SKILL_DIR/assets/init"
TARGET_DIR="."

usage() {
  cat << EOF
用法: $(basename "$0") <小说名称> [选项]

选项:
  --mode minimal|full   初始化模式，默认 full
  --clean               清理旧工作区（会先备份）
  --target-dir PATH     指定工作区目录，默认当前目录
  -h, --help            显示帮助
EOF
}

write_markdown_file() {
  local path="$1"
  local content="$2"
  printf "%s\n" "$content" > "$path"
}

get_template_content() {
  local template_name="$1"
  local template_path="$INIT_TEMPLATE_DIR/$template_name"
  local content

  content="$(cat "$template_path")"
  content="${content//\{\{NOVEL_NAME\}\}/$NOVEL_NAME}"
  content="${content//\{\{MODE\}\}/$MODE}"
  content="${content//\{\{CREATED_AT\}\}/$CREATED_AT}"

  printf '%s' "$content"
}

backup_workspace() {
  local timestamp
  timestamp="$(date +%Y%m%d-%H%M%S)"
  local target="$BACKUP_DIR/$timestamp"
  mkdir -p "$target"

  [ -e "$OUTPUT_DIR" ] && cp -R "$OUTPUT_DIR" "$target/"
  [ -e "$MEMORY_DIR" ] && cp -R "$MEMORY_DIR" "$target/"
  [ -e "$PLAN_DIR" ] && cp -R "$PLAN_DIR" "$target/"
  [ -e "$MANIFEST_PATH" ] && cp "$MANIFEST_PATH" "$target/"

  echo -e "${YELLOW}[备份]${NC} 已备份旧工作区到 $target"
}

NOVEL_NAME=""
MODE="full"
CLEAN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --clean)
      CLEAN=true
      shift
      ;;
    --target-dir)
      TARGET_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo -e "${RED}[错误]${NC} 未知选项: $1"
      usage
      exit 1
      ;;
    *)
      if [ -z "$NOVEL_NAME" ]; then
        NOVEL_NAME="$1"
      else
        echo -e "${RED}[错误]${NC} 意外参数: $1"
        usage
        exit 1
      fi
      shift
      ;;
  esac
done

mkdir -p "$TARGET_DIR"
WORKSPACE_DIR="$(cd "$TARGET_DIR" && pwd)"
OUTPUT_DIR="$WORKSPACE_DIR/output"
MEMORY_DIR="$WORKSPACE_DIR/memory"
PLAN_DIR="$WORKSPACE_DIR/plan"
BACKUP_DIR="$WORKSPACE_DIR/backup"
MANIFEST_PATH="$WORKSPACE_DIR/manifest.json"
CREATED_AT="$(date +%Y-%m-%dT%H:%M:%S)"

if [ -z "$NOVEL_NAME" ]; then
  echo -e "${RED}[错误]${NC} 请提供小说名称"
  usage
  exit 1
fi

if [[ "$MODE" != "minimal" && "$MODE" != "full" ]]; then
  echo -e "${RED}[错误]${NC} --mode 仅支持 minimal 或 full"
  exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  novel-creator 3.0 - 初始化工作区${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "  小说名称: ${GREEN}《${NOVEL_NAME}》${NC}"
echo -e "  初始化模式: ${GREEN}${MODE}${NC}"
echo -e "  工作目录: ${GREEN}${WORKSPACE_DIR}${NC}"

mkdir -p "$BACKUP_DIR"

if [ "$CLEAN" = true ]; then
  if [ -e "$OUTPUT_DIR" ] || [ -e "$MEMORY_DIR" ] || [ -e "$PLAN_DIR" ] || [ -e "$MANIFEST_PATH" ]; then
    echo -e "${CYAN}[步骤]${NC} 备份旧工作区..."
    backup_workspace
  fi
  echo -e "${CYAN}[步骤]${NC} 清理旧工作区..."
  rm -rf "$OUTPUT_DIR" "$MEMORY_DIR" "$PLAN_DIR"
  rm -f "$MANIFEST_PATH"
fi

echo -e "${CYAN}[步骤]${NC} 创建目录..."
mkdir -p "$OUTPUT_DIR" "$MEMORY_DIR" "$PLAN_DIR"

echo -e "${CYAN}[步骤]${NC} 初始化 plan ..."
write_markdown_file "$PLAN_DIR/outline.md" "$(get_template_content "outline.md")"
write_markdown_file "$PLAN_DIR/current_unit.md" "$(get_template_content "current_unit.md")"
write_markdown_file "$PLAN_DIR/style_guide.md" "$(get_template_content "style_guide.md")"

if [ "$MODE" = "full" ]; then
  write_markdown_file "$PLAN_DIR/current_arc.md" "$(get_template_content "current_arc.md")"
fi

echo -e "${CYAN}[步骤]${NC} 初始化 memory ..."
write_markdown_file "$MEMORY_DIR/roles.md" "$(get_template_content "roles.md")"
write_markdown_file "$MEMORY_DIR/plot_points.md" "$(get_template_content "plot_points.md")"
write_markdown_file "$MEMORY_DIR/story_bible.md" "$(get_template_content "story_bible.md")"

if [ "$MODE" = "full" ]; then
  write_markdown_file "$MEMORY_DIR/locations.md" "$(get_template_content "locations.md")"
  write_markdown_file "$MEMORY_DIR/errors.md" "$(get_template_content "errors.md")"
  write_markdown_file "$MEMORY_DIR/foreshadowing.md" "$(get_template_content "foreshadowing.md")"
  write_markdown_file "$MEMORY_DIR/items.md" "$(get_template_content "items.md")"
fi

touch "$OUTPUT_DIR/.gitkeep"
write_markdown_file "$MANIFEST_PATH" "$(get_template_content "manifest.json")"

echo -e "\n${GREEN}[信息]${NC} 《${NOVEL_NAME}》工作区初始化完成！"
echo "后续步骤:"
echo "  1. 先做文风预热，填写 plan/style_guide.md"
echo "  2. 再开始样章或正文创作"
