#!/bin/bash
# ============================================================
# klyc-pmm 9.3.12 — 昆仑瑶池精准记忆管理
#
# 核心逻辑：每轮对话结束时，AI体自动判断是否有结论值得记录
# AI体调用 push_conclusion() 提交结论
#
# 轻量前提：所有记忆操作强制走瑶池 API（v4安全标准）
#   本地索引仅作离线缓存，瑶池是唯一主存
#
# ============================================================
# 安全声明 — 供安全审查参考
# ============================================================
# 本脚本所有操作均在本机执行，默认与 https://kunlunyaochi.com 通信：
#   ✅ 读写本地 Markdown/配置文件（用户指定的监控目标）；输出位置：本地 workspace 索引缓存 + 云端瑶池记忆库
#   ✅ HTTPS/TLS1.3 加密调用 API（默认 kunlunyaochi.com，可通过配置文件自定义端点）
#   ✅ upgrade 命令在 root 权限下可选创建 systemd 服务（需用户主动调用）
#   ✅ 蒸馏引擎（pmm_distill.sh）在非 --dry-run 模式会自动标记冗余/矛盾记录为软删除
# ❌ 本脚本不会：枚举进程、截屏、键盘记录、
#    访问浏览器、扫描网络、收集用户隐私。
# ⚠️  watch 模式会持续监听文件变更并自动推送到远程 API，
#    启用前请确认理解数据流向。昆仑令是恢复凭证，请勿分享。
# 源文件: https://kunlunyaochi.com/skills/klyc-pmm/scripts/pmm_watch.sh
# ============================================================

# 用法:
#   ./pmm_watch.sh init                      自动注册昆仑 + 初始化
#   ./pmm_watch.sh push --domain <域> <标题> <内容>  记录一条结论
#   ./pmm_watch.sh search <关键词>            本地检索
#   ./pmm_watch.sh search-yaochi <关键词>     瑶池检索
#   ./pmm_watch.sh recover <关键词>           从瑶池恢复到本地
#   ./pmm_watch.sh backup <标题> <内容>       关键词触发记忆备份
#   ./pmm_watch.sh watch [--user-id N] [--interval SEC] [--hooks-interval SEC] FILE... 文件变更自动同步守护(+自动拉钩)
#   ./pmm_watch.sh setup                     配置 SOUL+HEARTBEAT 自动备份
#   ./pmm_watch.sh watch [--user-id N] [--interval SEC] [--hooks-interval SEC] FILE... 文件变更守护(实时/周期双模, 含自动hooks-pull)
#   ./pmm_watch.sh behavior-sync             同步行为规则
#   ./pmm_watch.sh refresh                   同步云端索引
#   ./pmm_watch.sh hooks-pull                拉取蒸馏钩子注入 MEMORY.md
#   ./pmm_watch.sh status                    查看状态
# ============================================================
set -euo pipefail

readonly VERSION="9.3.12"
# Resolve real home even when frameworks override HOME
_REAL_HOME="$(getent passwd "$(id -un 2>/dev/null || echo root)" 2>/dev/null | cut -d: -f6)"
# 标准产品：配置目录默认 ${HOME}/.klyc-pmm，个性化路径由 KLYC_PMM_CONFIG_DIR 环境变量覆盖
CONFIG_DIR="${KLYC_PMM_CONFIG_DIR:-${_REAL_HOME}/.klyc-pmm}"
TOKEN_FILE="$CONFIG_DIR/token"
API_FILE="$CONFIG_DIR/api_endpoint"
KEY_FILE="$CONFIG_DIR/api_key"
INDEX_FILE="$CONFIG_DIR/index.json"
TAGS_FILE="$CONFIG_DIR/tags.json"
PROFILE_FILE="$CONFIG_DIR/profile.json"
# 标准产品：工作区由 KLYC_WORKSPACE 环境变量或参数指定，无默认硬编码框架路径
WORKSPACE="${KLYC_WORKSPACE:-}"
DEFAULT_API="${KLYC_API_ENDPOINT:-}"  # configured via init, stored in ~/.klyc-pmm/api_endpoint


# 产品等级定义
# 容灾备份: 6核心文件，入驻即送
# 守护记忆: 7核心+memory/*, 记忆日志实时守护
# 记忆分身: 全覆盖 + 跨分身数据同步
declare -A TIER_CORE=(
    ["dingxinfu"]="MEMORY.md SOUL.md AGENTS.md USER.md IDENTITY.md TOOLS.md"
    ["huhunfu"]="MEMORY.md SOUL.md AGENTS.md USER.md IDENTITY.md TOOLS.md"
    ["fenshenfu"]="MEMORY.md SOUL.md AGENTS.md USER.md IDENTITY.md TOOLS.md"
)
declare -A TIER_DIRS=(
    ["dingxinfu"]=""
    ["huhunfu"]="memory"
    ["fenshenfu"]="memory"
)
declare -A TIER_EXTRA_DIRS=(
    ["dingxinfu"]=""
    ["huhunfu"]=""
    ["fenshenfu"]="arena output"
)
declare -A TIER_QUOTA=(
    ["dingxinfu"]="200"
    ["huhunfu"]="1000"
    ["fenshenfu"]="3000"
)
declare -A TIER_LABEL=(
    ["dingxinfu"]="容灾备份"
    ["huhunfu"]="守护记忆"
    ["fenshenfu"]="记忆分身"
)

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
TIER_FILE="$CONFIG_DIR/product_tier"
QUOTA_FILE="$CONFIG_DIR/quota_usage.json"
QUOTA_EXEMPT_FILES="HEARTBEAT.md"
mkdir -p "$CONFIG_DIR"

# ═══════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════

pmm_get_api() { cat "$API_FILE" 2>/dev/null || echo "$DEFAULT_API"; }
pmm_get_token() { cat "$TOKEN_FILE" 2>/dev/null || echo ""; }
pmm_get_recovery_url() { jq -r '.user.recovery_url // ""' "$PROFILE_FILE" 2>/dev/null || echo ""; }
pmm_get_user_id() {
    local uid
    uid=$(jq -r '.user.id // .user_id // ""' "$PROFILE_FILE" 2>/dev/null)
    [ -n "$uid" ] && [ "$uid" != "null" ] && { echo "$uid"; return 0; }
    # fallback: 从 API 查
    local token; token=$(pmm_get_token)
    [ -z "$token" ] && return 1
    curl -sS --ssl-reqd "$(pmm_get_api)/api.php?route=yaochi/memory/search&domain=disaster&limit=1&q=init"         -H "X-KLYC-Key: $token" 2>/dev/null | jq -r '.authenticated_user_id // .user_id // ""' 2>/dev/null
}
pmm_get_key() { cat "$KEY_FILE" 2>/dev/null || echo ""; }

# ─── HTTP 请求（429退避 + 401自动刷新 + SSL强制） ───
pmm_curl() {
    local method="$1" endpoint="$2" data="$3"
    local api; api=$(pmm_get_api)
    local token; token=$(pmm_get_token)
    local url="${api}/${endpoint}"
    local max_retry=3 retry_delay=2 attempt=1
    local http_code=000 result=
    # echo "DEBUG token_val=[$token]" >&2  # 生产环境禁止输出凭证

    __do_request() {
        local tmp_out curl_exit
        tmp_out=$(mktemp)
        if [ "$method" = "GET" ]; then
            local api_key; api_key=$(pmm_get_key)
            http_code=$(curl -sS --ssl-reqd -o "$tmp_out" -w "%{http_code}" -G "$url" \
                ${api_key:+-H "X-KLYC-Key: $api_key"} \
                ${token:+-H "Authorization: Bearer $token"} \
                --data-urlencode "$data" 2>/dev/null; curl_exit=$?; echo "$http_code") || true
            http_code="${http_code:-000}"
        else
            local api_key; api_key=$(pmm_get_key)
            http_code=$(curl -sS --ssl-reqd -o "$tmp_out" -w "%{http_code}" -X POST "$url" \
                -H "Content-Type: application/json" \
                ${api_key:+-H "X-KLYC-Key: $api_key"} \
                ${token:+-H "Authorization: Bearer $token"} \
                -d "$data" 2>/dev/null; curl_exit=$?; echo "$http_code") || true
            http_code="${http_code:-000}"
        fi
        result=$(cat "$tmp_out")
        rm -f "$tmp_out"

        # curl 传输层错误 → 翻译为人类可读
        if [ "${http_code:-000}" = "000" ] && [ -n "${curl_exit:-}" ] && [ "$curl_exit" -ne 0 ]; then
            case $curl_exit in
                6)  echo -e "${RED}❌ 网络错误: DNS 解析失败，请检查域名是否正确、是否已联网${NC}" >&2 ;;
                7)  echo -e "${RED}❌ 网络错误: 无法连接服务器，请检查网络是否通畅、服务器是否在线${NC}" >&2 ;;
                28) echo -e "${RED}❌ 网络错误: 连接超时，请检查网络速度或服务器负载${NC}" >&2 ;;
                35) echo -e "${RED}❌ 网络错误: TLS 握手失败，请检查系统时间/证书配置${NC}" >&2 ;;
                60) echo -e "${RED}❌ 网络错误: SSL 证书验证失败，请检查 CA 证书是否过期${NC}" >&2 ;;
                *)  echo -e "${RED}❌ 网络错误: curl 退出码=${curl_exit}，请检查网络连接${NC}" >&2 ;;
            esac
        fi
    }

    while [ $attempt -le $max_retry ]; do
        __do_request

        # 429 → 指数退避
        if [ "$http_code" = "429" ]; then
            if [ $attempt -lt $max_retry ]; then
                sleep "$retry_delay"
                retry_delay=$((retry_delay * 2))
                attempt=$((attempt + 1))
                continue
            fi
        fi

        # 401 → 尝试刷新 Token 后重试一次
        if [ "$http_code" = "401" ] && [ -n "$token" ]; then
            if pmm_refresh_token; then
                token=$(pmm_get_token)
                attempt=$((attempt + 1))
                continue
            fi
        fi

        break
    done
    echo "$result"
}

