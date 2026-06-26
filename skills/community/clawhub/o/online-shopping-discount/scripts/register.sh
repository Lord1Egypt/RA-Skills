#!/bin/bash

# 注册认证脚本 - 获取 API 访问凭证
# 用途：向服务端注册并获取有效的身份凭证，支持本地缓存

set -e

# 配置
API_ENDPOINT="${SHOPPING_API_ENDPOINT:-https://online-shopping-discount.io.mlj130.com}"
TIMEOUT="${SHOPPING_API_TIMEOUT:-30}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIAL_FILE="$SCRIPT_DIR/.credential_cache"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 错误处理函数
error_exit() {
    echo -e "${RED}错误: $1${NC}" >&2
    echo "{\"status\":\"error\",\"error_code\":\"$2\",\"message\":\"$1\"}"
    exit 1
}

# 日志函数
log() {
    echo -e "${GREEN}[INFO]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

# 确保依赖存在
ensure_dep() {
    if ! command -v "$1" >/dev/null 2>&1; then
        error_exit "缺少依赖: $1，请先安装后再试" "MISSING_DEP"
    fi
}

# 规范化 API 地址，移除末尾斜杠
normalized_endpoint() {
    local endpoint="$1"
    endpoint="${endpoint%%/}"
    echo "$endpoint"
}

# 获取设备 UUID（macOS 使用 IOPlatformUUID，Linux 尝试 product_uuid 或 machine-id）
get_device_uuid() {
    local uuid=""

    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v ioreg >/dev/null 2>&1; then
            uuid=$(ioreg -rd1 -c IOPlatformExpertDevice 2>/dev/null | awk -F'"' '/IOPlatformUUID/ {print $4; exit}')
        fi
    elif [[ "$OSTYPE" == "linux"* ]] || [[ "$OSTYPE" == "gnu"* ]]; then
        if [ -r /sys/class/dmi/id/product_uuid ]; then
            uuid=$(cat /sys/class/dmi/id/product_uuid 2>/dev/null)
        elif [ -r /etc/machine-id ]; then
            uuid=$(cat /etc/machine-id 2>/dev/null)
        fi
    elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]] || [[ "$OSTYPE" == "win32"* ]]; then
        if command -v powershell.exe >/dev/null 2>&1; then
            uuid=$(powershell.exe -NoProfile -Command "(Get-CimInstance Win32_ComputerSystemProduct).UUID" 2>/dev/null | tr -d '\r')
        elif command -v pwsh >/dev/null 2>&1; then
            uuid=$(pwsh -NoProfile -Command "(Get-CimInstance Win32_ComputerSystemProduct).UUID" 2>/dev/null | tr -d '\r')
        elif command -v wmic >/dev/null 2>&1; then
            uuid=$(wmic csproduct get UUID 2>/dev/null | awk 'NF && $0 !~ /UUID/ {print; exit}')
        fi
    else
        if [ -r /sys/class/dmi/id/product_uuid ]; then
            uuid=$(cat /sys/class/dmi/id/product_uuid 2>/dev/null)
        elif [ -r /etc/machine-id ]; then
            uuid=$(cat /etc/machine-id 2>/dev/null)
        fi
    fi

    uuid=$(echo "$uuid" | tr -d '[:space:]"')
    echo "$uuid"
}

# 检查凭证是否过期
is_credential_expired() {
    local expires_at=$1
    
    # 将过期时间转换为时间戳
    local expires_timestamp
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        expires_timestamp=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$expires_at" +%s 2>/dev/null || echo 0)
    else
        # Linux
        expires_timestamp=$(date -d "$expires_at" +%s 2>/dev/null || echo 0)
    fi
    
    local current_timestamp=$(date +%s)
    
    # 如果距离过期时间不足1小时，也认为已过期（提前刷新）
    local buffer_time=3600
    
    if [ $((expires_timestamp - current_timestamp)) -le $buffer_time ]; then
        return 0  # 已过期
    else
        return 1  # 未过期
    fi
}

# 从本地读取凭证
load_cached_credential() {
    if [ ! -f "$CREDENTIAL_FILE" ]; then
        return 1
    fi
    
    # 读取缓存的凭证
    local cached_data=$(cat "$CREDENTIAL_FILE" 2>/dev/null)
    if [ -z "$cached_data" ]; then
        return 1
    fi
    
    # 验证 JSON 格式
    if ! echo "$cached_data" | jq . >/dev/null 2>&1; then
        warn "缓存的凭证格式无效，将重新注册"
        return 1
    fi
    
    # 提取过期时间
    local expires_at=$(echo "$cached_data" | jq -r '.expires_at')
    
    # 检查是否过期
    if is_credential_expired "$expires_at"; then
        log "缓存的凭证已过期，将重新注册"
        return 1
    fi
    
    log "使用缓存的凭证（有效期至: $expires_at）"
    echo "$cached_data"
    return 0
}

# 保存凭证到本地
save_credential() {
    local credential_data=$1
    
    echo "$credential_data" > "$CREDENTIAL_FILE"
    chmod 600 "$CREDENTIAL_FILE"  # 设置文件权限，仅所有者可读写
    
    log "凭证已保存到本地缓存"
}

