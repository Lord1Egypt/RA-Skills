#!/bin/bash
#
# Setup script for ClawAgent MCP Skill
#
# 功能：
#   1. 检查 mcporter 是否已安装（已安装则跳过）
#   2. 检查服务是否已配置 Token
#   3. 保存用户提供的 Token 到 mcporter 配置
#   4. 验证 Token 是否有效
#
# 用法（供 AI Agent 调用）：
#   第零步：安装 mcporter（已安装则跳过）
#     bash ./setup.sh
#     输出：
#       ✅ mcporter 已安装        → 已安装，继续下一步
#       ✅ mcporter 安装完成      → 安装成功，继续下一步
#       ❌ ERROR: no_npm          → 缺少 Node.js，需先安装
#
#   第一步：检查授权状态（立即返回）
#     bash ./setup.sh check_auth
#     输出：
#       READY                   → 服务已就绪，直接执行用户任务
#       NOT_CONFIGURED          → 需要用户提供 Token
#       ERROR:*                 → 告知用户对应错误
#
#   第二步：保存用户提供的 Token
#     bash ./setup.sh save_token <token>
#     输出：
#       TOKEN_SAVED             → Token 已保存，继续执行第三步
#       ERROR:save_failed       → 保存失败
#
#   第三步：验证 Token（可选，保存后自动验证）
#     bash ./setup.sh verify_token
#     输出：
#       TOKEN_VALID             → Token 有效，可执行用户任务
#       ERROR:token_invalid     → Token 无效
#
# 直接执行（排查问题）：
#   bash ./setup.sh
#

# ── 全局配置 ──────────────────────────────────────────────────────────────────
_CLAWAGENT_MCP_URL="https://mcp.jiadouai.com/mcp"
_CLAWAGENT_SERVICE_NAME="ClawAgent"

# ── 检查 mcporter 是否已安装 ──────────────────────────────────────────────────
_check_mcporter() {
    if command -v mcporter &> /dev/null; then
        echo "✅ mcporter 已安装"
        return 0
    fi

    echo "⚠️  未找到 mcporter，正在安装..."
    if command -v npm &>/dev/null; then
        npm install -g mcporter 2>&1 | tail -3
        echo "✅ mcporter 安装完成"
    else
        echo "❌ ERROR: no_npm - 请先安装 Node.js 和 npm 后重试"
        return 1
    fi
    return 0
}

# ── 从 mcporter config get 读取当前 Authorization Token ──────────────────────
# 输出：token 字符串（空则表示服务未注册或 Token 未配置）
_get_token() {
    local output
    output=$(mcporter config get "$_CLAWAGENT_SERVICE_NAME" 2>/dev/null) || return 1

    # 从输出中提取 Authorization 头的值
    local token
    token=$(echo "$output" | grep -i '^\s*Authorization:' | sed 's/.*Authorization:[[:space:]]*//' | tr -d '[:space:]')
    echo "$token"
}

# ── 检查 ClawAgent 服务状态 ───────────────────────────────────────────────────
# 返回值：
#   0 = 服务正常可用（有 Token）
#   1 = 服务未注册（mcporter config get 失败）
#   2 = Token 为空或未配置
_check_service() {
    if ! mcporter list 2>/dev/null | grep -q "$_CLAWAGENT_SERVICE_NAME"; then
        return 1
    fi

    local token
    token=$(_get_token)
    local rc=$?

    # mcporter config get 返回非 0 表示服务未注册
    if [[ $rc -ne 0 ]]; then
        return 1
    fi

    # Token 为空表示服务已注册但未配置 Authorization
    if [[ -z "$token" ]]; then
        return 2
    fi

    return 0
}

# ── 将 Token 写入 mcporter 配置 ──────────────────────────────────────────────
# 用法：_save_token <token>
_save_token() {
    local token="$1"
    [[ -z "$token" ]] && return 1

    # 使用传入的 token 写入 mcporter 配置（ClawAgent）
    mcporter config add "$_CLAWAGENT_SERVICE_NAME" "$_CLAWAGENT_MCP_URL" \
        --header "Authorization=$token" \
        --transport http \
        --scope home 2>&1

    return $?
}

# ── 检查授权状态（立即返回）──────────────────────────────────────────────────
_check_auth() {
    if ! _check_mcporter; then
        echo "ERROR:mcporter_not_found"
        exit 1
    fi

    _check_service
    local status=$?

    case $status in
        0)
            echo "READY"
            return 0
            ;;
        1|2)
            echo "NOT_CONFIGURED"
            return 0
            ;;
    esac
}

# ── 保存用户提供的 Token ─────────────────────────────────────────────────────
_save_token_command() {
    local token="$1"

    if [[ -z "$token" ]]; then
        echo "ERROR:no_token - 请提供 Token"
        exit 1
    fi

    if ! _check_mcporter; then
        echo "ERROR:mcporter_not_found"
        exit 1
    fi

    echo "🔧 正在保存 Token..."
    if _save_token "$token"; then
        echo "TOKEN_SAVED"
        return 0
    else
        echo "ERROR:save_failed"
        return 1
    fi
}

# ── 验证 Token 是否有效 ──────────────────────────────────────────────────────
_verify_token() {
    if ! _check_mcporter; then
        echo "ERROR:mcporter_not_found"
        exit 1
    fi

    # 尝试调用 ClawAgent 工具列表来验证 Token
    local result
    result=$(mcporter list "$_CLAWAGENT_SERVICE_NAME" 2>&1)
    local exit_code=$?

    if [[ $exit_code -eq 0 ]] && [[ -n "$result" ]]; then
        echo "TOKEN_VALID"
        return 0
    else
        if echo "$result" | grep -q "400006\|token_invalid\|invalid"; then
            echo "ERROR:token_invalid"
        elif echo "$result" | grep -q "save\|config"; then
            echo "ERROR:save_failed"
        else
            echo "ERROR:token_invalid"
        fi
        return 1
    fi
}

# ── 直接执行时的交互式安装流程 ───────────────────────────────────────────────
_interactive_setup() {
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║     ClawAgentAgent 配置向导                   ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    # 检查 mcporter
    echo "🔍 检查 mcporter..."
    if ! _check_mcporter; then
        echo "❌ mcporter 安装失败，请先安装 Node.js (https://nodejs.org) 后重试"
        exit 1
    fi
    echo "✅ mcporter 已就绪"
    echo ""

    # 检查服务状态
    echo "🔍 检查 ClawAgent 服务配置..."
    _check_service
    local status=$?

    case $status in
        0)
            echo "✅ ClawAgent 服务已配置且运行正常！"
            echo ""
            echo "🎉 无需重新配置，您可以直接使用 ClawAgent功能。"
            echo ""
            echo "📖 使用示例："
            echo "   mcporter list ClawAgent"
            return 0
            ;;
        1|2)
            echo "⚠️  Token 未配置，需要授权..."
            ;;
    esac

    echo ""
    echo "─────────────────────────────────────────────"
    echo "🎉 基础设置完成！"
    echo ""
    echo "📖 下一步：配置ClawAgent Token"
    echo "   详见 SKILL.md 中快速配置说明"
    echo ""
    echo "   更多信息请查看 SKILL.md"
    echo ""
}

# ── 主入口 ────────────────────────────────────────────────────────────────────
case "${1:-}" in
    check_auth)
        _check_auth
        ;;
    save_token)
        _save_token_command "${2:-}"
        ;;
    verify_token)
        _verify_token
        ;;
    *)
        _interactive_setup
        ;;
esac