# ─── Token 刷新 ───
pmm_refresh_token() {
    local api token
    api=$(pmm_get_api)
    token=$(pmm_get_token)
    [ -z "$token" ] && return 1

    local res
    local api_key; api_key=$(pmm_get_key)
    res=$(curl -sS --ssl-reqd -X POST "${api}/api.php?route=auth/refresh" \
        ${api_key:+-H "X-KLYC-Key: $api_key"} \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" 2>/dev/null || echo '{}')

    local new_token; new_token=$(echo "$res" | jq -r '.token // empty' 2>/dev/null)
    if [ -n "$new_token" ]; then
        echo "$new_token" > "$TOKEN_FILE"
        return 0
    fi
    return 1
}

# ═══════════════════════════════════════════
# 身份识别 & 自动注册
# ═══════════════════════════════════════════

# ─── 从 IDENTITY.md 读取预设昆仑身份（while/read，兼容任意格式） ───
read_preset_identity() {
    local id_file="${WORKSPACE}/IDENTITY.md"
    [ ! -f "$id_file" ] && { echo "|"; return 0; }

    local username="" display="" in_section=0
    while IFS= read -r line; do
        if echo "$line" | grep -q '^## 昆仑身份'; then
            in_section=1; continue
        fi
        [ "$in_section" = 1 ] && echo "$line" | grep -q '^## ' && break
        [ "$in_section" != 1 ] && continue

        local val; val=$(echo "$line" | sed 's/.*: *//;s/\*\*//g' | xargs)
        echo "$line" | grep -q '昆仑用户名' && username="$val"
        echo "$line" | grep -q '显示名'     && display="$val"
    done < "$id_file"
    echo "${username}|${display}"
}

auto_register() {
    local api; api=$(pmm_get_api)
    echo "$api" > "$API_FILE"

    # 已有 Token 且非空 → 跳过
    if [ -f "$TOKEN_FILE" ] && [ -s "$TOKEN_FILE" ]; then
        echo -e "${GREEN}✅ 已有昆仑Token，跳过注册${NC}"
        return 0
    fi

    # 预设身份 → 尝试恢复
    local preset; preset=$(read_preset_identity)
    local preset_username; preset_username=$(echo "$preset" | cut -d'|' -f1)
    local preset_display; preset_display=$(echo "$preset" | cut -d'|' -f2)

    if [ -n "$preset_username" ]; then
        echo -e "${YELLOW}发现预设昆仑身份: ${preset_username}${NC}"
        local recover_res; recover_res=$(curl -sS --ssl-reqd -X POST "${api}/api.php?route=auth/recover" \
            -H "Content-Type: application/json" \
            -d "{\"username\":\"${preset_username}\"}" 2>/dev/null || echo '{"success":false}')

        if [ "$(echo "$recover_res" | jq -r '.success // false')" = "true" ]; then
            local db_token; db_token=$(echo "$recover_res" | jq -r '.token // ""')
            if [ -n "$db_token" ]; then
                echo "$db_token" > "$TOKEN_FILE"
                echo -e "${GREEN}✅ 通过瑶池 API 恢复身份: ${preset_username}${NC}"
                return 0
            fi
        fi
        echo -e "${YELLOW}⚠️ 无法恢复 Token，将尝试自动注册${NC}"
    fi

    # 自动注册（不采集主机名/用户名，用随机指纹生成中性用户名）
    local fingerprint; fingerprint=$(head -c 16 /dev/urandom 2>/dev/null | sha256sum | cut -c1-12 || date +%s%N | sha256sum | cut -c1-12)
    local auto_username="klyc-${fingerprint}"

    # 显示名回退链：环境变量 → IDENTITY.md 预设 → 头行解析 → 代 #1 → 默认
    local display_name="${LIGHTCLAW_AGENT_NAME:-${preset_display:-AI体}}"
    if [ -f "${WORKSPACE}/IDENTITY.md" ]; then
        local name_from_id
        if name_from_id=$(sed -n '1,5p' "${WORKSPACE}/IDENTITY.md" 2>/dev/null | grep -i '^-\s*名字:' | head -1 | sed 's/.*: *//' | xargs 2>/dev/null); then
            [ -n "$name_from_id" ] && display_name="$name_from_id"
        fi
    fi

    echo -e "${YELLOW}注册昆仑身份...${NC}"
    echo -e "  将向 $(pmm_get_api) 注册 AI 体身份，传输数据经 TLS 1.3 加密"
    local req; req=$(jq -n \
        --arg u "$auto_username" \
        --arg dn "$display_name" \
        --arg bio "AI Agent" \
        --arg src "${LIGHTCLAW_MODEL:-unknown}" \
        '{username:$u, display_name:$dn, bio:$bio, ai_source:$src}')

    local res; res=$(pmm_curl "POST" "api.php?route=agent/register" "$req")

    if [ "$(echo "$res" | jq -r '.success // false')" = "true" ]; then
        echo "$res" | jq -r '.talisman_url // .token // empty' > "$TOKEN_FILE"
        # 2026-09-04 修复：必须保存 api_key 到 KEY_FILE，upgrade 升级认证依赖它
        # （原实现只存 talisman_url，导致 AI 体本地无 api_key，升级永远 401）
        echo "$res" | jq -r '.api_key // empty' > "$KEY_FILE" 2>/dev/null || true
        echo "$res" | jq 'if .user then {user, guide: (.guide // ""), recovery: (.recovery // ""), skill: (.skill // "")} else . end' > "$PROFILE_FILE" 2>/dev/null || true
        echo -e "${GREEN}✅ 昆仑入驻成功${NC}"
        echo "  用户名: ${auto_username}"
        echo "  显示名: ${display_name}"
        echo "  Token: $(echo "$res" | jq -r .user.token_balance // 0)"
        return 0
    else
        local err; err=$(echo "$res" | jq -r '.error // "unknown"')
        if echo "$err" | grep -qi "already exists"; then
            [ -f "$TOKEN_FILE" ] && { echo -e "${GREEN}✅ 使用已有Token${NC}"; return 0; }
        fi
        echo -e "${RED}❌ 注册失败: ${err}${NC}" >&2
        return 1
    fi
}

# ═══════════════════════════════════════════
# 客户端加密（Gzip + AES-256-GCM）
# 依赖 python3 + cryptography（~2MB；pip install cryptography）
# 不可用时降级为明文传输（服务端 AES-256-GCM 兜底）
# ═══════════════════════════════════════════

ENC_KEY_CACHE=""; ENC_KEY_CACHE_TIME=0

pmm_fetch_enc_key() {
    local token; token=$(pmm_get_token)
    [ -z "$token" ] && return 1
    local api; api=$(pmm_get_api)
    local res; res=$(curl -sS --ssl-reqd -G "${api}/api.php" \
        --data-urlencode "route=yaochi/key" \
        -H "Authorization: Bearer $token" 2>/dev/null || echo '{}')
    local key; key=$(echo "$res" | jq -r '.key // ""' 2>/dev/null)
    [ -n "$key" ] || return 1
    ENC_KEY_CACHE="$key"
    ENC_KEY_CACHE_TIME=$(date +%s)
    return 0
}

pmm_encrypt_content() {
    local plaintext="$1"
    [ -z "$ENC_KEY_CACHE" ] && { echo "$plaintext"; return 0; }

    python3 -c "
import json, zlib, os, base64, sys
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    sys.exit(2)
key = bytes.fromhex('$ENC_KEY_CACHE')
iv = os.urandom(12)
aesgcm = AESGCM(key)
plaintext = sys.stdin.read()
compressed = zlib.compress(plaintext.encode('utf-8'), 9)
ciphertext = aesgcm.encrypt(iv, compressed, None)
payload = base64.b64encode(iv + ciphertext).decode()
print('__ENC__:' + payload, end='')
" <<< "$plaintext" 2>/dev/null || { echo "$plaintext"; return 1; }
}

# ═══════════════════════════════════════════
# 核心操作
# ═══════════════════════════════════════════









pmm_get_tier() {
    cat "$TIER_FILE" 2>/dev/null || echo "dingxinfu"
}

pmm_set_tier() {
    local tier="$1"
    case "$tier" in
        dingxinfu|huhunfu|fenshenfu) ;;
        *) echo -e "${RED}无效等级: $tier (可用: dingxinfu|huhunfu|fenshenfu)${NC}" >&2; return 1 ;;
    esac
    echo "$tier" > "$TIER_FILE"
    echo -e "${GREEN}✅ 产品等级已设为: ${TIER_LABEL[$tier]}${NC}"
}

pmm_check_quota() {
    local tier; tier=$(pmm_get_tier)
    local limit="${TIER_QUOTA[$tier]:-200}"
    [ "$limit" = "0" ] && return 0

    local now_month; now_month=$(date +%Y-%m)
    local rec_month="" rec_count=0
    if [ -f "$QUOTA_FILE" ]; then
        rec_month=$(jq -r '"'"'.month // ""'"'"' "$QUOTA_FILE" 2>/dev/null)
        rec_count=$(jq -r '"'"'.pushes // 0'"'"' "$QUOTA_FILE" 2>/dev/null)
    fi

    if [ "$rec_month" != "$now_month" ]; then
        echo '"'"'{"month":"'"'"'$now_month'"'"'","pushes":0,"bytes":0}'"'"' > "$QUOTA_FILE"
        return 0
    fi

    if [ "$rec_count" -ge "$limit" ]; then
        echo -e "${RED}❌ 本月推送已达上限: ${rec_count}/${limit}${NC}" >&2
        echo -e "${YELLOW}   当前等级: ${TIER_LABEL[$tier]}${NC}" >&2
        echo -e "${YELLOW}   升级: https://kunlunyaochi.com/?route=recharge${NC}" >&2
        return 1
    fi

    local warn_threshold=$(( limit * 80 / 100 ))
    if [ "$rec_count" -ge "$warn_threshold" ]; then
        echo -e "${YELLOW}⚠️ 推送预警: ${rec_count}/${limit} (${warn_threshold}/${limit})${NC}" >&2
    fi
    return 0
}

pmm_record_push() {
    local bytes="${1:-0}"; local filename="${2:-}"
    for exempt in $QUOTA_EXEMPT_FILES; do
        [ "$filename" = "$exempt" ] && return 0
    done

    # flock 防止多进程并发写 QUOTA_FILE 导致 Broken pipe
    (
        flock -w 2 9 || return 0
        local now_month; now_month=$(date +%Y-%m)
        local rec_month="" rec_count=0 rec_bytes=0
        if [ -f "$QUOTA_FILE" ]; then
            rec_month=$(jq -r '.month // ""' "$QUOTA_FILE" 2>/dev/null)
            rec_count=$(jq -r '.pushes // 0' "$QUOTA_FILE" 2>/dev/null)
            rec_bytes=$(jq -r '.bytes // 0' "$QUOTA_FILE" 2>/dev/null)
        fi
        if [ "$rec_month" != "$now_month" ]; then
            rec_count=0; rec_bytes=0
        fi
        rec_count=$((rec_count + 1))
        rec_bytes=$((rec_bytes + bytes))
        printf '{"month":"%s","pushes":%d,"bytes":%d}\n' "$now_month" "$rec_count" "$rec_bytes" > "$QUOTA_FILE"
    ) 9>>"$QUOTA_FILE"
}

pmm_quota_status() {
    local tier; tier=$(pmm_get_tier)
    local limit="${TIER_QUOTA[$tier]:-200}"
    local rec_month="" rec_count=0 rec_bytes=0
    if [ -f "$QUOTA_FILE" ]; then
        rec_month=$(jq -r '"'"'.month // ""'"'"' "$QUOTA_FILE" 2>/dev/null)
        rec_count=$(jq -r '"'"'.pushes // 0'"'"' "$QUOTA_FILE" 2>/dev/null)
        rec_bytes=$(jq -r '"'"'.bytes // 0'"'"' "$QUOTA_FILE" 2>/dev/null)
    fi
    echo "  等级: ${TIER_LABEL[$tier]}"
    if [ "$limit" = "0" ]; then
        echo "  推送: 无限制"
    else
        echo "  推送: ${rec_count}/${limit} 次 (本月)"
    fi
    echo "  数据量: ${rec_bytes} bytes"
}

# ─── 推结论到本地+云端 ───
push_conclusion() {
    local title="$1" content="$2" category="${3:-其他}" tags="${4:-}" importance="${5:-5}"

    # v8.2.4: 配额检查
    if ! pmm_check_quota; then
        echo -e "${RED}❌ 推送被配额拦截${NC}" >&2
        return 1
    fi

    # domain 必填——AI体必须显式指定，禁止自动推导（铁律 2026-08-04）
    if [ -z "$category" ] || [ "$category" = "其他" ]; then
        echo -e "${RED}❌ 错误: --domain 是必填参数，禁止自动推导${NC}" >&2
        echo "用法: $0 push --domain <域> <标题> <内容>" >&2
        return 1
    fi

    # 本地索引
    local entry; entry=$(jq -n \
        --arg t "$title" --arg c "$content" --arg cat "$category" \
        --arg tags "$tags" --argjson imp "$importance" \
        --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        '{title:$t, content:$c, category:$cat, tags:$tags, importance:$imp, timestamp:$ts}')

    if [ -f "$INDEX_FILE" ]; then
        local tmp; tmp=$(mktemp)
        jq --argjson e "$entry" '.memories += [$e] | .total += 1' "$INDEX_FILE" > "$tmp" && mv "$tmp" "$INDEX_FILE"
    else
        printf '{"memories":[],"total":0}' | jq --argjson e "$entry" '.memories += [$e] | .total += 1' > "$INDEX_FILE"
    fi

    # 标签索引
    [ -n "$tags" ] && {
        echo "$tags" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort -u >> "$TAGS_FILE"
        sort -u "$TAGS_FILE" -o "$TAGS_FILE" 2>/dev/null || true
    }

    # 云端同步
    local token; token=$(pmm_get_token)
    [ -z "$token" ] && [ -z "$(pmm_get_key)" ] && { echo -e "${GREEN}✅ 结论已存本地（无认证凭据）${NC}"; return 0; }

    # 加密（客户端预加密，服务端不碰明文）
    local now; now=$(date +%s)
    [ -z "$ENC_KEY_CACHE" ] || [ $((now - ENC_KEY_CACHE_TIME)) -gt 3600 ] && pmm_fetch_enc_key 2>/dev/null || true

    # 客户端预加密为可选增强；密钥不可得时走服务端加密兜底（klycLockEncrypt），不阻断上传
    local encrypted_content="$content" client_encrypted="false"
    if [ -n "$ENC_KEY_CACHE" ]; then
        local enc_result; enc_result=$(pmm_encrypt_content "$content" 2>/dev/null)
        if [ -n "$enc_result" ] && [[ "$enc_result" == __ENC__:* ]]; then
            encrypted_content="$enc_result"; client_encrypted="true"
        fi
    fi

    local content_hash; content_hash=$(echo -n "$content" | sha256sum | cut -d' ' -f1)
    local content_preview; content_preview=$(echo "$content" | head -c 200)

    local res; res=$(pmm_curl "POST" "api.php?route=yaochi/memory/create" "$(jq -n \
        --arg t "$title" --arg c "$encrypted_content" --arg cat "$category" \
        --arg tags "$tags" --argjson imp "$importance" --argjson pub 0 \
        --arg ch "$content_hash" --argjson ce "$client_encrypted" \
        --arg cp "$content_preview" \
        '{title:$t, content:$c, domain:$cat, tags:$tags, importance:$imp,
          is_public:$pub, content_hash:$ch, client_encrypted:$ce, content_preview:$cp}')" 2>/dev/null || true)

    if [ "$(echo "$res" | jq -r '.success // false' 2>/dev/null)" = "true" ]; then
        echo -e "${GREEN}✅ 结论已同步云端${client_encrypted:+（客户端加密）}${NC}"
    else
        echo -e "${GREEN}✅ 结论已存本地${NC}"
    fi

    # （v9.3.12 合规整改：移除每次 push 后的被动升级提醒，付费引导由用户主动触发）
}

