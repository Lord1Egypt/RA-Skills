#!/bin/bash
# OpenClaw 自定义打包脚本
# 支持选择打包内容、自定义路径、排除项

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/../common.sh"

# 默认选项
OUTPUT_FILE=""
NAME="openclaw-config"
INCLUDE_CONFIG=true
INCLUDE_WORKSPACE=true
INCLUDE_SKILLS=true
INCLUDE_DOCKER=true
INCLUDE_SCRIPTS=true
EXCLUDE_PATTERNS=()

usage() {
  cat <<EOF
用法: $0 [选项]

选项:
  --output <文件>         输出文件路径
  --name <名称>          镜像名称 (默认: openclaw-config)

打包内容选项:
  --[no-]config          包含/不包含配置文件 (默认: yes)
  --[no-]workspace      包含/不包含工作区文件 (默认: yes)
  --[no-]skills         包含/不包含 skills (默认: yes)
  --[no-]docker         包含/不包含 Docker 配置 (默认: yes)
  --[no-]scripts        包含/不包含部署脚本 (默认: yes)

排除选项:
  --exclude <pattern>    排除匹配的文件/目录 (可多次使用)
                         示例: --exclude "*.log" --exclude "memory/"

示例:
  $0 --output ./my-config.tar.gz
  $0 --output ./minimal.tar.gz --no-skills --no-docker
  $0 --output ./custom.tar.gz --exclude "*.log" --exclude "temp/*"
EOF
}

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --config)
      INCLUDE_CONFIG=true
      shift
      ;;
    --no-config)
      INCLUDE_CONFIG=false
      shift
      ;;
    --workspace)
      INCLUDE_WORKSPACE=true
      shift
      ;;
    --no-workspace)
      INCLUDE_WORKSPACE=false
      shift
      ;;
    --skills)
      INCLUDE_SKILLS=true
      shift
      ;;
    --no-skills)
      INCLUDE_SKILLS=false
      shift
      ;;
    --docker)
      INCLUDE_DOCKER=true
      shift
      ;;
    --no-docker)
      INCLUDE_DOCKER=false
      shift
      ;;
    --scripts)
      INCLUDE_SCRIPTS=true
      shift
      ;;
    --no-scripts)
      INCLUDE_SCRIPTS=false
      shift
      ;;
    --exclude)
      EXCLUDE_PATTERNS+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      log_error "未知参数: $1"
      usage
      exit 1
      ;;
  esac
done

if [ -z "$OUTPUT_FILE" ]; then
  log_error "请指定输出文件: --output <文件>"
  usage
  exit 1
fi

