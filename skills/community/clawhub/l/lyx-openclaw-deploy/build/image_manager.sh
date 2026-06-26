#!/bin/bash
# OpenClaw 镜像管理脚本
# 用于查看镜像信息、验证完整性、版本管理

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
# shellcheck source=/dev/null
source "$PROJECT_DIR/build/common.sh"

IMAGE_FILE=""
COMMAND="info"

usage() {
  cat <<EOF
用法: $0 <命令> [选项]

命令:
  info <镜像文件>       查看镜像信息
  verify <镜像文件>     验证镜像完整性 (SHA256)
  list <目录>          列出目录中的所有镜像
  extract <镜像文件> <目标目录> 解压镜像

示例:
  $0 info ./openclaw-latest.tar.gz
  $0 verify ./openclaw-latest.tar.gz
  $0 list ~/.openclaw/images/
  $0 extract ./openclaw-latest.tar.gz /tmp/openclaw
EOF
}

# 解析参数
if [ $# -lt 1 ]; then
  usage
  exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
  info)
    if [ $# -lt 1 ]; then
      log_error "请指定镜像文件"
      exit 1
    fi
    IMAGE_FILE="$1"
    ;;
  verify)
    if [ $# -lt 1 ]; then
      log_error "请指定镜像文件"
      exit 1
    fi
    IMAGE_FILE="$1"
    ;;
  list)
    if [ $# -lt 1 ]; then
      log_error "请指定目录"
      exit 1
    fi
    ;;
  extract)
    if [ $# -lt 2 ]; then
      log_error "请指定镜像文件和目标目录"
      exit 1
    fi
    IMAGE_FILE="$1"
    EXTRACT_DIR="$2"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    log_error "未知命令: $COMMAND"
    usage
    exit 1
    ;;
esac

# 命令: info
cmd_info() {
  local img="$IMAGE_FILE"

  if [ ! -f "$img" ]; then
    log_error "镜像文件不存在: $img"
    return 1
  fi

  log_info "📦 镜像信息: $img"
  echo ""

  # 文件大小
  local size
  size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
  local size_human
  if command -v numfmt &>/dev/null; then
    size_human=$(numfmt --to=iec-i --suffix=B "$size" 2>/dev/null || echo "${size} bytes")
  else
    size_human="${size} bytes"
  fi
  echo "   文件大小: $size_human"

  # 解压查看元数据
  local tmp_dir
  tmp_dir=$(mktemp -d)
  trap "rm -rf $tmp_dir" RETURN

  tar -tzf "$img" metadata.json &>/dev/null && {
    tar -xzf "$img" -C "$tmp_dir" metadata.json 2>/dev/null
    local metadata="$tmp_dir/metadata.json"

    if [ -f "$metadata" ]; then
      echo ""
      echo "   元数据:"
      local name version created_at file_count
      name=$(python3 -c "import json; print(json.load(open('$metadata')).get('name', 'N/A'))" 2>/dev/null || echo "N/A")
      version=$(python3 -c "import json; print(json.load(open('$metadata')).get('version', 'N/A'))" 2>/dev/null || echo "N/A")
      created_at=$(python3 -c "import json; print(json.load(open('$metadata')).get('created_at', 'N/A'))" 2>/dev/null || echo "N/A")
      file_count=$(python3 -c "import json; print(json.load(open('$metadata')).get('file_count', 'N/A'))" 2>/dev/null || echo "N/A")

      echo "      名称: $name"
      echo "      版本: $version"
      echo "      创建时间: $created_at"
      echo "      文件数量: $file_count"

      # 显示打包选项
      python3 -c "
import json
metadata = json.load(open('$metadata'))
if 'options' in metadata:
    print('      打包选项:')
    for k, v in metadata['options'].items():
        status = '✓' if v else '✗'
        print(f'        $status {k}')
" 2>/dev/null || true

      # 显示文件列表
      python3 -c "
import json
metadata = json.load(open('$metadata'))
if 'files' in metadata:
    print('      文件列表:')
    for f in metadata['files'][:10]:
        print(f'        - {f}')
    if len(metadata['files']) > 10:
        print(f'        ... 共 {len(metadata[\"files\"])} 个文件')
" 2>/dev/null || true
    fi
  } || {
    echo "   ⚠ 无法读取元数据"
  }

  echo ""
  log_success "✅ 信息读取完成"
}

# 命令: verify
cmd_verify() {
  local img="$IMAGE_FILE"

  if [ ! -f "$img" ]; then
    log_error "镜像文件不存在: $img"
    return 1
  fi

  log_info "🔐 验证镜像: $img"
  echo ""

  # 检查 SHA256 文件
  local sha_file="${img}.sha256"
  if [ ! -f "$sha_file" ]; then
    log_error "未找到 SHA256 文件: $sha_file"
    return 1
  fi

  # 验证
  local expected actual
  expected=$(awk '{print $1}' "$sha_file" | head -n1)
  actual=$($(sha256_cmd) "$img" | awk '{print $1}')

  if [ "$expected" = "$actual" ]; then
    log_success "✅ SHA256 校验通过"
    echo "   哈希值: $actual"
  else
    log_error "❌ SHA256 校验失败"
    echo "   预期: $expected"
    echo "   实际: $actual"
    return 1
  fi
}

# 命令: list
cmd_list() {
  local dir="$1"

  if [ ! -d "$dir" ]; then
    log_error "目录不存在: $dir"
    return 1
  fi

  log_info "📁 镜像列表: $dir"
  echo ""

  local count=0
  local total_size=0

  for img in "$dir"/*.tar.gz; do
    [ -f "$img" ] || continue
    count=$((count + 1))

    local size
    size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
    total_size=$((total_size + size))

    local name version created_at="未知"
    local tmp_dir
    tmp_dir=$(mktemp -d)

    if tar -tzf "$img" metadata.json &>/dev/null; then
      tar -xzf "$img" -C "$tmp_dir" metadata.json 2>/dev/null
      if [ -f "$tmp_dir/metadata.json" ]; then
        name=$(python3 -c "import json; print(json.load(open('$tmp_dir/metadata.json')).get('name', '未知'))" 2>/dev/null || echo "未知")
        version=$(python3 -c "import json; print(json.load(open('$tmp_dir/metadata.json')).get('version', '未知'))" 2>/dev/null || echo "未知")
        created_at=$(python3 -c "import json; print(json.load(open('$tmp_dir/metadata.json')).get('created_at', '未知'))" 2>/dev/null || echo "未知")
      fi
    fi
    rm -rf "$tmp_dir"

    local size_human
    if command -v numfmt &>/dev/null; then
      size_human=$(numfmt --to=iec-i --suffix=B "$size" 2>/dev/null || echo "${size}B")
    else
      size_human="${size}B"
    fi

    echo "   $(basename "$img")"
    echo "      版本: $version | 大小: $size_human | 创建: $created_at"
    echo ""
  done

  if [ $count -eq 0 ]; then
    log_warn "未找到镜像文件"
    return
  fi

  local total_human
  if command -v numfmt &>/dev/null; then
    total_human=$(numfmt --to=iec-i --suffix=B "$total_size" 2>/dev/null || echo "${total_size}B")
  else
    total_human="${total_size}B"
  fi

  echo "   共 $count 个镜像, 总大小 $total_human"
  log_success "✅ 列表完成"
}

# 命令: extract
cmd_extract() {
  local img="$IMAGE_FILE"
  local dest="$EXTRACT_DIR"

  if [ ! -f "$img" ]; then
    log_error "镜像文件不存在: $img"
    return 1
  fi

  if [ -d "$dest" ]; then
    log_warn "目标目录已存在: $dest"
    read -p "是否覆盖? (y/N) " -n 1 -r reply
    echo
    if [[ ! $reply =~ ^[Yy]$ ]]; then
      log_info "已取消"
      return 0
    fi
  fi

  log_info "📦 解压镜像到: $dest"
  echo ""

  mkdir -p "$dest"
  tar -xzf "$img" -C "$dest"

  log_success "✅ 解压完成"
  echo ""
  echo "内容:"
  ls -la "$dest"
}

# 执行命令
case "$COMMAND" in
  info) cmd_info ;;
  verify) cmd_verify ;;
  list) cmd_list "$1" ;;
  extract) cmd_extract ;;
esac