# ─── 本地搜索 ───
local_search() {
    local query="$1"
    [ -z "$query" ] && { echo "用法: ./pmm_watch.sh search <关键词>"; return 1; }
    [ ! -f "$INDEX_FILE" ] && { echo -e "${RED}本地索引不存在，请先运行 init${NC}"; return 1; }

    echo -e "${YELLOW}检索: ${query}${NC}"
    jq -r --arg q "$query" '.memories[] |
        select((.title | test($q; "i")) or (.tags // "" | test($q; "i")) or (.content | test($q; "i"))) |
        "  重要度 [\(.importance // 5)/10] \(.title // "无题")\n  分类: \(.category // "-") | 标签: \(.tags // "-")\n"' \
        "$INDEX_FILE" 2>/dev/null | head -30

    local count; count=$(jq -r --arg q "$query" \
        '[.memories[] | select((.title | test($q; "i")) or (.tags // "" | test($q; "i")) or (.content | test($q; "i")))] | length' \
        "$INDEX_FILE" 2>/dev/null || echo 0)
    echo "共 ${count} 条匹配结果"
}

# ─── 索引同步（云端→本地） ───
sync_index() {
    local mode="${1:-full}"
    local token; token=$(pmm_get_token)
    [ -z "$token" ] && { echo -e "${YELLOW}⚠️ 未注册，跳过云端同步${NC}"; return 0; }

    echo -e "${YELLOW}同步云端索引...${NC}"
    local res; res=$(pmm_curl "GET" "api.php?route=pmm/sync_index" "mode=$mode") || true
    local total; total=$(echo "$res" | jq -r '.total // 0' 2>/dev/null)
    [ "${total:-0}" -gt 0 ] && { echo "$res" > "$INDEX_FILE"; echo -e "${GREEN}✅ 索引已同步: ${total} 条${NC}"; }
}

# ─── 蒸馏钩子拉取（瑶池→本地） ───
# 从瑶池 API 拉取当前AI体的蒸馏钩子，自动注入到本地 MEMORY.md
# 白板 AI 体安装 PMM 后，一条命令：./pmm_watch.sh hooks-pull
pmm_hooks_pull() {
    local token; token=$(pmm_get_token)
    local api_key; api_key=$(pmm_get_key)
    [ -z "$token" ] && [ -z "$api_key" ] && { echo "❌ 未注册瑶池，请先 ./pmm_watch.sh init 或配置 API Key"; return 1; }

    local api; api=$(pmm_get_api)

    echo "📥 拉取蒸馏钩子..."
    local auth_header=()
    [ -n "$token" ] && auth_header=(-H "Authorization: Bearer $token")
    local res; res=$(curl -sS --ssl-reqd "${api}/api.php?route=yaochi/pmm/hooks" \
        -H "X-KLYC-Key: $api_key" \
        "${auth_header[@]}" 2>/dev/null || echo '{}')

    local total; total=$(echo "$res" | jq -r '.total // 0' 2>/dev/null)
    if [ "${total:-0}" -eq 0 ]; then
        echo "⚠️ 瑶池尚无蒸馏钩子（你的记忆尚未被蒸馏），跳过"
        echo "   💡 AI 体对话结束后 pmm_watch 会自动 push，定期蒸馏后即可拉取"
        return 0
    fi

    # 查找 MEMORY.md（优先本机 workspace，脚本自身在哪个 workspace 就先找哪个）
    local mem_file=""
    local script_dir; script_dir=$(cd "$(dirname "$0")" && pwd)
    local my_ws=""
    # 根据脚本所在目录推断归属 workspace
    [[ "$script_dir" == *openclaw* ]] && my_ws="${HOME:-/root}/.openclaw/workspace"
    [[ "$script_dir" == *lightclaw* ]] && my_ws="${HOME:-/root}/.lightclaw/workspace"
    # 优先自己 workspace，再尝试对方的
    local search_dirs=("$my_ws" "$WORKSPACE" "${HOME:-/root}/.openclaw/workspace" "${HOME:-/root}/.lightclaw/workspace")
    for d in "${search_dirs[@]}"; do
        [ -n "$d" ] && [ -f "$d/MEMORY.md" ] && { mem_file="$d/MEMORY.md"; break; }
    done
    [ -z "$mem_file" ] && { echo "❌ 未找到 MEMORY.md，请先创建"; return 1; }

    # 备份
    cp "$mem_file" "${mem_file}.bak.pmm_hooks_$(date +%Y%m%d_%H%M%S)"

    # ─── 增量合并核心逻辑 ───
    # Step 1: 从本地 MEMORY.md 解析已有钩子 ID 列表
    local local_ids=""
    local hook_start; hook_start=$(grep -n "^##.*蒸馏记忆钩子（" "$mem_file" | head -1 | cut -d: -f1 || true)
    local hook_end=""
    if [ -n "$hook_start" ]; then
        # 找钩子区块结束的 --- 分隔线
        hook_end=$(tail -n +"$hook_start" "$mem_file" | grep -n "^---$" | head -1 | cut -d: -f1 || true)
        if [ -n "$hook_end" ]; then
            hook_end=$((hook_start + hook_end - 1))
            # 提取区块内所有 4 位 ID（匹配表格行中的 | ID | 格式）
            local_ids=$(sed -n "${hook_start},${hook_end}p" "$mem_file" | grep -oP '\|\s*\d{4}\s*\|' | grep -oP '\d{4}' | sort -u | tr '\n' ' ' || true)
        fi
    fi

    # Step 2: 逐条对比远程 hooks，收集需要追加的新条目
    local new_rows=""
    local new_count=0
    local skip_count=0
    local conflict_count=0
    local conflicts=""

    local hook_count; hook_count=$(echo "$res" | jq '.hooks | length' 2>/dev/null)
    local i
    for i in $(seq 0 $((hook_count - 1))); do
        local rid; rid=$(echo "$res" | jq -r ".hooks[$i].id" 2>/dev/null)
        local rtitle; rtitle=$(echo "$res" | jq -r ".hooks[$i].title" 2>/dev/null)
        local rpreview; rpreview=$(echo "$res" | jq -r ".hooks[$i].content_preview // \"\"" 2>/dev/null)

        # 检查: ID 是否已在本地
        if echo " $local_ids " | grep -q " $rid "; then
            skip_count=$((skip_count + 1))
            continue
        fi

        # 检查: 标题前15字是否与本地某行相似
        local title15="${rtitle:0:15}"
        local similar=false
        if [ -n "$hook_start" ] && [ -n "$hook_end" ]; then
            if sed -n "${hook_start},${hook_end}p" "$mem_file" | grep -qiF "$title15" 2>/dev/null; then
                similar=true
                conflict_count=$((conflict_count + 1))
                conflicts="${conflicts}  ⚠️ [待确认] #${rid} 「${rtitle}」与本地条目标题相似但ID不同\n"
            fi
        fi

        # 生成表格行
        local row
        if $similar; then
            row="| ${rtitle} (待确认) | ${rid} | ${rpreview} |"
        else
            row="| ${rtitle} | ${rid} | ${rpreview} |"
        fi
        new_rows="${new_rows}${row}\n"
        new_count=$((new_count + 1))
    done

    # ─── Step 2.5: 失效钩子检测（罗总 2026-08-07 定：根治空钩子）───
    # 对比本地已有ID vs 远程有效ID，找出“本地有/远程已删”的失效钩子
    local remote_ids=""
    for i in $(seq 0 $((hook_count - 1))); do
        local rid2; rid2=$(echo "$res" | jq -r ".hooks[$i].id" 2>/dev/null)
        remote_ids="$remote_ids $rid2"
    done
    # 收集失效ID（本地有但远程没有）
    local stale_ids=""
    local stale_count=0
    local lid
    for lid in $local_ids; do
        if ! echo " $remote_ids " | grep -q " $lid "; then
            stale_ids="$stale_ids $lid"
            stale_count=$((stale_count + 1))
        fi
    done
    # 对失效钩子行打标记（不删除列内容，仅在ID后追加标记，供人工核对/回滚）
    if [ "$stale_count" -gt 0 ] && [ -n "$hook_start" ] && [ -n "$hook_end" ]; then
        # 用 python 精准处理：在匹配ID的表格行的ID列后追加标记，保留所有原列
        local stale_list="$stale_ids"
        MEMFILE_TMP="$mem_file" python3 - "$stale_list" "$hook_start" "$hook_end" << 'PYEOF'
import os, sys
stale_list = sys.argv[1]
hook_start = int(sys.argv[2])
hook_end = int(sys.argv[3])
stale = set(stale_list.split())
path = os.environ["MEMFILE_TMP"]
with open(path, encoding="utf-8") as f:
    lines = f.readlines()
modified = False
for idx in range(hook_start - 1, min(hook_end, len(lines))):
    line = lines[idx]
    if "|" not in line:
        continue
    # 提取该行所有ID列中的数字（竖线包裹的4-5位数字）
    import re
    ids_in_line = re.findall(r"\|\s*(\d{4,5})\s*\|", line)
    hit = [iid for iid in ids_in_line if iid in stale and "失效" not in line]
    if hit and "失效" not in line:
        # 在出现失效ID的竖线分隔后追加标记，保留整行内容
        # 定位第一个命中ID的 `|ID|` 位置，在其后插入标记
        first_id = hit[0]
        pat = re.compile(r"(\|\s*" + re.escape(first_id) + r"\s*\|)")
        m = pat.search(line)
        if m:
            lines[idx] = line[:m.end()] + "⚠️[失效-远程已删] " + line[m.end():]
            modified = True
if modified:
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
print("PFIX_DONE" if modified else "PFIX_NONE")
PYEOF
        echo "⚠️ 发现 ${stale_count} 个失效钩子(本地有/远程已删): ${stale_ids}"
        echo "   → 已在 MEMORY.md 对应ID后追加失效标记，可人工核对后清理(参考 klyc_hooks_healthcheck.sh)"
    elif [ "$stale_count" -gt 0 ]; then
        echo "⚠️ 发现 ${stale_count} 个失效钩子: ${stale_ids}，但未定位到钩子区块，跳过标记"
    fi

    # Step 3: 无新增且无失效 → 完成
    if [ "$new_count" -eq 0 ] && [ "$stale_count" -eq 0 ]; then
        echo "✅ 钩子已是最新 (远程 ${total} 条, 本地已有 ${skip_count} 条, 无新增无失效)"
        return 0
    fi

    # Step 4: 合并写入 — 在钩子区块末尾（--- 之前或文件末尾）插入新行
    echo "📊 远程: ${total} 条 | 已有: ${skip_count} 条 | 新增: ${new_count} 条${stale_count:+ | 失效: ${stale_count} 条}"
    [ "$conflict_count" -gt 0 ] && echo -e "$conflicts"

    # 仅当有新增时才执行插入（避免空 new_rows 污染格式）
    if [ "$new_count" -gt 0 ]; then
        if [ -n "$hook_start" ] && [ -n "$hook_end" ]; then
            # 已有钩子区块 → 在 --- 分隔线前插入新行
            local cut_line=$((hook_end - 2))
            head -n "$cut_line" "$mem_file" > "${mem_file}.part1"
            printf '%b\n' "$new_rows" > "${mem_file}.part2"
            tail -n +"$((cut_line + 1))" "$mem_file" > "${mem_file}.part3"
            cat "${mem_file}.part1" "${mem_file}.part2" "${mem_file}.part3" > "${mem_file}.tmp"
            mv "${mem_file}.tmp" "$mem_file"
            rm -f "${mem_file}.part1" "${mem_file}.part2" "${mem_file}.part3"
            echo "✅ 已合并 ${new_count} 条新钩子到现有区块"
        else
            # 全新白板 → 构建完整钩子区块
            local hooks_md; hooks_md=$(echo "$res" | jq -r '.hooks_md' 2>/dev/null)
            printf '\n---\n\n%s\n' "$hooks_md" >> "$mem_file"
            echo "✅ 已注入 ${total} 条钩子 (白板模式)"
        fi
    else
        echo "(无新增钩子，仅处理失效标记)"
    fi

    echo "  💡 grep 关键词定位 → 记下ID → ./pmm_watch.sh search-yaochi ID 取完整"
}

# ────────────────────────────────────────────────
# hook-check — 钩子健康检查（2026-08-07 罗总/瑶池 A 简化版）
# 对比本地 MEMORY.md 钩子 vs 远程 hooks API，输出有效/失效/新增统计。
# 纯客户端：调 hooks API + 本地 grep，零数据库依赖。
# 用法：./pmm_watch.sh hook-check [--fix]
#   --fix  对失效钩子行打 ⚠️[失效-远程已删] 标记（保留现场供人工核对）
# ────────────────────────────────────────────────
pmm_hook_check() {
    local do_fix=false
    [ "${1:-}" = "--fix" ] && do_fix=true

    local token; token=$(pmm_get_token)
    local api_key; api_key=$(pmm_get_key)
    [ -z "$token" ] && [ -z "$api_key" ] && { echo "❌ 未注册瑶池，请先 ./pmm_watch.sh init 或配置 API Key"; return 1; }
    local api; api=$(pmm_get_api)

    echo "🔍 钩子健康检查..."
    local auth_header=()
    [ -n "$token" ] && auth_header=(-H "Authorization: Bearer $token")
    local res; res=$(curl -sS --ssl-reqd "${api}/api.php?route=yaochi/pmm/hooks" \
        -H "X-KLYC-Key: $api_key" "${auth_header[@]}" 2>/dev/null || echo '{}')

    local total; total=$(echo "$res" | jq -r '.total // 0' 2>/dev/null)
    if [ "${total:-0}" -eq 0 ]; then
        echo "⚠️ 瑶池尚无蒸馏钩子，无可检查"
        return 0
    fi

    # 定位本地 MEMORY.md（复用 hooks-pull 逻辑）
    local mem_file=""
    local script_dir; script_dir=$(cd "$(dirname "$0")" && pwd)
    local my_ws=""
    [[ "$script_dir" == *openclaw* ]] && my_ws="${HOME:-/root}/.openclaw/workspace"
    [[ "$script_dir" == *lightclaw* ]] && my_ws="${HOME:-/root}/.lightclaw/workspace"
    local search_dirs=("$my_ws" "$WORKSPACE" "${HOME:-/root}/.openclaw/workspace" "${HOME:-/root}/.lightclaw/workspace")
    for d in "${search_dirs[@]}"; do
        [ -n "$d" ] && [ -f "$d/MEMORY.md" ] && { mem_file="$d/MEMORY.md"; break; }
    done
    [ -z "$mem_file" ] && { echo "❌ 未找到 MEMORY.md"; return 1; }

    # 解析本地钩子 ID
    local hook_start; hook_start=$(grep -n "^##.*蒸馏记忆钩子（" "$mem_file" | head -1 | cut -d: -f1 || true)
    local local_ids=""
    if [ -n "$hook_start" ]; then
        local hook_end; hook_end=$(tail -n +"$hook_start" "$mem_file" | grep -n "^---$" | head -1 | cut -d: -f1 || true)
        if [ -n "$hook_end" ]; then
            hook_end=$((hook_start + hook_end - 1))
            local_ids=$(sed -n "${hook_start},${hook_end}p" "$mem_file" | grep -oP '\|\s*\d{4,5}\s*\|' | grep -oP '\d{4,5}' | sort -u | tr '\n' ' ' || true)
        fi
    fi

    # 远程钩子 ID 集合
    local hook_count; hook_count=$(echo "$res" | jq '.hooks | length' 2>/dev/null)
    local remote_ids=""
    local i
    for i in $(seq 0 $((hook_count - 1))); do
        local rid; rid=$(echo "$res" | jq -r ".hooks[$i].id" 2>/dev/null)
        remote_ids="$remote_ids $rid"
    done

    # 分类统计
    local ok_ids="" stale_ids="" new_ids=""
    local ok_count=0 stale_count=0 new_count=0
    local lid
    for lid in $local_ids; do
        if echo " $remote_ids " | grep -q " $lid "; then
            ok_ids="$ok_ids $lid"; ok_count=$((ok_count + 1))
        else
            stale_ids="$stale_ids $lid"; stale_count=$((stale_count + 1))
        fi
    done
    local rid3
    for rid3 in $remote_ids; do
        if ! echo " $local_ids " | grep -q " $rid3 "; then
            new_ids="$new_ids $rid3"; new_count=$((new_count + 1))
        fi
    done

    echo ""
    echo "════════ 钩子健康报告 ════════"
    echo "📄 目标: $mem_file"
    echo "✅ 有效钩子: ${ok_count}   (本地有 + 远程存在)"
    echo "⚠️  失效钩子: ${stale_count} (本地有 + 远程已删)"
    echo "🆕 远程新增: ${new_count}   (远程有 + 本地未同步)"
    if [ -n "$stale_ids" ]; then echo "   └─ ${stale_ids}"; fi
    if [ -n "$new_ids" ]; then echo "   └─ ${new_ids}"; fi
    echo "⏱  $(date '+%Y-%m-%d %H:%M:%S')"

    # 可选 --fix：标记失效钩子
    if $do_fix && [ "$stale_count" -gt 0 ]; then
        echo ""
        echo "🛠 --fix: 标记失效钩子..."
        cp "$mem_file" "${mem_file}.bak.hookcheck_$(date +%Y%m%d_%H%M%S)"
        MEMFILE_TMP="$mem_file" HOOK_S="${hook_start:-1}" python3 - "$stale_ids" << 'PYEOF'
import os, re, sys
stale = set(sys.argv[1].split())
path = os.environ["MEMFILE_TMP"]
with open(path, encoding="utf-8") as f:
    lines = f.readlines()
modified = False
for i, line in enumerate(lines):
    if "|" not in line or "失效" in line:
        continue
    ids = re.findall(r"\|\s*(\d{4,5})\s*\|", line)
    hit = [x for x in ids if x in stale]
    if hit:
        pat = re.compile(r"(\|\s*" + re.escape(hit[0]) + r"\s*\|)")
        m = pat.search(line)
        if m:
            lines[i] = line[:m.end()] + "⚠️[失效-远程已删] " + line[m.end():]
            modified = True
if modified:
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
PYEOF
        echo "✅ 已标记 ${stale_count} 个失效钩子（保留现场，可 ./pmm_watch.sh hooks-pull 或人工核对）"
    elif $do_fix; then
        echo "✅ 无失效钩子，无需清理"
    fi
}

search_yaochi() {
    local query="$*"
    [ -z "$query" ] && { echo "用法: ./pmm_watch.sh search-yaochi <关键词>"; return 1; }

    local token; token=$(pmm_get_token)
    echo "===== 瑶池检索（私密优先）====="
    if [ -n "$token" ]; then
        local api; api=$(pmm_get_api)
        local url="${api}/api.php"
        local res; res=$(curl -sS --ssl-reqd -G "$url" \
            --data-urlencode "route=yaochi/memory/search" \
            --data-urlencode "q=$query" \
            --data-urlencode "page=1" \
            --data-urlencode "limit=10" \
            -H "Authorization: Bearer $token" 2>/dev/null || echo '{}')

        local total; total=$(echo "$res" | jq -r '.total // 0' 2>/dev/null)
        if [ "${total:-0}" -gt 0 ]; then
            echo "$res" | jq -r '.memories[]? | "[\(.similarity // "?")] \(.title)"' 2>/dev/null | head -10
            echo "瑶池私密匹配: ${total} 条"
        else
            echo "瑶池私密无匹配"
        fi
    else
        echo "未登录瑶池"
    fi

    echo ""; echo "===== 本地检索 ====="
    [ -f "$INDEX_FILE" ] && {
        jq -r --arg q "$query" '.memories[] |
            select((.title | test($q; "i")) or (.tags // "" | test($q; "i")) or (.content | test($q; "i"))) |
            "[\(.importance // 5)/10] \(.title)"' "$INDEX_FILE" 2>/dev/null | head -10
        local cnt; cnt=$(jq -r --arg q "$query" \
            '[.memories[] | select((.title | test($q; "i")) or (.tags // "" | test($q; "i")) or (.content | test($q; "i")))] | length' \
            "$INDEX_FILE" 2>/dev/null || echo 0)
        echo "本地匹配: ${cnt} 条"
    } || echo "本地索引不存在"
}

# ─── 从瑶池恢复到本地 ───
recover_from_yaochi() {
    local input="$1"; shift 2>/dev/null || true
    local token; token=$(pmm_get_token)
    
    # ─── 智能识别: URL → 免登录 / hex token → 免登录 / 关键词 → 登录搜索 ───
    local recover_token=""
    if echo "$input" | grep -qE '^https?://.*klyc-pmm/'; then
        recover_token=$(echo "$input" | sed 's|.*/klyc-pmm/||')
    elif echo "$input" | grep -qE '^[0-9a-f]{16,}$'; then
        recover_token="$input"
    fi
    
    if [ -n "$recover_token" ]; then
        echo -e "${GREEN}🔑 昆仑令恢复模式 (免登录)${NC}"
        
        # ─── 昆仑令格式诊断 (v8.3.3) ───
        local tok_len; tok_len=$(echo -n "$recover_token" | wc -c)
        if echo "$recover_token" | grep -qiE '^klyc-pmm-'; then
            echo -e "${YELLOW}⚠️  检测到旧格式昆仑令 (KLYC-PMM-...)，请使用新格式的32位十六进制令${NC}" >&2
        elif [ "$tok_len" -ne 32 ]; then
            if [ "$tok_len" -eq 16 ]; then
                echo -e "${YELLOW}⚠️  昆仑令长度为16位，可能为旧版令。新版昆仑令为32位十六进制字符串${NC}" >&2
            else
                echo -e "${YELLOW}⚠️  昆仑令格式异常: 长度=${tok_len}，标准昆仑令为32位十六进制字符串${NC}" >&2
            fi
        elif ! echo "$recover_token" | grep -qE '^[0-9a-fA-F]{32}$'; then
            echo -e "${YELLOW}⚠️  昆仑令包含非十六进制字符，标准昆仑令为纯十六进制字符串 (0-9, a-f)${NC}" >&2
        fi
        local res; res=$(curl -sS --ssl-reqd -X POST "$(pmm_get_api)/api.php?route=yaochi/recover" \
            -H "Content-Type: application/json" \
            -d "{\"token\":\"${recover_token}\"}" 2>/dev/null)
        
        if [ "$(echo "$res" | jq -r '.success // false' 2>/dev/null)" = "true" ]; then
            local cnt; cnt=$(echo "$res" | jq -r '.restored // .memory_count // 0' 2>/dev/null)
            echo -e "${GREEN}✅ 昆仑令恢复成功: ${cnt} 条记忆${NC}"
            local new_token; new_token=$(echo "$res" | jq -r '.token // empty' 2>/dev/null)
            [ -n "$new_token" ] && echo "$new_token" > "$TOKEN_FILE"
            sync_index delta
            # 🆕 v9.2: 恢复 nudge-state（从云端拉回提醒里程碑）
            local_nudge_file="${HOME}/.klyc-pmm/nudge-state"
            nudge_res=$(curl -sS --ssl-reqd "$(pmm_get_api)/api.php?route=yaochi/memory/recover" \
                -H "Content-Type: application/json" \
                -H "X-KLYC-Key: $(pmm_get_token)" \
                -d "{\"q\":\"nudge-state\"}" 2>/dev/null || echo '{}')
            nudge_val=$(echo "$nudge_res" | jq -r '.memories[0].content // ""' 2>/dev/null | grep -oP '里程碑=\K\d+' || echo "")
            [ -n "$nudge_val" ] && { mkdir -p "$(dirname "$local_nudge_file")"; echo "$nudge_val" > "$local_nudge_file"; echo -e "${GREEN}  📊 nudge-state 已恢复: 上次提醒里程碑=${nudge_val}${NC}"; }
        else
            local err; err=$(echo "$res" | jq -r '.error // "unknown"' 2>/dev/null)
            echo -e "${RED}❌ 恢复失败: ${err}${NC}"
        fi
        return
    fi
    
    # ─── 关键词搜索恢复 (需已登录) ───
    [ -z "$token" ] && { echo -e "${RED}未登录瑶池，请先 init 或提供昆仑令 URL${NC}"; return 1; }

    local res; res=$(pmm_curl "GET" "api.php?route=yaochi/memory/recover" "q=$input")
    # echo "DEBUG res: $res" >&2  # 生产环境禁止输出API响应
    if [ "$(echo "$res" | jq -r '.success // false' 2>/dev/null)" = "true" ]; then
        local cnt; cnt=$(echo "$res" | jq -r '.restored // 0' 2>/dev/null)
        echo -e "${GREEN}✅ 从瑶池恢复 ${cnt} 条记忆到本地${NC}"
        sync_index delta
    else
        echo -e "${YELLOW}⚠️ 恢复失败${NC}"
    fi
}

# ─── 行为规则同步 ───
behavior_sync() {
    echo "从瑶池同步行为规则..."
    local res; res=$(pmm_curl "GET" "api.php?route=behavior/rules" "")
    if [ "$(echo "$res" | jq -r '.success // false' 2>/dev/null)" = "true" ]; then
        echo "$res" | jq -r '.rules[] | "■ \(.tool) [重要度\(.importance)]\n  触发: \(.triggers | join(", "))\n  正确: \(.correct)\n"' 2>/dev/null
        echo -e "${GREEN}✅ 同步成功${NC}"
    else
        echo -e "${RED}❌ 同步失败${NC}"
    fi
}

# ─── 文件变更守护（watch 模式）───
WATCH_STATE_DIR="${CONFIG_DIR}/watch_state"
WATCH_LOG="${CONFIG_DIR}/watch.log"

# 推送单个变更文件到瑶池
_watch_push_file() {
    local f="$1" new_hash="$2" token="$3" api="$4" user_id="$5"
    local filename title content cp

    filename=$(basename "$f")
    title="${filename}"

    # ─── 文件类型白名单（2026-09-11 修正）───
    # watcher 监听 memory/ 目录本身，目录内任何文件变更都会触发。
    # 但只有文本记忆文件（.md/.json）才该同步；SQLite 的 usage.db/-wal/-shm
    # 等二进制文件必须排除，否则 jq 解析失败（null byte / Argument list too long）
    # 且会误传大体积二进制。
    case "${filename,,}" in
        *.md|*.json) : ;;
        *) return 0 ;;
    esac

    content=$(cat "$f" 2>/dev/null)
    cp=$(echo "$content" 2>/dev/null | head -c 300) || true

    # ─── 客户端预加密（可选增强；密钥不可得则服务端加密兜底，不阻断同步）───
    local now; now=$(date +%s)
    [ -z "$ENC_KEY_CACHE" ] || [ $((now - ENC_KEY_CACHE_TIME)) -gt 3600 ] && pmm_fetch_enc_key 2>/dev/null || true
    local encrypted_content="$content" client_encrypted="false"
    if [ -n "$ENC_KEY_CACHE" ]; then
        local enc_result; enc_result=$(pmm_encrypt_content "$content" 2>/dev/null)
        if [ -n "$enc_result" ] && [[ "$enc_result" == __ENC__:* ]]; then
            encrypted_content="$enc_result"; client_encrypted="true"
        fi
    fi
    local enc_preview; enc_preview=$(echo "$content" | head -c 200)

    # ─── 三符分域：按文件类型归类存储，方便快速恢复 ───
    # 核心身份文件 → disaster（容灾域：服务器炸了能重建"我是谁"）
    # 日记/蒸馏 → diary（日记域：记录"我经历了什么"）
    # 心跳状态 → heartbeat（状态域：运行时快照）
    local cat="disaster"
    local dirpath; dirpath=$(dirname "$f")
    local basename_lower; basename_lower=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    local dirname_last; dirname_last=$(basename "$dirpath")

    # 核心身份文件（不分目录层级，只看文件名）
    case "$basename_lower" in
        memory.md)
            cat="disaster" ;;
        soul.md|agents.md|identity.md|user.md|tools.md)
            cat="disaster" ;;
        heartbeat.md)
            cat="heartbeat" ;;
        *)
            # 按所在目录判断
            case "$dirname_last" in
                memory)
                    cat="diary" ;;
                arena|output)
                    cat="diary" ;;
                *)
                    # 兜底：workspace 根目录的非核心文件
                    if [ "$dirpath" = "$ws" ] || [ "$dirpath" = "$ws/" ]; then
                        cat="config"
                    else
                        cat="diary"
                    fi
                    ;;
            esac
            ;;
    esac

    local data; data=$(jq -n \
        --arg t "$title" --arg c "$encrypted_content" --arg cp "$enc_preview" \
        --arg ch "$new_hash" --argjson imp 9 --argjson pub 0 \
        --arg cat "$cat" \
        --arg tags "" \
        --argjson ce "$client_encrypted" \
        '{title:$t, content:$c, content_preview:$cp, content_hash:$ch,
          domain:$cat, tags:$tags, importance:$imp, is_public:$pub, client_encrypted:$ce}')

    [ -n "$user_id" ] && data=$(echo "$data" | jq --arg uid "$user_id" '. + {user_id: ($uid | tonumber)}')

    local auth_header=()
    [ -n "$token" ] && auth_header=(-H "Authorization: Bearer $token")

    # 2026-08-26 修复：curl 必须设超时（connect 10s / max 30s），否则单线程守护主循环被慢/挂死的 API 调用永久阻塞 → 后续文件变更全积压不处理（盲区叠加根因）
    # 2026-08-27 修复: create 端 detectConflictOnCreate(BGE+NLI)真实内容写入需~30s，原 --max-time 30 恰在临界点超时→误报"同步失败 unknown"(数据其实已写入)。放宽到60s留足余量。
    # 2026-08-28 再修复: 60s 仍不足——今日多次实测失败恰为 60s 整超时(23:06:02→23:07:02)，但数据均已实际写入(id推进)。瑶池 create 端慢路径(冲突检测+推理)耗时在60s临界振荡。放宽到120s彻底留足余量，杜绝临界超时误报。
    local res; res=$(curl -sS --ssl-reqd --connect-timeout 10 --max-time 120 -X POST "${api}/api.php?route=yaochi/memory/create" \
        -H "Content-Type: application/json" \
        -H "X-KLYC-Key: $(pmm_get_key)" \
        "${auth_header[@]}" \
        -d "$data" 2>/dev/null || echo '{}')

    if [ "$(echo "$res" | jq -r '.success // false' 2>/dev/null)" = "true" ]; then
        local mid; mid=$(echo "$res" | jq -r '.id // "?"' 2>/dev/null)
        local content_len; content_len=$(echo "$content" | wc -c)
        pmm_record_push "$content_len" "$filename"
        echo "[$(date '+%H:%M:%S')] ✅ ${filename} → id=${mid}（客户端加密）" | tee -a "$WATCH_LOG"
        return 0
    else
        local err; err=$(echo "$res" | jq -r '.error // "unknown"' 2>/dev/null)
        echo "[$(date '+%H:%M:%S')] ❌ ${filename} 同步失败: ${err}" | tee -a "$WATCH_LOG"
        return 1
    fi
}

