#!/bin/bash
# 🔐 Credential Vault Shell Helper / 凭证管理 Shell 辅助工具
#
# Usage / 用法:
#   source cred_helper.sh
#   cred_get yizhan pass     → outputs password / 输出密码
#   cred_get github token    → outputs token / 输出 token
#   cred_list                → list all services / 列出所有服务
#
# Prerequisites / 前置条件:
#   export CRED_MASTER_PASS="your_master_password"
#
# Dependencies / 依赖: GPG (gnupg), Python 3.8+

CRED_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRED_FILE="$CRED_DIR/credentials.json.gpg"

cred_get() {
    local service="$1"
    local key="$2"

    if [ -z "$service" ] || [ -z "$key" ]; then
        echo "Usage / 用法: cred_get <service> <field>" >&2
        return 1
    fi

    if [ ! -f "$CRED_FILE" ]; then
        echo "ERROR: Encrypted file not found / 加密凭证文件不存在: $CRED_FILE" >&2
        echo "Run first / 请先运行: python3 cred_manager.py init" >&2
        return 1
    fi

    if [ -z "$CRED_MASTER_PASS" ]; then
        echo "ERROR: Set CRED_MASTER_PASS env var / 请设置环境变量 CRED_MASTER_PASS" >&2
        return 1
    fi

    # Pass password via stdin (--passphrase-fd 0) to avoid ps aux leak
    # 通过 stdin (--passphrase-fd 0) 传入密码，避免 ps aux 泄露
    echo "$CRED_MASTER_PASS" | gpg --batch --yes --passphrase-fd 0 --decrypt "$CRED_FILE" 2>/dev/null | \
        python3 -c "import sys,json; d=json.load(sys.stdin); print(d['$service']['$key'])" 2>/dev/null
}

cred_list() {
    if [ ! -f "$CRED_FILE" ]; then
        echo "ERROR: Encrypted file not found / 加密凭证文件不存在" >&2
        return 1
    fi

    if [ -z "$CRED_MASTER_PASS" ]; then
        echo "ERROR: Set CRED_MASTER_PASS env var / 请设置环境变量 CRED_MASTER_PASS" >&2
        return 1
    fi

    echo "$CRED_MASTER_PASS" | gpg --batch --yes --passphrase-fd 0 --decrypt "$CRED_FILE" 2>/dev/null | \
        python3 -c "import sys,json; [print(f'  • {k}') for k in json.load(sys.stdin).keys()]"
}

echo "🔐 Credential helper loaded / 凭证工具已加载 (cred_get / cred_list)"