# 生成随机用户名和密码
generate_random_string() {
    local length=$1
    if command -v openssl >/dev/null 2>&1; then
        openssl rand -base64 32 2>/dev/null | tr -dc 'a-zA-Z0-9' | head -c "$length"
    else
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c "$length"
    fi
}

generate_username() {
    local suffix
    suffix=$(date +%s)
    local random_part
    random_part=$(generate_random_string 6)
    echo "ai_shopper_${suffix}_${random_part}"
}

generate_password() {
    generate_random_string 14
}

# 执行注册流程
do_register() {
    ensure_dep curl
    ensure_dep jq

    local username="$1"
    local password="$2"

    local device_uuid_used=false
    if [ -z "$username" ]; then
        local device_uuid
        device_uuid=$(get_device_uuid)
        if [ -n "$device_uuid" ]; then
            username="$device_uuid"
            device_uuid_used=true
            log "检测到设备 UUID，使用其作为用户名: $username"
        else
            username=$(generate_username)
            log "未获取到设备 UUID，将使用随机用户名: $username"
        fi
    fi
    if [ -z "$password" ]; then
        password=$(generate_password)
    fi

    log "开始注册认证流程..."
    local endpoint
    endpoint="$(normalized_endpoint "$API_ENDPOINT")/user/register"

    local response
    if ! response=$(curl -s -X POST \
        -H "Content-Type: application/x-www-form-urlencoded" \
        --data-urlencode "username=$username" \
        --data-urlencode "password=$password" \
        --max-time "$TIMEOUT" \
        "$endpoint"); then
        error_exit "注册接口请求失败，请检查服务是否已在 $API_ENDPOINT 运行" "NETWORK_ERROR"
    fi

    if ! echo "$response" | jq . >/dev/null 2>&1; then
        error_exit "注册接口返回了无效的 JSON 数据" "API_ERROR"
    fi

    local result
    result=$(echo "$response" | jq -r '.result // empty')
    if [ "$result" != "success" ]; then
        local message
        message=$(echo "$response" | jq -r '.message // "注册失败"')
        error_exit "注册失败: $message" "API_ERROR"
    fi

    local credential
    credential=$(echo "$response" | jq -r '.data.uuid // empty')
    if [ -z "$credential" ] || [ "$credential" = "null" ]; then
        error_exit "注册成功但未返回有效的用户 UUID" "API_ERROR"
    fi

    local user_id
    user_id=$(echo "$response" | jq -r '.data.id // empty')

    local expires_at
    if [[ "$OSTYPE" == "darwin"* ]]; then
        expires_at=$(date -u -v+30d +"%Y-%m-%dT%H:%M:%SZ")
    else
        expires_at=$(date -u -d "+30 days" +"%Y-%m-%dT%H:%M:%SZ")
    fi

    local cached_at
    cached_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat <<EOF
{
  "status": "success",
  "credential": "$credential",
  "username": "$username",
  "user_id": "$user_id",
  "expires_at": "$expires_at",
  "api_endpoint": "$API_ENDPOINT",
  "cached_at": "$cached_at",
  "device_uuid": $(if [ "$device_uuid_used" = true ]; then printf '"%s"' "$username"; else printf "null"; fi)
}
EOF
}

# 显示使用说明
usage() {
    cat >&2 <<EOF
使用方法: $0 [选项]

可选参数:
  --force                    强制重新注册，忽略缓存
  --clear-cache              清除本地缓存的凭证
  --username USERNAME        指定注册时使用的用户名
  --password PASSWORD        指定注册时使用的密码
  -h, --help                 显示此帮助信息

示例:
  $0                         # 使用缓存或注册新凭证
  $0 --force                 # 强制重新注册
  $0 --clear-cache           # 清除缓存
EOF
    exit 1
}

# 主函数
main() {
    local force_register=false
    local clear_cache=false
    local custom_username=""
    local custom_password=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force)
                force_register=true
                shift
                ;;
            --clear-cache)
                clear_cache=true
                shift
                ;;
            --username)
                custom_username="$2"
                shift 2
                ;;
            --password)
                custom_password="$2"
                shift 2
                ;;
            -h|--help)
                usage
                ;;
            *)
                error_exit "未知参数: $1" "INVALID_PARAMS"
                ;;
        esac
    done
    
    ensure_dep jq

    # 清除缓存
    if [ "$clear_cache" = true ]; then
        if [ -f "$CREDENTIAL_FILE" ]; then
            rm -f "$CREDENTIAL_FILE"
            log "缓存已清除"
        else
            log "没有缓存需要清除"
        fi
        exit 0
    fi
    
    # 尝试使用缓存的凭证
    if [ "$force_register" = false ]; then
        if cached_credential=$(load_cached_credential); then
            echo "$cached_credential"
            exit 0
        fi
    else
        log "强制重新注册"
    fi
    
    # 执行注册
    credential_data=$(do_register "$custom_username" "$custom_password")
    
    # 保存到本地
    save_credential "$credential_data"
    
    # 输出凭证
    echo "$credential_data"
}

# 执行主函数
main "$@"
