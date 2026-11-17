#!/usr/bin/env bash
# qq_to_mp3.sh — 批量将音频文件转换为 MP3
# Usage:
#   qq_to_mp3.sh <file_or_dir>           # 转换文件或目录（递归）
#   qq_to_mp3.sh <dir> -q 0              # 指定质量档位（0-6，默认 2）
#   qq_to_mp3.sh <dir> -o /output/dir    # 指定输出目录
#   qq_to_mp3.sh <dir> -q 0 -o /output   # 组合使用
set -euo pipefail

# ── 默认参数 ──
QUALITY=2
OUTPUT_DIR=""
INPUT_PATH=""

# ── 解析参数 ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    -q|--quality)
      QUALITY="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 <file_or_dir> [-q <0-6>] [-o <output_dir>]"
      echo ""
      echo "Options:"
      echo "  -q, --quality   VBR quality (0=best ~245kbps, 2=default ~190kbps, 6=small ~135kbps)"
      echo "  -o, --output    Output directory (default: same as source)"
      echo "  -h, --help      Show this help"
      exit 0
      ;;
    *)
      if [[ -z "$INPUT_PATH" ]]; then
        INPUT_PATH="$1"
      else
        echo "Error: unexpected argument '$1'" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$INPUT_PATH" ]]; then
  echo "Error: no input file or directory specified" >&2
  echo "Usage: $0 <file_or_dir> [-q <0-6>] [-o <output_dir>]" >&2
  exit 1
fi

if [[ ! -e "$INPUT_PATH" ]]; then
  echo "Error: '$INPUT_PATH' does not exist" >&2
  exit 1
fi

# ── 检查 ffmpeg ──
if ! command -v ffmpeg &>/dev/null; then
  echo "Error: ffmpeg not found in PATH" >&2
  echo "Install:" >&2
  echo "  macOS:   brew install ffmpeg" >&2
  echo "  Ubuntu:  sudo apt install ffmpeg" >&2
  echo "  Windows: download from https://ffmpeg.org/download.html" >&2
  exit 1
fi

# ── 支持的输入格式 ──
SUPPORTED_EXT="ogg flac m4a aac wav opus wma aiff aif"

# ── 计数器 ──
SUCCESS=0
FAILED=0
SKIPPED=0
TOTAL=0

# ── 转码函数 ──
convert_file() {
  local src="$1"
  local src_ext="${src##*.}"
  src_ext=$(echo "$src_ext" | tr '[:upper:]' '[:lower:]')

  # 检查是否为支持的格式
  local is_supported=false
  for ext in $SUPPORTED_EXT; do
    if [[ "$src_ext" == "$ext" ]]; then
      is_supported=true
      break
    fi
  done

  if [[ "$is_supported" == false ]]; then
    return 2  # 不支持的格式
  fi

  # 计算输出路径
  local src_dir src_base dest
  src_dir=$(dirname "$src")
  src_base=$(basename "$src" ".$src_ext")

  if [[ -n "$OUTPUT_DIR" ]]; then
    # 保持相对目录结构
    local rel_dir
    if [[ -d "$INPUT_PATH" ]]; then
      rel_dir=$(realpath --relative-to="$INPUT_PATH" "$src_dir" 2>/dev/null || echo "")
    else
      rel_dir=""
    fi
    dest="$OUTPUT_DIR/$rel_dir/$src_base.mp3"
    mkdir -p "$(dirname "$dest")"
  else
    dest="$src_dir/$src_base.mp3"
  fi

  # 跳过已存在的 MP3
  if [[ -f "$dest" ]]; then
    echo "  ⏭️  SKIP (already exists): $dest"
    return 1
  fi

  # 执行转码
  if ffmpeg -y -i "$src" -vn -acodec libmp3lame -q:a "$QUALITY" "$dest" 2>/dev/null; then
    local src_size dest_size
    src_size=$(du -h "$src" | cut -f1)
    dest_size=$(du -h "$dest" | cut -f1)
    echo "  ✅ OK: $src_base.$src_ext ($src_size) → $src_base.mp3 ($dest_size)"
    return 0
  else
    echo "  ❌ FAIL: $src"
    # 清理可能的残缺输出
    rm -f "$dest" 2>/dev/null
    return 3
  fi
}

# ── 主逻辑 ──
echo "════════════════════════════════════════════"
echo "  QQ音乐转 MP3 工具"
echo "  输入: $INPUT_PATH"
echo "  质量: VBR -q:a $QUALITY"
if [[ -n "$OUTPUT_DIR" ]]; then
  echo "  输出: $OUTPUT_DIR"
fi
echo "════════════════════════════════════════════"
echo ""

if [[ -f "$INPUT_PATH" ]]; then
  # 单文件模式
  TOTAL=1
  convert_file "$INPUT_PATH"
  case $? in
    0) SUCCESS=1 ;;
    1) SKIPPED=1 ;;
    2) echo "Error: unsupported format"; FAILED=1 ;;
    3) FAILED=1 ;;
  esac
elif [[ -d "$INPUT_PATH" ]]; then
  # 目录递归模式
  while IFS= read -r -d '' file; do
    TOTAL=$((TOTAL + 1))
    convert_file "$file"
    case $? in
      0) SUCCESS=$((SUCCESS + 1)) ;;
      1) SKIPPED=$((SKIPPED + 1)) ;;
      2) ;;  # 不支持的格式，不计入失败
      3) FAILED=$((FAILED + 1)) ;;
    esac
  done < <(find "$INPUT_PATH" -type f -print0)
  TOTAL=$((TOTAL - 1))  # 修正计数（初始为 0，循环中先 +1）
else
  echo "Error: '$INPUT_PATH' is neither a file nor a directory" >&2
  exit 1
fi

# ── 汇总报告 ──
echo ""
echo "════════════════════════════════════════════"
echo "  转换完成"
echo "  总计: $TOTAL  成功: $SUCCESS  跳过: $SKIPPED  失败: $FAILED"
echo "════════════════════════════════════════════"

if [[ "$FAILED" -gt 0 ]]; then
  exit 1
fi
exit 0
