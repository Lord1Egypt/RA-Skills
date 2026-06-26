#!/bin/bash
# OpenClaw 打包脚本
# 用法: ./base_builder.sh --output ./openclaw-{version}-{date}.tar.gz

set -euo pipefail

# 加载通用函数
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/../common.sh"

OUTPUT_FILE=""
NAME="openclaw-config"

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
    -h|--help)
      echo "用法: $0 --output <输出文件路径> [--name <配置名称>]"
      echo "示例: $0 --output ./openclaw-latest.tar.gz"
      exit 0
      ;;
    *)
      log_error "未知参数: $1"
      exit 1
      ;;
  esac
done

if [ -z "$OUTPUT_FILE" ]; then
  echo "用法: $0 --output <输出文件路径> [--name <配置名称>]"
  exit 1
fi

# 自动生成文件名（如果未指定）
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

VERSION="$(get_version)"
if [ -z "$VERSION" ]; then
  VERSION="dev"
fi
BUILD_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

export TEMP_DIR METADATA_FILE NAME VERSION BUILD_TS

log_info "📦 打包 OpenClaw 配置..."
echo "   名称: $NAME"
echo "   版本: $VERSION"
echo "   时间: $BUILD_TS"
echo "   输出: $OUTPUT_FILE"

# 1. 导出 config.json (移除敏感信息)
echo "📝 处理配置文件..."
mkdir -p "$TEMP_DIR/config"
if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
  python3 - "$OPENCLAW_DIR/openclaw.json" "$TEMP_DIR/config/openclaw.json" << 'PYTHON_SCRIPT'
import json
import sys

config_path = sys.argv[1]
output_path = sys.argv[2]

with open(config_path, 'r') as f:
    config = json.load(f)

# 移除敏感信息 (统一小写比较)
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

print("敏感信息已移除")
PYTHON_SCRIPT
else
  echo "⚠️  找不到配置文件"
fi

# 2. 导出 workspace 文件
echo "📁 复制工作区文件..."
mkdir -p "$TEMP_DIR/workspace"
for file in SOUL.md IDENTITY.md USER.md AGENTS.md HEARTBEAT.md MEMORY.md TOOLS.md; do
  if [ -f "$WORKSPACE_DIR/$file" ]; then
    cp "$WORKSPACE_DIR/$file" "$TEMP_DIR/workspace/"
    echo "   ✓ $file"
  fi
done

# 复制 memory 目录
if [ -d "$WORKSPACE_DIR/memory" ]; then
  cp -r "$WORKSPACE_DIR/memory" "$TEMP_DIR/workspace/"
  echo "   ✓ memory/"
fi

# 3. 导出 skills
echo "🛠️  复制 skills..."
mkdir -p "$TEMP_DIR/skills"
if [ -d "$SKILLS_DIR" ]; then
  cp -r "$SKILLS_DIR"/* "$TEMP_DIR/skills/" 2>/dev/null || true
  echo "   ✓ custom skills"
fi

# 4. 复制 docker 相关文件（可选）
echo "🐳 复制 Docker 配置..."
if [ -d "$PROJECT_DIR/docker" ]; then
  (cd "$PROJECT_DIR/docker" && tar -cf - .) | (mkdir -p "$TEMP_DIR/docker" && cd "$TEMP_DIR/docker" && tar -xf - 2>/dev/null || true)
  echo "   ✓ docker/"
else
  echo "   ⚠ docker/ 目录不存在，跳过"
fi

# 5. 创建安装脚本
echo "📜 生成安装脚本..."
cat > "$TEMP_DIR/install.sh" << 'INSTALL_SCRIPT'
#!/bin/bash
# OpenClaw 配置安装脚本

set -e

OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_DIR="$OPENCLAW_DIR.backup.$(date +%Y%m%d)"

echo "🚀 开始安装 OpenClaw 配置..."

# 备份旧配置
if [ -d "$OPENCLAW_DIR" ]; then
  echo "📦 备份旧配置到 $BACKUP_DIR"
  mv "$OPENCLAW_DIR" "$BACKUP_DIR"
fi

# 创建目录结构
mkdir -p "$OPENCLAW_DIR/workspace/memory"

# 复制配置文件
if [ -d "config" ]; then
  echo "📝 安装配置文件..."
  cp config/openclaw.json "$OPENCLAW_DIR/"
fi

# 复制工作区文件
if [ -d "workspace" ]; then
  echo "📁 安装工作区文件..."
  cp -r workspace/* "$OPENCLAW_DIR/workspace/"
fi

# 安装 skills
if [ -d "skills" ]; then
  echo "🛠️  安装 skills..."
  mkdir -p "$OPENCLAW_DIR/workspace/skills"
  cp -r skills/* "$OPENCLAW_DIR/workspace/skills/"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "⚠️  需要手动配置："
echo "   1. 运行 openclaw configure 配置凭据"
echo "   2. 编辑 ~/.openclaw/openclaw.json 填入 API keys"
echo "   3. 运行 openclaw gateway start 启动"
echo ""
INSTALL_SCRIPT

chmod +x "$TEMP_DIR/install.sh"

# 6. 复制 scripts
echo "📜 复制部署脚本..."
mkdir -p "$TEMP_DIR/scripts"
if [ -d "$PROJECT_DIR/scripts" ]; then
  cp "$PROJECT_DIR/scripts/deploy.sh" "$TEMP_DIR/scripts/" 2>/dev/null || true
fi

# 7. 镜像元数据
echo "🧾 生成镜像元数据..."
python3 - << 'PY'
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
}

metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
print(f"元数据已生成: {metadata_file}")
PY

# 8. 打包
log_info "📦 打包..."
cd "$TEMP_DIR"

# 构建打包文件列表
PACKAGE_FILES="config workspace skills install.sh metadata.json"
[ -d "docker" ] && PACKAGE_FILES="$PACKAGE_FILES docker"
[ -d "scripts" ] && PACKAGE_FILES="$PACKAGE_FILES scripts"

tar -czf "$OUTPUT_FILE" $PACKAGE_FILES

# 9. 生成 SHA256
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
echo ""
echo "或使用 Docker 部署："
echo "  cd docker && cp .env.example .env"
echo "  # 编辑 .env 填入 API Keys"
echo "  docker-compose up -d"