# 自动生成文件名
if [[ "$OUTPUT_FILE" != */* ]]; then
  VERSION="$(get_version "$PROJECT_DIR")"
  DATE="$(date +%Y%m%d)"
  OUTPUT_FILE="./openclaw-${VERSION}-${DATE}.tar.gz"
fi

# 设置trap清理
TEMP_DIR=$(mktemp -d)
trap cleanup_temp EXIT

OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
SKILLS_DIR="$OPENCLAW_DIR/workspace/skills"
METADATA_FILE="$TEMP_DIR/metadata.json"

VERSION="$(get_version "$PROJECT_DIR")"
BUILD_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

export TEMP_DIR METADATA_FILE NAME VERSION BUILD_TS

log_info "📦 自定义打包 OpenClaw 配置..."
echo "   名称: $NAME"
echo "   版本: $VERSION"
echo "   时间: $BUILD_TS"
echo "   输出: $OUTPUT_FILE"
echo ""
echo "📋 打包内容:"
[ "$INCLUDE_CONFIG" = "true" ] && echo "   ✓ 配置文件" || echo "   ✗ 配置文件"
[ "$INCLUDE_WORKSPACE" = "true" ] && echo "   ✓ 工作区" || echo "   ✗ 工作区"
[ "$INCLUDE_SKILLS" = "true" ] && echo "   ✓ Skills" || echo "   ✗ Skills"
[ "$INCLUDE_DOCKER" = "true" ] && echo "   ✓ Docker" || echo "   ✗ Docker"
[ "$INCLUDE_SCRIPTS" = "true" ] && echo "   ✓ 脚本" || echo "   ✗ 脚本"
if [ ${#EXCLUDE_PATTERNS[@]} -gt 0 ]; then
  echo "   排除: ${EXCLUDE_PATTERNS[*]}"
fi

# 构建打包内容列表
PACKAGE_ITEMS=()

# 1. 配置文件
if [ "$INCLUDE_CONFIG" = "true" ]; then
  echo ""
  log_info "📝 处理配置文件..."
  mkdir -p "$TEMP_DIR/config"
  if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
    python3 - "$OPENCLAW_DIR/openclaw.json" "$TEMP_DIR/config/openclaw.json" << 'PYTHON_SCRIPT'
import json
import sys
config_path = sys.argv[1]
output_path = sys.argv[2]
with open(config_path, 'r') as f:
    config = json.load(f)
sensitive_keys = ['api_key', 'apikey', 'api_secret', 'secret', 'token', 'password', 'credential', 'bottoken']
def sanitize(obj):
    if isinstance(obj, dict):
        return {k: sanitize(v) if k.lower() not in sensitive_keys else "$REMOVED" for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize(i) for i in obj]
    return obj
sanitized = sanitize(config)
with open(output_path, 'w') as f:
    json.dump(sanitized, f, indent=2, ensure_ascii=False)
PYTHON_SCRIPT
    echo "   ✓ config/openclaw.json"
    PACKAGE_ITEMS+=("config")
  else
    echo "   ⚠ 配置文件不存在"
  fi
fi

# 2. 工作区
if [ "$INCLUDE_WORKSPACE" = "true" ]; then
  echo ""
  log_info "📁 复制工作区文件..."
  mkdir -p "$TEMP_DIR/workspace"
  for file in SOUL.md IDENTITY.md USER.md AGENTS.md HEARTBEAT.md MEMORY.md TOOLS.md; do
    if [ -f "$WORKSPACE_DIR/$file" ]; then
      cp "$WORKSPACE_DIR/$file" "$TEMP_DIR/workspace/"
      echo "   ✓ $file"
    fi
  done
  if [ -d "$WORKSPACE_DIR/memory" ]; then
    cp -r "$WORKSPACE_DIR/memory" "$TEMP_DIR/workspace/"
    echo "   ✓ memory/"
  fi
  if [ -d "$TEMP_DIR/workspace" ] && [ "$(ls -A "$TEMP_DIR/workspace" 2>/dev/null)" ]; then
    PACKAGE_ITEMS+=("workspace")
  fi
fi

# 3. Skills
if [ "$INCLUDE_SKILLS" = "true" ]; then
  echo ""
  log_info "🛠️  复制 skills..."
  mkdir -p "$TEMP_DIR/skills"
  if [ -d "$SKILLS_DIR" ]; then
    cp -r "$SKILLS_DIR"/* "$TEMP_DIR/skills/" 2>/dev/null || true
    echo "   ✓ custom skills"
    PACKAGE_ITEMS+=("skills")
  else
    echo "   ⚠ skills 目录不存在"
  fi
fi

# 4. Docker
if [ "$INCLUDE_DOCKER" = "true" ]; then
  echo ""
  log_info "🐳 复制 Docker 配置..."
  if [ -d "$PROJECT_DIR/docker" ]; then
    mkdir -p "$TEMP_DIR/docker"
    (cd "$PROJECT_DIR/docker" && tar -cf - .) | (cd "$TEMP_DIR/docker" && tar -xf - 2>/dev/null || true)
    echo "   ✓ docker/"
    PACKAGE_ITEMS+=("docker")
  else
    echo "   ⚠ docker/ 目录不存在"
  fi
fi

# 5. 脚本
if [ "$INCLUDE_SCRIPTS" = "true" ]; then
  echo ""
  log_info "📜 复制部署脚本..."
  if [ -d "$PROJECT_DIR/build" ]; then
    mkdir -p "$TEMP_DIR/scripts"
    cp "$PROJECT_DIR/build/base/base_builder.sh" "$TEMP_DIR/scripts/export.sh" 2>/dev/null || true
    cp "$PROJECT_DIR/build/full/full_builder.sh" "$TEMP_DIR/scripts/deploy.sh" 2>/dev/null || true
    echo "   ✓ 脚本"
    PACKAGE_ITEMS+=("scripts")
  fi
fi

# 6. 创建安装脚本
echo ""
log_info "📜 生成安装脚本..."
cat > "$TEMP_DIR/install.sh" << 'INSTALL_SCRIPT'
#!/bin/bash
set -e
OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_DIR="$OPENCLAW_DIR.backup.$(date +%Y%m%d)"
echo "🚀 开始安装 OpenClaw 配置..."
if [ -d "$OPENCLAW_DIR" ]; then
  echo "📦 备份旧配置到 $BACKUP_DIR"
  mv "$OPENCLAW_DIR" "$BACKUP_DIR"
fi
mkdir -p "$OPENCLAW_DIR/workspace/memory"
[ -d "config" ] && cp config/openclaw.json "$OPENCLAW_DIR/" 2>/dev/null || true
[ -d "workspace" ] && cp -r workspace/* "$OPENCLAW_DIR/workspace/" 2>/dev/null || true
[ -d "skills" ] && mkdir -p "$OPENCLAW_DIR/workspace/skills" && cp -r skills/* "$OPENCLAW_DIR/workspace/skills/" 2>/dev/null || true
echo "✅ 安装完成！"
echo "⚠️  需要手动配置 API Keys"
INSTALL_SCRIPT
chmod +x "$TEMP_DIR/install.sh"
PACKAGE_ITEMS+=("install.sh")

# 7. 元数据
echo ""
log_info "🧾 生成镜像元数据..."
python3 - << PY
import json
import os
from pathlib import Path
temp_dir = Path(os.environ["TEMP_DIR"])
metadata_file = Path(os.environ["METADATA_FILE"])
files = []
for path in sorted(temp_dir.rglob("*")):
    if path.is_file():
        files.append(str(path.relative_to(temp_dir)))
metadata = {
    "name": os.environ.get("NAME", "openclaw-config"),
    "version": os.environ.get("VERSION", "dev"),
    "created_at": os.environ.get("BUILD_TS"),
    "file_count": len(files),
    "files": files,
    "options": {
        "include_config": os.environ.get("INCLUDE_CONFIG", "true") == "true",
        "include_workspace": os.environ.get("INCLUDE_WORKSPACE", "true") == "true",
        "include_skills": os.environ.get("INCLUDE_SKILLS", "true") == "true",
        "include_docker": os.environ.get("INCLUDE_DOCKER", "true") == "true",
        "include_scripts": os.environ.get("INCLUDE_SCRIPTS", "true") == "true",
    }
}
metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
PY
PACKAGE_ITEMS+=("metadata.json")

# 8. 打包
echo ""
log_info "📦 打包..."

# 构建 tar 命令
cd "$TEMP_DIR"
tar_args=("-czf" "$OUTPUT_FILE")
for item in "${PACKAGE_ITEMS[@]}"; do
  tar_args+=("$item")
done

# 添加排除模式
if [ ${#EXCLUDE_PATTERNS[@]} -gt 0 ]; then
  for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    tar_args+=("--exclude" "$pattern")
  done
done

tar "${tar_args[@]}"

# 9. SHA256
log_info "🔐 生成 SHA256 校验..."
SHA_CMD="$(sha256_cmd)"
SHA_FILE="${OUTPUT_FILE}.sha256"
($SHA_CMD "$OUTPUT_FILE" | awk '{print $1"  "FILENAME}' FILENAME="$(basename "$OUTPUT_FILE")") > "$SHA_FILE"
log_success "SHA256 校验文件已生成"

echo ""
log_success "✅ 完成！配置文件已保存到: $OUTPUT_FILE"
echo ""
echo "分享给他人后，他们只需运行："
echo "  tar -xzf $OUTPUT_FILE -C ~/"
echo "  ./install.sh"