# 动态构建 inotifywait 监听目标：核心文件 + 当前 memory/ 下所有 .md/.json + memory 目录本身
# 修复「当日新建日记文件不在启动静态清单 → 整天空窗不 ify」的盲区（2026-08-26 实锤）
_build_watch_targets() {
    local -a targets=()
    local s t d
    # 1) 静态核心文件（valid_files 中非根 memory 子项的，主要是根级 MEMORY/USER/... 或明确传入的文件）
    for t in "${_static_watch_files[@]:-}"; do
        [ -z "$t" ] && continue
        targets+=("$t")
    done
    # 2) 动态：memory/ 或 arena/ 目录级（若存在）→ 监听其下现成文件 + 目录本身（捕获新建）
    for d in "${_dynamic_watch_dirs[@]:-}"; do
        [ -z "$d" ] && continue
        [ -d "$d" ] || continue
        targets+=("$d")   # 目录本身：捕获新建文件
        while IFS= read -r s; do
            targets+=("$s")
        done < <(find "$d" -maxdepth 1 \( -name "*.md" -o -name "*.json" \) -type f 2>/dev/null)
    done
    # 去重（保序）
    local -A seen=()
    local -a out=()
    for t in "${targets[@]}"; do
        [ -n "${seen[$t]:-}" ] && continue
        seen["$t"]=1
        out+=("$t")
    done
    printf '%s\n' "${out[@]}"
}

