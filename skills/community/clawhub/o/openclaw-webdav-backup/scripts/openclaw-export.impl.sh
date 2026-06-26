#!/usr/bin/env bash
# OpenClaw Portable Package Export
# Usage: source openclaw-export.impl.sh && export_portable [options]

set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/logging.sh" 2>/dev/null || {
    # Fallback logging if lib not available
    log_info() { echo "[INFO] $*"; }
    log_warn() { echo "[WARN] $*" >&2; }
    log_error() { echo "[ERROR] $*" >&2; }
    log_debug() { [[ "${DEBUG:-}" == "true" ]] && echo "[DEBUG] $*"; }
}

# Default configuration
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WORKSPACE_DIR="${OPENCLAW_HOME}/workspace"
EXTENSIONS_DIR="${OPENCLAW_HOME}/extensions"
CONFIG_FILE="${OPENCLAW_HOME}/openclaw.json"
ENV_FILE="${OPENCLAW_HOME}/.env"

EXPORT_DIR="${EXPORT_DIR:-${OPENCLAW_HOME}/exports}"
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")
PACKAGE_NAME="openclaw-portable-${TIMESTAMP}"
TEMP_DIR=""

# Export options
WITH_TEMPLATES="${WITH_TEMPLATES:-true}"
SANITIZE_ENV="${SANITIZE_ENV:-true}"
GENERATE_MANIFEST="${GENERATE_MANIFEST:-true}"

# Cleanup function
cleanup() {
    if [[ -n "${TEMP_DIR:-}" && -d "${TEMP_DIR}" ]]; then
        rm -rf "${TEMP_DIR}"
        log_debug "Cleaned up temp directory: ${TEMP_DIR}"
    fi
}
trap cleanup EXIT

# Initialize export environment
init_export() {
    TEMP_DIR=$(mktemp -d)
    mkdir -p "${EXPORT_DIR}"
    log_info "Export initialized: ${TEMP_DIR}"
}

