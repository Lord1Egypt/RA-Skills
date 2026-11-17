#!/usr/bin/env bash
# _lib_profile.sh — 共享的开源身份读取函数
#
# ⚠️ 本文件设计为被 source 而非直接执行；故意不在文件级 `set -euo pipefail`
# （会污染 source 它的调用方 shell 行为）。各调用脚本自己负责开启严格模式。
# audit 工具的 set-e 检查在此豁免。
#
# 优先级（高 → 低）：
#   1. 函数参数显式传入（脚本调用方可覆盖）
#   2. OSG_* 环境变量（CI/CD / 临时覆盖）
#   3. ~/.config/opensource-skill-to-github/profile.env（持久化主载体，跨 agent）
#   4. git config --global user.name/user.email（兜底）
#   5. 首次缺失 → setup_profile.sh 引导
#
# Usage in other scripts:
#   set -euo pipefail
#   . "$(dirname "$0")/_lib_profile.sh"
#   osg_resolve_identity     # 加载 profile.env + git config 兜底
#   echo "$OSG_AUTHOR_NAME / $OSG_GITHUB_HANDLE / $OSG_AUTHOR_EMAIL"
#
# 函数不输出任何 stdout（除非 debug），可被静默 source。

# XDG 兼容：优先 XDG_CONFIG_HOME，回退 ~/.config
osg_profile_path() {
  local cfg="${XDG_CONFIG_HOME:-$HOME/.config}"
  echo "$cfg/opensource-skill-to-github/profile.env"
}

# 加载 profile.env（如存在），但不覆盖已设的 OSG_* 环境变量
load_osg_profile() {
  local profile
  profile="$(osg_profile_path)"
  if [[ -f "$profile" ]]; then
    # 只 source 安全字段（OSG_* 开头，简单 KEY=VALUE 行）
    while IFS='=' read -r key val; do
      [[ -z "$key" || "$key" =~ ^# ]] && continue
      [[ ! "$key" =~ ^OSG_[A-Z_]+$ ]] && continue
      # 不覆盖已存在的环境变量（优先级 2 > 3）
      if [[ -z "${!key:-}" ]]; then
        # 去掉首尾引号
        val="${val%\"}"
        val="${val#\"}"
        val="${val%\'}"
        val="${val#\'}"
        export "$key=$val"
      fi
    done < "$profile"
  fi
}

# 从 git config 兜底（只对未设的字段）
fallback_git_config() {
  if [[ -z "${OSG_AUTHOR_NAME:-}" ]]; then
    local gn
    gn="$(git config --global user.name 2>/dev/null || true)"
    [[ -n "$gn" ]] && export OSG_AUTHOR_NAME="$gn"
  fi
  if [[ -z "${OSG_AUTHOR_EMAIL:-}" ]]; then
    local ge
    ge="$(git config --global user.email 2>/dev/null || true)"
    [[ -n "$ge" ]] && export OSG_AUTHOR_EMAIL="$ge"
  fi
  # OSG_GITHUB_HANDLE 无 git config 兜底来源
}

# 完整加载：profile + git fallback
osg_resolve_identity() {
  load_osg_profile
  fallback_git_config
}

# 解析 GitHub push token。
#
# 优先级（高 → 低）：
#   1. GITHUB_TOKEN 环境变量（兼容 GitHub/Codex 常见写法）
#   2. OSG_GITHUB_TOKEN 环境变量或 profile.env（可选；明文 token，谨慎）
#   3. OSG_GITHUB_TOKEN_CMD 环境变量或 profile.env（推荐；命令 stdout 第一行返回 token）
#   4. gh auth token（如果已安装并登录 GitHub CLI）
#
# 成功时设置：
#   OSG_RESOLVED_GITHUB_TOKEN
#   OSG_RESOLVED_GITHUB_TOKEN_SOURCE
osg_resolve_github_token() {
  load_osg_profile
  OSG_RESOLVED_GITHUB_TOKEN=""
  OSG_RESOLVED_GITHUB_TOKEN_SOURCE=""

  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    OSG_RESOLVED_GITHUB_TOKEN="$GITHUB_TOKEN"
    OSG_RESOLVED_GITHUB_TOKEN_SOURCE="GITHUB_TOKEN"
    return 0
  fi

  if [[ -n "${OSG_GITHUB_TOKEN:-}" ]]; then
    OSG_RESOLVED_GITHUB_TOKEN="$OSG_GITHUB_TOKEN"
    OSG_RESOLVED_GITHUB_TOKEN_SOURCE="OSG_GITHUB_TOKEN"
    return 0
  fi

  if [[ -n "${OSG_GITHUB_TOKEN_CMD:-}" ]]; then
    local cmd_token
    cmd_token="$((sh -c "$OSG_GITHUB_TOKEN_CMD" 2>/dev/null || true) | awk 'NF {print; exit}' | tr -d '\r\n')"
    if [[ -n "$cmd_token" ]]; then
      OSG_RESOLVED_GITHUB_TOKEN="$cmd_token"
      OSG_RESOLVED_GITHUB_TOKEN_SOURCE="OSG_GITHUB_TOKEN_CMD"
      return 0
    fi
  fi

  if command -v gh >/dev/null 2>&1; then
    local gh_token
    gh_token="$((gh auth token 2>/dev/null || true) | awk 'NF {print; exit}' | tr -d '\r\n')"
    if [[ -n "$gh_token" ]]; then
      OSG_RESOLVED_GITHUB_TOKEN="$gh_token"
      OSG_RESOLVED_GITHUB_TOKEN_SOURCE="gh auth token"
      return 0
    fi
  fi

  return 1
}

# 检查必需字段，缺失时给清晰指引（exit 1）
require_osg_identity() {
  osg_resolve_identity
  local missing=()
  [[ -z "${OSG_AUTHOR_NAME:-}"   ]] && missing+=("OSG_AUTHOR_NAME")
  [[ -z "${OSG_GITHUB_HANDLE:-}" ]] && missing+=("OSG_GITHUB_HANDLE")
  [[ -z "${OSG_AUTHOR_EMAIL:-}"  ]] && missing+=("OSG_AUTHOR_EMAIL")
  if [[ ${#missing[@]} -gt 0 ]]; then
    local profile
    profile="$(osg_profile_path)"
    cat <<EOF >&2

❌ 缺少开源身份字段: ${missing[*]}

请用以下任一方式之一配置（推荐第一种，一次设置永久使用）：

  ① 跑首次引导脚本（推荐，写到 ${profile}）:
       bash $(dirname "${BASH_SOURCE[0]}")/setup_profile.sh

  ② 临时环境变量（仅当前 shell 生效）:
       export OSG_AUTHOR_NAME="Your Name"
       export OSG_GITHUB_HANDLE="your-handle"
       export OSG_AUTHOR_EMAIL="you@example.com"

  ③ 命令行参数显式传入（如脚本支持）

EOF
    return 1
  fi
  return 0
}