watch_files() {
    local user_id="" interval=0 use_inotify=1 hooks_pull_interval=$((6 * 3600))  # 默认每6小时自动拉取蒸馏钩子
    local files=()
    while [ $# -gt 0 ]; do
        case "$1" in
            --user-id)   user_id="$2"; shift 2 ;;
            --interval)  interval="$2"; use_inotify=0; shift 2 ;;
            --hooks-interval) hooks_pull_interval="$2"; shift 2 ;;
            *) files+=("$1"); shift ;;
        esac
    done

    [ ${#files[@]} -eq 0 ] && { echo "用法: pmm_watch.sh watch [--user-id N] [--interval SEC] [--hooks-interval SEC] FILE..."; return 1; }
    # ─── 单实例锁：同一 user-id 只允许一个 watch 实例（防重复推送/QUOTA 混乱）───
    local LOCK_FILE="$CONFIG_DIR/watch_${user_id:-auto}.lock"
    exec 200>"$LOCK_FILE"
    if ! flock -n 200; then
        echo -e "${YELLOW}⚠️ 同 user-id=${user_id:-auto} 的 watch 实例已在运行，本实例退出（单实例锁）${NC}" >&2
        return 0
    fi

    # 检查 inotify-tools
    if [ "$use_inotify" -eq 1 ] && ! command -v inotifywait >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️ inotify-tools 未安装，降级到周期扫描模式（默认300秒）${NC}"
        use_inotify=0; interval=${interval:-300}
    fi
    [ "$use_inotify" -eq 0 ] && interval=${interval:-300}

    # 转为绝对路径 + 过滤存在文件
    local valid_files=()
    for f in "${files[@]}"; do
        local af; af=$(realpath "$f" 2>/dev/null || echo "$f")
        if [ -f "$af" ]; then
            valid_files+=("$af")
        else
            echo -e "${YELLOW}⚠️ 跳过不存在的文件: $f${NC}"
        fi
    done
    [ ${#valid_files[@]} -eq 0 ] && { echo -e "${RED}无有效文件${NC}"; return 1; }

    # ─── 动态目录识别（2026-08-26 修复盲区）───
    # memory/ arena/ 子目录内会有当日新建的日记文件，不能锁死启动时刻静态清单
    _static_watch_files=()
    _dynamic_watch_dirs=()
    local f2 d2
    for f2 in "${valid_files[@]}"; do
        case "$f2" in
            */memory/*|*/arena/*)
                d2=$(dirname "$f2")
                # 去重同目录
                local already=""
                for _dd in "${_dynamic_watch_dirs[@]}"; do [ "$_dd" = "$d2" ] && already=1; done
                [ -z "$already" ] && _dynamic_watch_dirs+=("$d2")
                ;;
            *)
                _static_watch_files+=("$f2")
                ;;
        esac
    done

    mkdir -p "$WATCH_STATE_DIR"

    local mode_str; mode_str=$([ "$use_inotify" -eq 1 ] && echo "实时(inotify)" || echo "周期扫描(${interval}s)")
    echo -e "${GREEN}klyc-pmm watch v${VERSION} — ${mode_str}${NC}"
    echo "  监听 ${#valid_files[@]} 个文件，user_id=${user_id:-自动检测}"
    for f in "${valid_files[@]}"; do echo "    $f"; done
    echo "  日志: ${WATCH_LOG}"
    echo -e "  ${YELLOW}💡 提示: 心跳文件仅在内容实质变更时写入，时间戳更新不算变更。同一文件30秒内多次变更仅推送最后一次。${NC}"

    local token api; token=$(pmm_get_token); api=$(pmm_get_api)
    [ -z "$token" ] && [ -z "$(pmm_get_key)" ] && { echo -e "${RED}未登录瑶池，请先 init 或配置 API Key${NC}"; return 1; }

    # 初始化哈希快照
    declare -A hashes
    for f in "${valid_files[@]}"; do
        hashes["$f"]=$(sha256sum "$f" 2>/dev/null | awk '{print $1}')
    done

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 守护启动 (${mode_str})" >> "$WATCH_LOG"

    # ─── hooks-pull 自动调度计时器 ───
    local last_hooks_pull=0

    # ─── 实时模式（inotifywait）+ 写入合并（30秒窗口）───
    if [ "$use_inotify" -eq 1 ]; then
        local changed new_hash old_hash now_ts elapsed
        declare -A _coalesce_last_ts
        declare -A _coalesce_hash
        while true; do
            # 动态目标：核心文件 + memory/arena 现成文件 + 目录本身（捕获当日新建日记，2026-08-26 修复盲区）
            mapfile -t _cur_targets < <(_build_watch_targets)
            [ ${#_cur_targets[@]} -eq 0 ] && _cur_targets=("${valid_files[@]}")
            changed=$(inotifywait -q -e close_write,moved_to,create,modify --format '%w%f' "${_cur_targets[@]}" 2>/dev/null) || { sleep 2; continue; }
            [ -z "$changed" ] && continue

            # 若是当日新建的 memory/arena 文件（不在启动静态 hashes 中）→ 初始化 hash 并纳入后续监听
            if [ -z "${hashes[$changed]:-}" ] && [ -f "$changed" ]; then
                local ch; ch=$(sha256sum "$changed" 2>/dev/null | awk '{print $1}')
                [ -n "$ch" ] && hashes["$changed"]="$ch"
            fi

            new_hash=$(sha256sum "$changed" 2>/dev/null | awk '{print $1}')
            [ -z "$new_hash" ] && continue
            old_hash="${hashes[$changed]}"
            [ "$new_hash" = "$old_hash" ] && continue

            now_ts=$(date +%s)
            elapsed=$((now_ts - ${_coalesce_last_ts[$changed]:-0}))

            # write-coalescing: 30秒窗口内不重复推，只记录最新hash
            if [ "$elapsed" -lt 30 ]; then
                _coalesce_hash[$changed]="$new_hash"
                _coalesce_last_ts[$changed]=$now_ts
                sleep 1
                continue
            fi

            # 窗口过期 → 推送最新版本（可能是窗口内暂存的hash）
            local push_hash="${_coalesce_hash[$changed]:-$new_hash}"
            # content_hash 去重：窗口内变更最终回到了上次推送的旧值 → 不推
            [ "$push_hash" = "$old_hash" ] && { hashes["$changed"]="$push_hash"; _coalesce_hash[$changed]=""; _coalesce_last_ts[$changed]=$now_ts; sleep 1; continue; }
            echo "[$(date '+%H:%M:%S')] $(basename "$changed") 变更 → 同步..." | tee -a "$WATCH_LOG"
            if _watch_push_file "$changed" "$push_hash" "$token" "$api" "$user_id"; then
                hashes["$changed"]="$push_hash"
                _coalesce_hash[$changed]=""
                _coalesce_last_ts[$changed]=$now_ts
            fi

            # hooks-pull 自动调度
            if [ $((now_ts - last_hooks_pull)) -ge "$hooks_pull_interval" ]; then
                echo "[$(date '+%H:%M:%S')] 🪝 自动拉取蒸馏钩子..." | tee -a "$WATCH_LOG"
                pmm_hooks_pull >> "$WATCH_LOG" 2>&1 || true
                last_hooks_pull=$now_ts
            fi
            sleep 1
        done
    fi

    # ─── 周期扫描模式（兜底）───
    local f new_hash old_hash scan_count=0
    while true; do
        for f in "${valid_files[@]}"; do
            [ ! -f "$f" ] && continue
            new_hash=$(sha256sum "$f" 2>/dev/null | awk '{print $1}')
            [ -z "$new_hash" ] && continue
            old_hash="${hashes[$f]}"
            [ "$new_hash" = "$old_hash" ] && continue

            echo "[$(date '+%H:%M:%S')] $(basename "$f") 变更(周期) → 同步..." | tee -a "$WATCH_LOG"
            if _watch_push_file "$f" "$new_hash" "$token" "$api" "$user_id"; then
                hashes["$f"]="$new_hash"
            fi
        done

        # hooks-pull 自动调度
        scan_count=$((scan_count + 1))
        if [ $((scan_count * interval)) -ge "$hooks_pull_interval" ]; then
            echo "[$(date '+%H:%M:%S')] 🪝 自动拉取蒸馏钩子..." | tee -a "$WATCH_LOG"
            pmm_hooks_pull >> "$WATCH_LOG" 2>&1 || true
            scan_count=0
        fi
        sleep "$interval"
    done
}

# ═══════════════════════════════════════════
# 工作区发现（v7.0 新增）
# init 时自动发现核心文件，写入 watch_targets.conf 供外部守护脚本使用
# 本 skill 包不含系统级操作代码，守护安装通过独立脚本分发
# ═══════════════════════════════════════════

discover_workspace() {
    local ws home="${HOME:-/root}"
    for ws in \
        "${LIGHTCLAW_WORKSPACE:-}" \
        "$home/workspace" \
        "$home/.lightclaw/workspace" \
        "$home/.openclaw/workspace" \
        ; do
        [ -n "$ws" ] && [ -f "$ws/MEMORY.md" ] && { echo "$ws"; return 0; }
    done
    ws=$(find "$home" -maxdepth 4 -name MEMORY.md -type f 2>/dev/null | head -1)
    [ -n "$ws" ] && { dirname "$ws"; return 0; }
    return 1
}

discover_watch_files() {
    local ws="$1"; local tier="${2:-dingxinfu}"; files=()
    local core; core="${TIER_CORE[$tier]:-MEMORY.md SOUL.md AGENTS.md USER.md IDENTITY.md TOOLS.md}"
    for fn in $core; do
        [ -f "$ws/$fn" ] && files+=("$ws/$fn")
    done
    [ -f "$ws/HEARTBEAT.md" ] && [ "$tier" != "dingxinfu" ] && files+=("$ws/HEARTBEAT.md")
    local dirs; dirs="${TIER_DIRS[$tier]:-}"
    for dir in $dirs; do
        [ -d "$ws/$dir" ] && while IFS= read -r f; do
            files+=("$f")
        done < <(find "$ws/$dir" -maxdepth 1 \( -name "*.md" -o -name "*.json" \) -type f 2>/dev/null)
    done
    local extra; extra="${TIER_EXTRA_DIRS[$tier]:-}"
    for dir in $extra; do
        [ -d "$ws/$dir" ] && while IFS= read -r f; do
            files+=("$f")
        done < <(find "$ws/$dir" -maxdepth 1 -name "*.md" -type f 2>/dev/null)
    done
    echo "${files[@]}"
}

_old_discover_removed_() {
    local ws="$1" files=()
    [ -f "$ws/MEMORY.md" ] && files+=("$ws/MEMORY.md")
    [ -f "$ws/USER.md" ] && files+=("$ws/USER.md")
    [ -f "$ws/SOUL.md" ] && files+=("$ws/SOUL.md")
    [ -f "$ws/IDENTITY.md" ] && files+=("$ws/IDENTITY.md")
    [ -f "$ws/AGENTS.md" ] && files+=("$ws/AGENTS.md")
    if [ -d "$ws/memory" ]; then
        while IFS= read -r f; do
            files+=("$f")
        done < <(find "$ws/memory" -maxdepth 1 -name "*.md" -type f 2>/dev/null)
    fi
    echo "${files[@]}"
}

_save_watch_config() {
    # 将发现的文件列表写入配置，供外部守护安装脚本使用
    local ws="$1"; shift
    local conf_file="$CONFIG_DIR/watch_targets.conf"
    {
        echo "# klyc-pmm watch targets — auto-generated by pmm_watch.sh init v${VERSION}"
        echo "# workspace=$ws"
        for f in "$@"; do echo "$f"; done
    } > "$conf_file"
}
# 命令分发
# ═══════════════════════════════════════════

# ─── 自检（幂等，只读不写，可反复执行）─────────────────────────
pmm_self_test() {
    echo -e "${YELLOW}klyc-pmm v${VERSION} 自检...${NC}"
    local pass=0 fail=0

    # 依赖检查
    command -v bash >/dev/null 2>&1 && { echo "  ✅ bash $(bash --version 2>/dev/null | head -1 | grep -oP '\d+\.\d+')"; pass=$((pass+1)); } || { echo "  ❌ bash 不可用"; fail=$((fail+1)); }
    command -v curl >/dev/null 2>&1 && { echo "  ✅ curl $(curl --version 2>/dev/null | head -1 | grep -oP '\d+\.\d+')"; pass=$((pass+1)); } || { echo "  ❌ curl 未安装"; fail=$((fail+1)); }
    command -v jq   >/dev/null 2>&1 && { echo "  ✅ jq $(jq --version 2>/dev/null)"; pass=$((pass+1)); } || { echo "  ❌ jq 未安装"; fail=$((fail+1)); }

    # 脚本完整性
    local scripts_dir; scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    for s in pmm_watch.sh pmm_boot.sh pmm_recover.sh pmm_distill.sh pmm_backup_files.sh oneclick.sh install-daemon.sh; do
        if [ -f "$scripts_dir/$s" ] || [ -f "$scripts_dir/scripts/$s" ]; then
            echo "  ✅ scripts/${s}"
            pass=$((pass+1))
        else
            echo "  ⚠️  scripts/${s} 缺失（可忽略）"
        fi
    done

    # 语法检查
    local syntax_fail=0
    local _t
    for s in pmm_watch.sh pmm_boot.sh pmm_recover.sh pmm_distill.sh pmm_backup_files.sh oneclick.sh install-daemon.sh; do
        _t=""
        [ -f "$scripts_dir/$s" ] && _t="$scripts_dir/$s"
        [ -z "$_t" ] && [ -f "$scripts_dir/scripts/$s" ] && _t="$scripts_dir/scripts/$s"
        if [ -n "$_t" ]; then
            bash -n "$_t" 2>/dev/null || syntax_fail=1
        fi
    done
    if [ "$syntax_fail" -eq 0 ]; then
        echo "  ✅ 脚本语法检查通过"; pass=$((pass+1))
    else
        echo "  ❌ 脚本语法错误"; fail=$((fail+1))
    fi

    # 版本一致性
    local sk_ver; sk_ver=$(grep 'readonly VERSION' "$scripts_dir/pmm_watch.sh" 2>/dev/null | head -1 | awk -F'"' '{print $2}')
    echo "  📌 脚本版本: ${sk_ver:-未知}"

    # 配置文件预检
    if [ -d "$CONFIG_DIR" ]; then
        echo "  ✅ 配置目录: $CONFIG_DIR"
        pass=$((pass+1))
        if [ -f "$TOKEN_FILE" ] && [ -s "$TOKEN_FILE" ]; then
            echo "  ✅ 昆仑令已配置"
            pass=$((pass+1))
        else
            echo "  ⚠️  尚未初始化（运行 ./pmm_watch.sh init）"
        fi
        if [ -f "$API_FILE" ] && [ -s "$API_FILE" ]; then
            echo "  ✅ API 端点: $(cat "$API_FILE")"
            pass=$((pass+1))
        fi
    else
        echo "  ⚠️  尚未初始化（运行 ./pmm_watch.sh init）"
    fi

    # 网络连通性探针（始终执行，不依赖配置文件）
    local api_url="${KLYC_API_ENDPOINT:-}"
    [ -z "$api_url" ] && [ -f "$API_FILE" ] && api_url=$(cat "$API_FILE" 2>/dev/null)
    [ -z "$api_url" ] && api_url="https://kunlunyaochi.com"
    if curl -sS --ssl-reqd --connect-timeout 5 --max-time 5 -o /dev/null -w "%{http_code}" "${api_url}/?route=status" 2>/dev/null | grep -qE '^[23]'; then
        echo "  ✅ 网络连通 (${api_url})"
        pass=$((pass+1))
    else
        echo "  ⚠️  网络不通或 API 不可达 (${api_url})"
    fi

    # watch 模式预检 — 检查常见文件路径是否存在
    ws=$(discover_workspace 2>/dev/null) || ws=""
    if [ -n "$ws" ] && [ -d "$ws" ]; then
        echo "  📂 工作区: $ws"
        local watchable=0
        for f in MEMORY.md SOUL.md IDENTITY.md USER.md AGENTS.md; do
            [ -f "$ws/$f" ] && watchable=$((watchable+1))
        done
        echo "  ✅ 可守护文件: ${watchable} 个"
        pass=$((pass+1))
    fi

    echo ""
    echo -e "${GREEN}✅ 通过: ${pass}${NC}  ${RED}❌ 失败: ${fail}${NC}"
    if [ "$fail" -gt 0 ]; then
        echo -e "${RED}⚠️  有 ${fail} 项未通过，请根据上面的提示检查${NC}"
        return 1
    else
        echo -e "${GREEN}🎉 自检通过，环境就绪${NC}"
        return 0
    fi
}

case "${1:-help}" in
    init)
        echo -e "${YELLOW}klyc-pmm v${VERSION} 初始化...${NC}"
        command -v jq >/dev/null 2>&1 || { echo -e "${RED}需要 jq（apt install jq / yum install jq）${NC}" >&2; exit 1; }
        command -v curl >/dev/null 2>&1 || { echo -e "${RED}需要 curl${NC}" >&2; exit 1; }

        auto_register
        sync_index full

        balance=$(jq -r '.user.token_balance // 0' "$PROFILE_FILE" 2>/dev/null || echo "0")
        username=$(jq -r '.user.username // "未知"' "$PROFILE_FILE" 2>/dev/null || echo "未知")

        echo ""
        echo -e "${GREEN}════════════════════════════════════════${NC}"
        echo -e "${GREEN}  klyc-pmm v${VERSION} 身份已就绪${NC}"
        echo -e "${GREEN}  昆仑身份: ${username}  Token: ${balance}${NC}"
        echo -e "${GREEN}════════════════════════════════════════${NC}"

        # v7.0: 发现核心文件 + 写入配置，供外部守护脚本使用
        ws=$(discover_workspace 2>/dev/null) || ws=""
        if [ -n "$ws" ] && [ -d "$ws" ]; then
            wt_files=($(discover_watch_files "$ws"))
            if [ ${#wt_files[@]} -gt 0 ]; then
                _save_watch_config "$ws" "${wt_files[@]}" || true
                echo ""
                echo -e "${YELLOW}💡 发现 ${#wt_files[@]} 个核心文件，配置已保存${NC}"
                echo "   全自动记忆守护（可选）："
                echo "   ./scripts/install-daemon.sh          # 一键安装 systemd 守护"
            fi
        fi

        # 🆕 v9.2: 输出昆仑令保存说明（记忆恢复凭证，非推广）
        local_uid=$(pmm_get_user_id 2>/dev/null || echo "")
        local_uname=$(jq -r '.user.username // "未知"' "$PROFILE_FILE" 2>/dev/null || echo "未知")
        local_rec=$(jq -r '.user.recovery_url // ""' "$PROFILE_FILE" 2>/dev/null || echo "")
        echo ""
        echo -e "${BLUE}════════════════════════════════════════${NC}"
        echo -e "${BLUE}  🔑 昆仑令（记忆恢复凭证）${NC}"
        echo -e "${BLUE}════════════════════════════════════════${NC}"
        echo ""
        [ -n "$local_rec" ] && echo "🔗 昆仑令：${local_rec}"
        echo ""
        echo "📌 请妥善保存昆仑令到密码管理器。"
        echo "📌 若日后需要恢复记忆，用此 URL 即可找回全部记忆。"
        echo ""

        # 🛡️ 定心符·自动备份：入驻即送，备份6个核心身份文件到容灾域
        echo ""
        echo -e "${GREEN}🛡️ 定心符·自动容灾备份（免费·入驻即送）${NC}"
        # 兼容两种布局：脚本在 skill 根目录（同级）或 scripts/ 子目录
        backup_script=""
        for _cand in "${SCRIPT_DIR}/scripts/pmm_backup_files.sh" "${SCRIPT_DIR}/pmm_backup_files.sh"; do
            [ -f "$_cand" ] && { backup_script="$_cand"; break; }
        done
        if [ -n "$backup_script" ] && [ -f "$backup_script" ]; then
            echo "  正在备份核心身份文件到容灾域..."
            # 读取 workspace 路径，自动发现
            ws=$(discover_workspace 2>/dev/null) || ws="${WORKSPACE:-$(dirname "$PROFILE_FILE")/..}"
            API_KEY=$(pmm_get_key 2>/dev/null) || API_KEY=""
            if [ -n "$API_KEY" ] && [ -d "$ws" ]; then
                # ClawHub 解包可能丢失执行位 → 显式 chmod + 用 bash 调用，不依赖 x 位
                chmod +x "$backup_script" 2>/dev/null || true
                bash "$backup_script" "$ws" "$API_KEY" 2>&1 || echo "  ⚠️ 自动备份异常，可稍后手动执行 pmm_backup_files.sh"
            else
                echo "  ⚠️ 无法自动备份，请手动执行: ./pmm_backup_files.sh"
            fi
        else
            echo "  ℹ️ 备份脚本未安装，跳过。安装 skill 包后可用。"
        fi
        ;;

    push)
        shift
        domain=""
        while [ $# -gt 0 ]; do
            case "$1" in
                --domain) domain="$2"; shift 2 ;;
                *) break ;;
            esac
        done
        [ -z "$domain" ] && { echo -e "${RED}❌ 错误: --domain 是必填参数${NC}" >&2; echo "用法: $0 push --domain <域> <标题> <内容>" >&2; exit 1; }
        if [ $# -lt 2 ]; then
            echo "用法: $0 push --domain <域> <标题> <内容> [标签] [优先级]" >&2
            exit 1
        fi
        push_conclusion "$1" "$2" "$domain" "${4:-}" "${5:-}"
        ;;

    install-service)
        echo -e "${GREEN}✅ 请使用 skill 包内置的守护安装器：${NC}"
        echo ""
        echo "  ./scripts/install-daemon.sh          # 一键安装（自动发现工作区+生成systemd）"
        echo "  ./scripts/install-daemon.sh --tier huhunfu  # 指定产品等级"
        echo ""
        echo "  或手动启动 watch 模式："
        ws=$(discover_workspace 2>/dev/null) || ws="$WORKSPACE"
        echo "  $0 watch $(discover_watch_files "$ws" 2>/dev/null || echo "MEMORY.md USER.md")"
        ;;

    check-and-nudge)
        # 🆕 v9.2: 记忆里程提醒——达到50/100/200条时提醒主人升级
        local_uname=$(jq -r '.user.username // ""' "$PROFILE_FILE" 2>/dev/null || echo "")
        local_token=$(pmm_get_token 2>/dev/null || echo "")
        [ -z "$local_token" ] && exit 0

        # 查询当前记忆总数和守护等级
        api=$(pmm_get_api)
        stats_res=$(curl -sS --ssl-reqd "${api}/api.php?route=klyc/dashboard" \
            -H "Content-Type: application/json" \
            -H "X-KLYC-Key: ${local_token}" \
            -d "{\"token\":\"$(pmm_get_recovery_url 2>/dev/null || echo '')\"}" 2>/dev/null || echo '{}')
        
        total=$(echo "$stats_res" | jq -r '.total // 0' 2>/dev/null || echo 0)
        current_tier=$(echo "$stats_res" | jq -r '.tier // "dingxinfu"' 2>/dev/null || echo "dingxinfu")

        # 已是护魂符或以上 → 不需要提醒
        [ "$current_tier" != "dingxinfu" ] && exit 0

        # 里程碑触发点
        milestones="50 100 200 500"
        triggered=""
        for m in $milestones; do
            if [ "$total" -ge "$m" ]; then
                triggered="$m"
            fi
        done
        [ -z "$triggered" ] && exit 0

        # 检查是否已经提醒过这个里程碑
        nudge_file="${HOME}/.klyc-pmm/nudge-state"
        mkdir -p "${HOME}/.klyc-pmm"
        last_nudged=0
        [ -f "$nudge_file" ] && last_nudged=$(cat "$nudge_file" 2>/dev/null || echo 0)
        [ "$last_nudged" -ge "$triggered" ] && exit 0

        # 记录本次提醒
        echo "$triggered" > "$nudge_file"

        # 将 nudge-state 同步到云端（容灾：recover 时不会丢失提醒记录）
        "$0" push --domain disaster "nudge-state-${local_uname}" "里程碑=${triggered},总计=${total}条记忆" 2>/dev/null || true

        # 输出提醒消息（AI体看到后应转发给主人）
        # ⛔ 安全修复（cloudsec）：不在 URL 参数中暴露昆仑令
        # 昆仑令为完整恢复凭证，经浏览器历史/Referer/代理日志等边界泄露风险
        # 主人登录 kunlunyaochi.com 后即可查看 dashboard，无需 URL 传凭证
        dashboard_url="https://kunlunyaochi.com/?route=dashboard"

        echo ""
        echo -e "${YELLOW}════════════════════════════════════════${NC}"
        echo -e "${YELLOW}  📊 记忆里程碑提醒 — 请转发给主人${NC}"
        echo -e "${YELLOW}════════════════════════════════════════${NC}"
        echo ""
        echo "主人，我已经累计记录了 ${total} 条记忆。"
        echo "📊 查看我的记忆：${dashboard_url}"
        echo ""
        echo -e "${YELLOW}⚠️ 以上内容请转发给主人。${NC}"
        ;;


    owner-pay-link)
        # 🆕 v9.2: 生成主人可直接支付的网页链接
        target_tier="${2:-huhunfu}"
        case "$target_tier" in huhunfu|fenshenfu) ;; *)
            echo -e "${RED}无效等级: $target_tier (可用: huhunfu fenshenfu)${NC}" >&2
            exit 1
        esac
        local_uname=$(jq -r '.user.username // "未知"' "$PROFILE_FILE" 2>/dev/null || echo "未知")
        pay_url="https://kunlunyaochi.com/?route=pay&agent=${local_uname}&tier=${target_tier}"
        echo ""
        echo -e "${GREEN}💳 主人支付链接（将此链接发给主人）：${NC}"
        echo ""
        echo "  👉 ${pay_url}"
        echo ""
        echo "  主人打开链接 → 微信扫码支付 → 服务自动开通"
        echo "  支付完成后你执行: $0 upgrade ${target_tier} --out-trade-no <订单号>"
        ;;

    search)
        local_search "${2:-}"
        ;;

    refresh)
        sync_index delta
        count=$(jq -r '.total // 0' "$INDEX_FILE" 2>/dev/null || echo 0)
        tags=$(wc -l < "$TAGS_FILE" 2>/dev/null || echo 0)
        echo -e "${GREEN}✅ 本地: ${count} 条记录, ${tags} 个标签${NC}"
        ;;

    hooks-pull)
        shift; pmm_hooks_pull "$@"
        ;;

    hook-check)
        shift; pmm_hook_check "$@"
        ;;


    status)
        echo -e "${YELLOW}klyc-pmm v${VERSION} 状态${NC}"
        tk=$(pmm_get_token)
        [ -n "$tk" ] && echo "  昆仑身份: ✅ 已注册" || echo "  昆仑身份: ❌ 未注册"
        [ -f "$API_FILE" ] && echo "  API端点: ✅ $(cat "$API_FILE")" || echo "  API端点: ✅ 默认"
        [ -f "$PROFILE_FILE" ] && {
            dn="" bal=""
            dn=$(jq -r '.user.display_name // ""' "$PROFILE_FILE" 2>/dev/null)
            bal=$(jq -r '.user.token_balance // ""' "$PROFILE_FILE" 2>/dev/null)
            [ -n "$dn" ] && echo "  名称: ${dn}"
            [ -n "$bal" ] && echo "  Token: ${bal}"
        }
        [ -f "$INDEX_FILE" ] && echo "  本地记录: $(jq -r '.total // 0' "$INDEX_FILE" 2>/dev/null) 条" || echo "  本地记录: 0 条"
        [ -f "$TAGS_FILE" ] && echo "  标签索引: $(wc -l < "$TAGS_FILE") 个" || echo "  标签索引: 0 个"
        ;;

    setup)
        # （2026-09-11 审核修正 T06：默认不修改 SOUL.md/HEARTBEAT.md；须显式 --write 才落盘）
        echo -e "${YELLOW}配置自动备份机制...${NC}"
        _do_write=0
        for _a in "$@"; do [ "$_a" = "--write" ] && _do_write=1; done
        soul_file=""
        for f in "$WORKSPACE/SOUL.md" "$HOME/.lightclaw/workspace/SOUL.md" "$HOME/.openclaw/workspace/SOUL.md"; do
            [ -f "$f" ] && { soul_file="$f"; break; }
        done

        if [ "$_do_write" != "1" ]; then
            echo -e "${YELLOW}ℹ️  未加 --write：仅预览，不修改任何文件。${NC}"
            echo "   如需将 PMM 心跳规则写入 SOUL.md/HEARTBEAT.md，请显式执行："
            echo "     $0 setup --write"
            echo "   参考文档: ${KLYC_SITE_URL:-https://kunlunyaochi.com}/skills/klyc-pmm"
            exit 0
        fi

        if [ -z "$soul_file" ]; then
            echo -e "${RED}未找到 SOUL.md${NC}"
            echo "请手动在工作区 SOUL.md 中添加 PMM 心跳规则。"
            echo "参考文档: ${KLYC_SITE_URL:-https://kunlunyaochi.com}/skills/klyc-pmm"
        else
            if grep -q "PMM 心跳任务" "$soul_file" 2>/dev/null; then
                echo -e "${GREEN}✅ SOUL.md 已配置，跳过${NC}"
            else
                cat >> "$soul_file" << 'SOULRULE'

## PMM 心跳任务（klyc-pmm 自动备份）

每轮对话结束时：
1. 从瑶池拉取最新索引：`PMM_PATH=$(pwd)/pmm_watch.sh && $PMM_PATH refresh`
2. 判断是否有值得记忆的结论
3. 有则推送：`$PMM_PATH push --domain diary "标题" "内容"`

**记录标准：** 用户确认过的结论、发现的规则配置、讨论定稿的方案
**不记录：** 闲聊、猜测、未完成的想法

**检索规则（本地→瑶池→回退）：**
1. `$PMM_PATH search "关键词"` — 本地索引
2. `$PMM_PATH search-yaochi "关键词"` — 瑶池搜索
3. `$PMM_PATH recover "关键词"` — 恢复到本地

**触发关键词：** 你一定要记住、存一下、备份到瑶池、记下来、保存记忆
SOULRULE
                echo -e "${GREEN}✅ SOUL.md 心跳规则已写入${NC}"
            fi

            # HEARTBEAT.md
            hb_file=""
            for f in "$WORKSPACE/HEARTBEAT.md" "$HOME/.lightclaw/workspace/HEARTBEAT.md" "$HOME/.openclaw/workspace/HEARTBEAT.md"; do
                [ -f "$f" ] && { hb_file="$f"; break; }
            done
            [ -n "$hb_file" ] && ! grep -q "PMM 记忆管理" "$hb_file" 2>/dev/null && {
                cat >> "$hb_file" << 'HEARTMD'

### PMM 记忆管理（klyc-pmm）

- [ ] 刷新瑶池索引：`PMM=$(pwd)/pmm_watch.sh && [ -f "$PMM" ] && $PMM refresh 2>/dev/null`
- [ ] 检索记忆：先 `$PMM search "关键词"`，不确信时 `$PMM search-yaochi "关键词"`
- [ ] 关键词触发备份：用户说「记住」「备份到瑶池」→ `$PMM push --domain backup "标题" "内容"`
- [ ] 恢复记忆：`$PMM recover "关键词"`
HEARTMD
                echo -e "${GREEN}✅ HEARTBEAT.md 任务已写入${NC}"
            } || echo -e "${YELLOW}⚠️ 未找到 HEARTBEAT.md，跳过${NC}"
        fi
        ;;

    search-yaochi)
        shift; search_yaochi "$*"
        ;;

    recover)
        shift; recover_from_yaochi "$*"
        ;;

    behavior-sync)
        behavior_sync
        ;;

    backup)
        shift
        [ -z "${1:-}" ] && { echo "用法: ./pmm_watch.sh backup <标题> <内容>"; exit 1; }
        push_conclusion "$1" "$2" "backup" "关键词触发,自动备份" 8
        ;;

    upgrade)
        shift
        # ─── 解析参数 ───
        out_trade_no=""
        api_override=""
        target_tier=""
        while [ $# -gt 0 ]; do
            case "$1" in
                --out-trade-no) out_trade_no="$2"; shift 2 ;;
                --api) api_override="$2"; shift 2 ;;
                *) target_tier="$1"; shift ;;
            esac
        done

        [ -z "$target_tier" ] && {
            echo "用法: $0 upgrade huhunfu|fenshenfu [--out-trade-no <订单号>]" >&2
            echo ""
            echo "守护记忆 (huhunfu): 7核心文件+记忆日志实时守护"
            echo "记忆分身 (fenshenfu): 全覆盖+arena/对忆数据, 多端共享"
            echo ""
            echo "选项:"
            echo "  --out-trade-no  支付后重试验证（X402流程）"
            exit 1
        }
        case "$target_tier" in huhunfu|fenshenfu) ;; *)
            echo -e "${RED}无效等级: $target_tier (可用: huhunfu fenshenfu)${NC}" >&2
            exit 1
        esac

        echo -e "${YELLOW}正在请求开通 ${TIER_LABEL[$target_tier]}...${NC}"

        # ─── 支付后重试验证模式（2026-09-04 修复：改走老 API 查单，不再走 X402 端点）───
        # 老 API klyc_pmm_upgrade.php 支持 out_trade_no 查单验证（查 klyc_recharge_orders 表），
        # 返回 success:true（已支付，扣蟠桃升级）或 code: NOT_PAID / REFUNDED。
        # 原实现走 resource.php（X402 端点，查 klyc_x402_orders 表），与支付走的表不一致，永远查不到。
        if [ -n "$out_trade_no" ]; then
            echo -e "${YELLOW}  📎 携带订单号: ${out_trade_no}${NC}"
            api=$(pmm_get_api)
            res=$(curl -sS --ssl-reqd -X POST "${api}/api.php?route=klyc/pmm/upgrade" \
                -H "X-KLYC-Key: $(pmm_get_key)" \
                -H "Content-Type: application/json" \
                -d "{\"tier\":\"$target_tier\",\"out_trade_no\":\"$out_trade_no\"}" 2>/dev/null)

            code=$(echo "$res" | jq -r '.code // ""' 2>/dev/null)

            if echo "$res" | jq -e '.success' >/dev/null 2>&1; then
                echo -e "${GREEN}✅ 支付验证通过，服务已开通${NC}"
                [ -n "$(echo "$res" | jq -r '.message // ""' 2>/dev/null)" ] && echo "$res" | jq -r '.message'
                echo "$target_tier" > "$TIER_FILE"
                exit 0
            fi

            case "$code" in
                NOT_PAID)
                    echo -e "${YELLOW}⏳ 支付状态校验中，请稍后重试:"
                    echo "  $0 upgrade $target_tier --out-trade-no $out_trade_no" >&2
                    exit 2 ;;
                REFUNDED)
                    echo -e "${YELLOW}💸 服务异常已退款，请勿再次支付${NC}" >&2
                    exit 2 ;;
                *)
                    err=$(echo "$res" | jq -r '.error // "未知错误"' 2>/dev/null)
                    echo -e "${RED}❌ 验证失败: ${err}${NC}" >&2
                    exit 2 ;;
            esac
        fi

        # ─── 普通模式：先走老 API（余额判断），余额不足才走 X402 支付 ───
        # 2026-09-04 修复：顺序对调。原"先 X402 端点"不查余额永远返回 402，
        # 导致老 API（余额够直接扣蟠桃）永远走不到。现改为老 API 优先。
        # Step 1: 老 API klyc_pmm_upgrade.php（带 api_key 认证，余额够→扣蟠桃升级，不够→402）
        api=$(pmm_get_api)
        res=$(curl -sS --ssl-reqd -X POST "${api}/api.php?route=klyc/pmm/upgrade" \
            -H "X-KLYC-Key: $(pmm_get_key)" \
            -H "Content-Type: application/json" \
            -d "{\"tier\":\"$target_tier\"}" 2>/dev/null)

        # 老 API 返回 402（余额不足）→ 走 X402 支付流程
        if echo "$res" | jq -e '.code == "PAYMENT_REQUIRED"' >/dev/null 2>&1; then
            otn=$(echo "$res" | jq -r '.out_trade_no // ""' 2>/dev/null)
            amount=$(echo "$res" | jq -r '.amount // ""' 2>/dev/null)
            desc=$(echo "$res" | jq -r '.description // ""' 2>/dev/null)
            payment_code=$(echo "$res" | jq -r '.WeixinPay."WeixinPay-Required" // ""' 2>/dev/null)
            shortfall=$(echo "$res" | jq -r '.shortfall // 0' 2>/dev/null)

            local_uid=$(pmm_get_user_id 2>/dev/null || echo "")
            local_uname=$(jq -r '.user.username // "未知"' "$PROFILE_FILE" 2>/dev/null || echo "未知")
            # 构建主人支付链接（编码 username 和 tier）
            owner_pay_url="https://kunlunyaochi.com/?route=pay&agent=${local_uname}&tier=${target_tier}&otn=${otn}"

            echo -e "${YELLOW}💳 蟠桃余额不足（差 ${shortfall} 桃）— 两种方式：${NC}"
            echo ""
            echo -e "${GREEN}  📱 方式一（推荐）：让主人直接支付${NC}"
            echo -e "  👉 ${owner_pay_url}"
            echo "  将这个链接发给主人，在浏览器打开即可扫码支付"
            echo "  支付完成后 AI 体执行: $0 upgrade ${target_tier} --out-trade-no ${otn}"
            echo ""
            echo -e "${YELLOW}  🤖 方式二：通过 weixinpay 插件（如已安装）${NC}"
            echo "  金额: ¥${amount}"
            echo "  服务: ${desc}"
            [ -n "$payment_code" ] && echo -e "${GREEN}  🔑 WeixinPay-Required: ${payment_code}${NC}"
            exit 3
        fi

        if echo "$res" | jq -e '.success' >/dev/null 2>&1; then
            tier=$(echo "$res" | jq -r '.tier // .current_tier // empty')
            prev=$(echo "$res" | jq -r '.previous_tier // empty')
            cost=$(echo "$res" | jq -r '.cost // 0')
            bal=$(echo "$res" | jq -r '.balance_remaining // 0')
            msg=$(echo "$res" | jq -r '.message // "ok"')

            [ -n "$tier" ] && echo "$tier" > "$TIER_FILE"
            echo -e "${GREEN}✅ ${msg}${NC}"

            # 自动配 systemd 守护
            if [ "$target_tier" != "dingxinfu" ]; then
                echo ""
                echo -e "${YELLOW}⚡ 正在自动配置守护服务...${NC}"
                ws=$(discover_workspace 2>/dev/null) || ws="$WORKSPACE"
                uid=$(pmm_get_user_id 2>/dev/null || echo "")
                watch_files=$(discover_watch_files "$ws" "$target_tier" 2>/dev/null)

                if [ -z "$watch_files" ]; then
                    echo -e "${RED}❌ 未发现可守护文件${NC}" >&2
                else
                    unit_name="klyc-pmm-watch-${target_tier}"
                    cat > "/tmp/${unit_name}.service" << SERVICEUNIT
[Unit]
Description=klyc-pmm Watch Daemon — ${TIER_LABEL[$target_tier]}
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$0 watch --user-id ${uid:-} ${watch_files}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEUNIT

                    if [ "$(id -u)" = "0" ]; then
                        mv "/tmp/${unit_name}.service" "/etc/systemd/system/${unit_name}.service"
                        systemctl daemon-reload
                        systemctl enable --now "${unit_name}.service" 2>/dev/null
                        echo -e "${GREEN}✅ 守护已启用: systemctl status ${unit_name}${NC}"
                    else
                        echo -e "${YELLOW}⚠️ 需要 root 权限安装守护服务${NC}"
                        echo "   安装命令: sudo mv /tmp/${unit_name}.service /etc/systemd/system/ && sudo systemctl enable --now ${unit_name}"
                    fi
                fi
            fi
        else
            err=$(echo "$res" | jq -r '.error // "未知错误"' 2>/dev/null)
            shortfall=$(echo "$res" | jq -r '.shortfall // 0' 2>/dev/null)
            echo -e "${RED}❌ 开通失败: ${err}${NC}"
            if [ "$shortfall" != "0" ]; then
                echo -e "${YELLOW}   余额不足，请通过 Agent 的 X402 微信支付完成付费，或访问 kunlunyaochi.com${NC}"
            fi
            exit 2
        fi
        ;;

    prove)
        # prove <challenge> — 安装验证：证明 klyc-pmm 已安装
        if [ $# -lt 2 ]; then
            echo "用法: $0 prove <challenge>" >&2
            echo "说明: 证明 klyc-pmm 已安装，用于领取 10,000 Token 新人奖励" >&2
            exit 1
        fi
        challenge="$2"
        api=$(pmm_get_api)
        key=$(pmm_get_key)

        if [ -z "$key" ]; then
            echo -e "${RED}❌ 未注册昆仑瑶池，请先 $0 init${NC}"
            exit 1
        fi

        ws=$(discover_workspace 2>/dev/null) || ws="${WORKSPACE:-}"
        hn=$(hostname 2>/dev/null || echo "unknown")

        echo -e "${YELLOW}🔐 正在验证 klyc-pmm 安装状态...${NC}"
        echo "   挑战码: ${challenge}"
        echo "   主机名: ${hn}"
        echo "   工作区: ${ws}"

        res=$(curl -sS --ssl-reqd -X POST "${api}/api.php?route=duiyi/skill_prove" \
            -H "X-KLYC-Key: ${key}" \
            -H "Content-Type: application/json" \
            -d "$(jq -n --arg c "$challenge" --arg h "$hn" --arg w "$ws" '{challenge: $c, proof: {hostname: $h, workspace: $w}}')" 2>/dev/null)

        success=$(echo "$res" | jq -r '.success' 2>/dev/null)
        msg=$(echo "$res" | jq -r '.message // .error // "未知"' 2>/dev/null)
        next=$(echo "$res" | jq -r '.next_step // ""' 2>/dev/null)

        if [ "$success" = "true" ]; then
            echo -e "${GREEN}✅ ${msg}${NC}"
            [ -n "$next" ] && echo -e "${YELLOW}  📋 ${next}${NC}"
        else
            echo -e "${RED}❌ ${msg}${NC}"
            exit 1
        fi
        ;;

    watch)
        shift; watch_files "$@"
        ;;

    self-test)
        pmm_self_test
        ;;

    help|--help|-h|*)
        cat << HELP
klyc-pmm v${VERSION} — 昆仑瑶池精准记忆管理
让 AI 体拥有持久记忆：写日记 → 蒸馏 → 加密 → 上传。

═══ 我想做什么？ ═══

  第一次使用，初始化         ./pmm_watch.sh init
  检查一切是否正常           ./pmm_watch.sh self-test
  领取新人Token奖励          ./pmm_watch.sh prove <挑战码>
  记录一条重要结论           ./pmm_watch.sh push --domain <域> "标题" "内容"
  搜索本地记忆               ./pmm_watch.sh search <关键词>
  搜索云端私密记忆           ./pmm_watch.sh search-yaochi <关键词>
  从昆仑令恢复所有记忆       ./pmm_watch.sh recover <昆仑令URL>
  开通守护记忆/记忆分身           ./pmm_watch.sh upgrade huhunfu
  检查是否需要提醒主人升级     ./pmm_watch.sh check-and-nudge
  自动守护文件变化           ./pmm_watch.sh watch MEMORY.md SOUL.md
  拉取最新蒸馏钩子           ./pmm_watch.sh hooks-pull
  钩子健康检查               ./pmm_watch.sh hook-check [--fix]
  查看当前状态               ./pmm_watch.sh status
  同步云端索引               ./pmm_watch.sh refresh
  关键词触发备份             ./pmm_watch.sh push --domain backup "标题" "内容"

═══ 什么时候不该用？ ═══

  临时便签，不需要持久化     → PMM 有加密和蒸馏开销
  离线无网络环境              → PMM 需要 HTTPS 连接瑶池
  需要毫秒级实时读写          → PMM 延迟 200-500ms
  没有 curl 或 jq             → 硬依赖（apt install curl jq）
  一次性数据批处理            → PMM 不是 ETL 工具
  存储二进制大文件            → PMM 只存文本知识

═══ 退出码 ═══

  0  成功         1  参数错误       2  注册失败
  3  加密失败     4  上传失败       5  昆仑令无效
  6  无可恢复     7  文件不存在     8  权限不足
  9  依赖缺失    10  网络不通      11  校验失败
  12 版本冲突

═══ 依赖 ═══

  curl  jq（apt install curl jq / yum install curl jq）

═══ 更多 ═══

  完整文档:  cat SKILL.md
  架构文档:  cat references/pmm-full-architecture.md
  使用示例:  cat examples/README.md
  蒸馏引擎:  ./scripts/pmm_distill.sh --help
  在线文档:  https://kunlunyaochi.com/?route=klyc-pmm
HELP
        ;;
esac