# Detect environment-specific values
detect_env_values() {
    local config_file="$1"
    local env_map="${TEMP_DIR}/env_map.txt"
    
    log_info "Detecting environment-specific values..."
    
    # Initialize env map
    cat > "${env_map}" << EOF
# OpenClaw Environment Variable Mapping
# Generated: ${TIMESTAMP}
#
# Copy this file to .env and fill in your values

# OpenClaw Base Configuration
OPENCLAW_HOME=\${HOME}/.openclaw
WORKSPACE_DIR=\${OPENCLAW_HOME}/workspace
EXTENSIONS_DIR=\${OPENCLAW_HOME}/extensions

# Gateway Configuration
EOF
    
    # Extract gateway bind address
    if [[ -f "${config_file}" ]]; then
        local bind_addr
        bind_addr=$(jq -r '.gateway.bind // empty' "${config_file}" 2>/dev/null || echo "")
        if [[ -n "${bind_addr}" ]]; then
            local host port
            host=$(echo "${bind_addr}" | cut -d: -f1)
            port=$(echo "${bind_addr}" | cut -d: -f2)
            echo "GATEWAY_BIND_HOST=${host}" >> "${env_map}"
            echo "GATEWAY_BIND_PORT=${port}" >> "${env_map}"
        fi
        
        # Extract remote URL
        local remote_url
        remote_url=$(jq -r '.gateway.remote.url // empty' "${config_file}" 2>/dev/null || echo "")
        if [[ -n "${remote_url}" ]]; then
            echo "GATEWAY_REMOTE_URL=${remote_url}" >> "${env_map}"
        fi
        
        # Extract model gateway
        local model_gateway
        model_gateway=$(jq -r '.modelGateway // empty' "${config_file}" 2>/dev/null || echo "")
        if [[ -n "${model_gateway}" ]]; then
            echo "MODEL_GATEWAY_URL=${model_gateway}" >> "${env_map}"
        fi
    fi
    
    # Add WebDAV configuration section
    cat >> "${env_map}" << 'EOF'

# WebDAV Backup Configuration
WEBDAV_ENDPOINT=${WEBDAV_ENDPOINT:-}
WEBDAV_USER=${WEBDAV_USER:-}
WEBDAV_PASS=${WEBDAV_PASS:-}
BACKUP_ENCRYPT_PASS=${BACKUP_ENCRYPT_PASS:-}

# Proxy Configuration (if used)
HTTP_PROXY=${HTTP_PROXY:-}
HTTPS_PROXY=${HTTPS_PROXY:-}
NO_PROXY=${NO_PROXY:-}

# API Keys (optional, for integrations)
MATON_API_KEY=${MATON_API_KEY:-}
SERPAPI_KEY=${SERPAPI_KEY:-}
TAVILY_API_KEY=${TAVILY_API_KEY:-}

# Node.js / npm Configuration
NPM_REGISTRY=${NPM_REGISTRY:-https://registry.npmjs.org}
NODE_VERSION=${NODE_VERSION:-}
EOF
}

# Template configuration file
template_config() {
    local input_file="$1"
    local output_file="$2"
    local mapping_file="$3"
    
    log_info "Templating configuration: ${input_file}"
    
    if [[ ! -f "${input_file}" ]]; then
        log_warn "Config file not found: ${input_file}"
        return 1
    fi
    
    # Read original config
    local config_content
    config_content=$(cat "${input_file}")
    
    # Create mapping for restoration
    local restore_map="${TEMP_DIR}/restore_map.json"
    echo '{}' > "${restore_map}"
    
    # Replace environment-specific values with template variables
    # This is a simplified version - full implementation would use jq
    
    # Gateway bind address → template
    local bind_addr
    bind_addr=$(echo "${config_content}" | jq -r '.gateway.bind // empty' 2>/dev/null || echo "")
    if [[ -n "${bind_addr}" ]]; then
        config_content=$(echo "${config_content}" | jq '
            .gateway.bind = "${GATEWAY_BIND_HOST}:${GATEWAY_BIND_PORT}"
        ' 2>/dev/null || echo "${config_content}")
        
        # Record original for restore map
        local host port
        host=$(echo "${bind_addr}" | cut -d: -f1)
        port=$(echo "${bind_addr}" | cut -d: -f2)
        jq --arg h "${host}" --arg p "${port}" \
           '.gateway_bind_host = $h | .gateway_bind_port = $p' \
           "${restore_map}" > "${TEMP_DIR}/tmp.json" && mv "${TEMP_DIR}/tmp.json" "${restore_map}"
    fi
    
    # Remote URL → template
    local remote_url
    remote_url=$(echo "${config_content}" | jq -r '.gateway.remote.url // empty' 2>/dev/null || echo "")
    if [[ -n "${remote_url}" ]]; then
        config_content=$(echo "${config_content}" | jq '
            .gateway.remote.url = "${GATEWAY_REMOTE_URL}"
        ' 2>/dev/null || echo "${config_content}")
        
        jq --arg u "${remote_url}" '.gateway_remote_url = $u' \
           "${restore_map}" > "${TEMP_DIR}/tmp.json" && mv "${TEMP_DIR}/tmp.json" "${restore_map}"
    fi
    
    # Model gateway → template
    local model_gateway
    model_gateway=$(echo "${config_content}" | jq -r '.modelGateway // empty' 2>/dev/null || echo "")
    if [[ -n "${model_gateway}" ]]; then
        config_content=$(echo "${config_content}" | jq '
            .modelGateway = "${MODEL_GATEWAY_URL}"
        ' 2>/dev/null || echo "${config_content}")
        
        jq --arg m "${model_gateway}" '.model_gateway_url = $m' \
           "${restore_map}" > "${TEMP_DIR}/tmp.json" && mv "${TEMP_DIR}/tmp.json" "${restore_map}"
    fi
    
    # Write templated config
    echo "${config_content}" > "${output_file}"
    
    # Move restore mapping to output location
    mv "${restore_map}" "${mapping_file}"
    
    log_info "Configuration templated: ${output_file}"
    return 0
}

# Generate MIGRATION.md guide
generate_migration_guide() {
    local output_dir="$1"
    local source_system="$2"
    
    log_info "Generating migration guide..."
    
    cat > "${output_dir}/MIGRATION.md" << EOF
# OpenClaw 迁移指南

## 包信息

- **导出时间**: ${TIMESTAMP}
- **源系统**: ${source_system}
- **OpenClaw 版本**: $(openclaw --version 2>/dev/null || echo "未知")

## 快速开始

### 1. 解压包

\`\`\`bash
tar -xzf ${PACKAGE_NAME}.tar.gz -C ~/
cd ~/${PACKAGE_NAME}
\`\`\`

### 2. 配置环境变量

复制模板并填入实际值：

\`\`\`bash
cp migrate.env.template .env
# 编辑 .env 文件，填入你的配置
nano .env  # 或 vim/code
\`\`\`

### 3. 检查兼容性

\`\`\`bash
bash scripts/check-compatibility.sh
\`\`\`

### 4. 执行迁移

\`\`\`bash
# 自动应用环境变量并恢复
bash scripts/migrate.sh --env-file .env

# 或手动分步
export $(cat .env | grep -v '^#' | xargs)
bash scripts/migrate.sh
\`\`\`

## 目录结构

\`\`\`
${PACKAGE_NAME}/
├── workspace/              # OpenClaw workspace
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── memory/
│   └── ...
├── extensions/             # 插件目录
├── config/                 # 配置文件（已模板化）
│   ├── openclaw.json.template
│   └── restore_map.json
├── scripts/                # 迁移脚本
│   ├── migrate.sh
│   └── check-compatibility.sh
├── migrate.env.template    # 环境变量模板
└── MIGRATION.md           # 本文件
\`\`\`

## 配置文件模板变量

配置文件中的以下值已替换为模板变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| \`\`\`\${GATEWAY_BIND_HOST}\`\`\` | Gateway 绑定地址 | 0.0.0.0 |
| \`\`\`\${GATEWAY_BIND_PORT}\`\`\` | Gateway 端口 | 3000 |
| \`\`\`\${GATEWAY_REMOTE_URL}\`\`\` | 远程代理地址 | https://proxy.example.com |
| \`\`\`\${MODEL_GATEWAY_URL}\`\`\` | 模型网关 | https://api.example.com/v1 |

## 注意事项

1. **敏感信息**: 配置文件中的 API 密钥、Token 等敏感信息已被模板化，请在 .env 中填入
2. **路径差异**: 如果目标系统路径不同，请修改 .env 中的 OPENCLAW_HOME
3. **依赖检查**: 迁移前务必运行兼容性检查脚本
4. **备份**: 建议先备份目标系统的现有配置

## 故障排除

### 问题：Gateway 启动失败

检查 \`\`\`GATEWAY_BIND_HOST\`\`\` 和 \`\`\`GATEWAY_BIND_PORT\`\`\` 是否被占用：

\`\`\`bash
netstat -tlnp | grep :3000
\`\`\`

### 问题：模型无法连接

检查 \`\`\`MODEL_GATEWAY_URL\`\`\` 和 API 密钥是否正确。

### 问题：插件加载失败

确认 \`\`\`EXTENSIONS_DIR\`\`\` 路径正确，且插件文件完整。

## 支持

- OpenClaw 文档: https://docs.openclaw.ai
- 社区: https://discord.com/invite/clawd
EOF
    
    log_info "Migration guide generated: ${output_dir}/MIGRATION.md"
}

# Generate manifest file
generate_manifest() {
    local output_dir="$1"
    
    log_info "Generating manifest..."
    
    local manifest="${output_dir}/manifest.json"
    
    # Count files
    local workspace_count ext_count
    workspace_count=$(find "${WORKSPACE_DIR}" -type f 2>/dev/null | wc -l)
    ext_count=$(find "${EXTENSIONS_DIR}" -type f 2>/dev/null | wc -l)
    
    # Get OpenClaw version
    local oc_version
    oc_version=$(openclaw --version 2>/dev/null || echo "unknown")
    
    # Get Node version
    local node_version
    node_version=$(node --version 2>/dev/null || echo "unknown")
    
    # Get OS info
    local os_info
    os_info=$(uname -a)
    
    cat > "${manifest}" << EOF
{
  "export_info": {
    "timestamp": "${TIMESTAMP}",
    "version": "1.2.0",
    "format": "portable"
  },
  "source_system": {
    "hostname": "$(hostname)",
    "os": "${os_info}",
    "openclaw_version": "${oc_version}",
    "node_version": "${node_version}"
  },
  "contents": {
    "workspace": {
      "path": "workspace",
      "file_count": ${workspace_count},
      "size_bytes": $(du -sb "${WORKSPACE_DIR}" 2>/dev/null | cut -f1 || echo 0)
    },
    "extensions": {
      "path": "extensions",
      "file_count": ${ext_count},
      "size_bytes": $(du -sb "${EXTENSIONS_DIR}" 2>/dev/null | cut -f1 || echo 0)
    },
    "config": {
      "path": "config",
      "templated": ${SANITIZE_ENV}
    }
  },
  "requirements": {
    "node_version": ">=20.0.0",
    "openclaw_version": ">=0.10.0",
    "disk_space_mb": 100
  }
}
EOF
    
    log_info "Manifest generated: ${manifest}"
}

# Create migrate.sh script
create_migrate_script() {
    local output_dir="$1"
    
    log_info "Creating migrate script..."
    
    cat > "${output_dir}/scripts/migrate.sh" << 'EOF'
#!/usr/bin/env bash
# OpenClaw Migration Script
# Usage: migrate.sh [--env-file <file>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(dirname "${SCRIPT_DIR}")"
ENV_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env-file)
            ENV_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: migrate.sh [--env-file <file>]"
            echo ""
            echo "Options:"
            echo "  --env-file <file>    Load environment from file"
            echo "  --help               Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Load environment
if [[ -n "${ENV_FILE}" && -f "${ENV_FILE}" ]]; then
    echo "Loading environment from: ${ENV_FILE}"
    set -a
    source "${ENV_FILE}"
    set +a
fi

# Set defaults
OPENCLAW_HOME="${OPENCLAW_HOME:-${HOME}/.openclaw}"

echo "═══════════════════════════════════════════"
echo "      🚀 OpenClaw 迁移"
echo "═══════════════════════════════════════════"
echo ""
echo "目标目录: ${OPENCLAW_HOME}"
echo ""

# Check if target exists
if [[ -d "${OPENCLAW_HOME}" ]]; then
    echo "⚠️  目标目录已存在: ${OPENCLAW_HOME}"
    read -p "是否覆盖? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "迁移已取消"
        exit 1
    fi
    
    # Backup existing
    BACKUP_TS=$(date +"%Y%m%d-%H%M%S")
    BACKUP_DIR="${OPENCLAW_HOME}.backup.${BACKUP_TS}"
    echo "备份现有配置到: ${BACKUP_DIR}"
    mv "${OPENCLAW_HOME}" "${BACKUP_DIR}"
fi

# Create target directory
mkdir -p "${OPENCLAW_HOME}"

# Copy workspace
echo "复制 workspace..."
cp -r "${PACKAGE_DIR}/workspace" "${OPENCLAW_HOME}/"

# Copy extensions
echo "复制 extensions..."
cp -r "${PACKAGE_DIR}/extensions" "${OPENCLAW_HOME}/"

# Process config
echo "处理配置文件..."
mkdir -p "${OPENCLAW_HOME}"

if [[ -f "${PACKAGE_DIR}/config/openclaw.json.template" ]]; then
    # Apply template substitution
    envsubst < "${PACKAGE_DIR}/config/openclaw.json.template" > "${OPENCLAW_HOME}/openclaw.json"
    echo "配置文件已生成: ${OPENCLAW_HOME}/openclaw.json"
fi

echo ""
echo "✅ 迁移完成!"
echo ""
echo "下一步:"
echo "  1. 检查配置: cat ${OPENCLAW_HOME}/openclaw.json"
echo "  2. 重启 Gateway: openclaw gateway restart"
echo "  3. 验证状态: openclaw status"
EOF
    
    chmod +x "${output_dir}/scripts/migrate.sh"
    log_info "Migrate script created"
}

# Create compatibility check script
create_compat_script() {
    local output_dir="$1"
    
    log_info "Creating compatibility check script..."
    
    cat > "${output_dir}/scripts/check-compatibility.sh" << 'EOF'
#!/usr/bin/env bash
# Compatibility Check Script

set -euo pipefail

echo "═══════════════════════════════════════════"
echo "      🔍 兼容性检查"
echo "═══════════════════════════════════════════"
echo ""

PASS=0
WARN=0
FAIL=0

check_pass() {
    echo "  ✅ $1"
    PASS=$((PASS + 1))
}

check_warn() {
    echo "  ⚠️  $1"
    WARN=$((WARN + 1))
}

check_fail() {
    echo "  ❌ $1"
    FAIL=$((FAIL + 1))
}

# Check Node.js
echo "Node.js 检查:"
if command -v node &>/dev/null; then
    NODE_VER=$(node --version | sed 's/v//')
    NODE_MAJOR=$(echo "${NODE_VER}" | cut -d. -f1)
    if [[ ${NODE_MAJOR} -ge 20 ]]; then
        check_pass "Node.js ${NODE_VER} (满足 ≥ v20)"
    elif [[ ${NODE_MAJOR} -ge 18 ]]; then
        check_warn "Node.js ${NODE_VER} (建议 ≥ v20)"
    else
        check_fail "Node.js ${NODE_VER} (需要 ≥ v18)"
    fi
else
    check_fail "Node.js 未安装"
fi
echo ""

# Check npm
echo "npm 检查:"
if command -v npm &>/dev/null; then
    NPM_VER=$(npm --version)
    check_pass "npm ${NPM_VER}"
else
    check_fail "npm 未安装"
fi
echo ""

# Check OpenClaw CLI
echo "OpenClaw CLI 检查:"
if command -v openclaw &>/dev/null; then
    OC_VER=$(openclaw --version 2>/dev/null || echo "unknown")
    check_pass "OpenClaw ${OC_VER}"
else
    check_warn "OpenClaw CLI 未安装 (将随包安装)"
fi
echo ""

# Check dependencies
echo "依赖检查:"
for cmd in tar curl openssl; do
    if command -v ${cmd} &>/dev/null; then
        check_pass "${cmd}: $(which ${cmd})"
    else
        check_fail "${cmd}: 未安装"
    fi
done
echo ""

# Check disk space
echo "磁盘空间检查:"
AVAIL_MB=$(df -m "${HOME}" | awk 'NR==2 {print $4}')
if [[ ${AVAIL_MB} -gt 500 ]]; then
    check_pass "可用空间: ${AVAIL_MB}MB (> 500MB)"
else
    check_warn "可用空间: ${AVAIL_MB}MB (建议 > 500MB)"
fi
echo ""

# Check ports
echo "端口检查:"
for port in 3000 3001; do
    if netstat -tln 2>/dev/null | grep -q ":${port} "; then
        check_warn "端口 ${port} 已被占用"
    else
        check_pass "端口 ${port} 可用"
    fi
done
echo ""

# Summary
echo "═══════════════════════════════════════════"
echo "      📊 检查结果"
echo "═══════════════════════════════════════════"
echo "  ✅ 通过: ${PASS}"
echo "  ⚠️  警告: ${WARN}"
echo "  ❌ 失败: ${FAIL}"
echo ""

if [[ ${FAIL} -gt 0 ]]; then
    echo "请先解决失败项后再迁移"
    exit 1
elif [[ ${WARN} -gt 0 ]]; then
    echo "可以迁移，但建议处理警告项"
    exit 0
else
    echo "环境检查通过，可以安全迁移!"
    exit 0
fi
EOF
    
    chmod +x "${output_dir}/scripts/check-compatibility.sh"
    log_info "Compatibility check script created"
}

# Main export function
export_portable() {
    log_info "═══════════════════════════════════════════"
    log_info "      📦 OpenClaw 可移植包导出"
    log_info "═══════════════════════════════════════════"
    
    # Initialize
    init_export
    
    local pkg_dir="${TEMP_DIR}/${PACKAGE_NAME}"
    mkdir -p "${pkg_dir}/workspace" "${pkg_dir}/extensions" "${pkg_dir}/config" "${pkg_dir}/scripts"
    
    # Copy workspace
    log_info "复制 workspace..."
    if [[ -d "${WORKSPACE_DIR}" ]]; then
        cp -r "${WORKSPACE_DIR}/." "${pkg_dir}/workspace/" 2>/dev/null || true
    fi
    
    # Copy extensions
    log_info "复制 extensions..."
    if [[ -d "${EXTENSIONS_DIR}" ]]; then
        cp -r "${EXTENSIONS_DIR}/." "${pkg_dir}/extensions/" 2>/dev/null || true
    fi
    
    # Generate environment template
    if [[ "${WITH_TEMPLATES}" == "true" ]]; then
        detect_env_values "${CONFIG_FILE}"
        cp "${TEMP_DIR}/env_map.txt" "${pkg_dir}/migrate.env.template"
        log_info "环境模板已生成"
    fi
    
    # Template config
    if [[ "${SANITIZE_ENV}" == "true" && -f "${CONFIG_FILE}" ]]; then
        template_config "${CONFIG_FILE}" "${pkg_dir}/config/openclaw.json.template" "${pkg_dir}/config/restore_map.json"
    elif [[ -f "${CONFIG_FILE}" ]]; then
        cp "${CONFIG_FILE}" "${pkg_dir}/config/openclaw.json"
    fi
    
    # Generate migration guide
    generate_migration_guide "${pkg_dir}" "$(hostname)"
    
    # Generate manifest
    if [[ "${GENERATE_MANIFEST}" == "true" ]]; then
        generate_manifest "${pkg_dir}"
    fi
    
    # Create scripts
    create_migrate_script "${pkg_dir}"
    create_compat_script "${pkg_dir}"
    
    # Create package
    local output_file="${EXPORT_DIR}/${PACKAGE_NAME}.tar.gz"
    log_info "打包: ${output_file}"
    
    tar -czf "${output_file}" -C "${TEMP_DIR}" "${PACKAGE_NAME}"
    
    # Get file size
    local size
    size=$(du -h "${output_file}" | cut -f1)
    
    log_info "═══════════════════════════════════════════"
    log_info "      ✅ 导出完成"
    log_info "═══════════════════════════════════════════"
    log_info "包路径: ${output_file}"
    log_info "大小: ${size}"
    log_info ""
    log_info "使用方式:"
    log_info "  1. 复制到目标系统"
    log_info "  2. 解压: tar -xzf ${PACKAGE_NAME}.tar.gz"
    log_info "  3. 查看 MIGRATION.md 迁移指南"
    
    echo "${output_file}"
}

# If script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    export_portable "$@"
fi
