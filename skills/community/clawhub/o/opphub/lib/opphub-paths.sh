#!/usr/bin/env bash
# 偶合 OppHub · 路径解析（兼容各种机器/容器/K8s 环境）
# 用法：source "$(dirname "${BASH_SOURCE[0]}")/lib/opphub-paths.sh"
#
# 解析顺序（命中即返回）：
#   1. $OPPHUB_HOME         用户显式指定（推荐，最优先）
#   2. $XDG_STATE_HOME/opphub  桌面 Linux 符合 XDG Base Dir
#   3. $OPPHUB_DATA_DIR     容器/K8s 专用（只读 rootfs 友好）
#   4. $HOME/.opphub        传统兜底
#   5. /tmp/opphub-$UID     无 HOME 时的最后兜底
#
# 解析后会把：
#   OPPHUB_HOME            解析出的绝对路径
#   OPPHUB_BIN_DIR         $OPPHUB_HOME/bin
#   OPPHUB_CONFIG_DIR      $OPPHUB_HOME/config
#   OPPHUB_LOG_DIR         $OPPHUB_HOME/logs
#   OPPHUB_RESOLVED_FROM   命中第几条规则（debug 用）
#
# 调用 opphub_init_home 后才会建目录 + 写日志。

# 调试开关：export OPPHUB_DEBUG=1 看解析过程
_opphub_log_path() {
  if [ "${OPPHUB_DEBUG:-0}" = "1" ]; then
    echo "[opphub-paths] $*" >&2
  fi
}

_opphub_is_writable() {
  local d="$1"
  # 目录存在且可写
  [ -d "$d" ] && [ -w "$d" ] && return 0
  # 父目录存在且可写（可创建）
  local parent
  parent="$(dirname "$d")"
  [ -d "$parent" ] && [ -w "$parent" ] && return 0
  return 1
}

# 解析 OPPHUB_HOME，不创建目录
opphub_resolve_home() {
  # 1. 用户显式指定
  if [ -n "${OPPHUB_HOME:-}" ]; then
    _opphub_log_path "命中规则1: OPPHUB_HOME=$OPPHUB_HOME (用户指定)"
    echo "$OPPHUB_HOME"
    return 0
  fi

  # 2. XDG Base Dir
  if [ -n "${XDG_STATE_HOME:-}" ]; then
    _opphub_log_path "命中规则2: XDG_STATE_HOME=$XDG_STATE_HOME/opphub"
    echo "$XDG_STATE_HOME/opphub"
    return 0
  fi

  # 3. 容器 / K8s 专用
  if [ -n "${OPPHUB_DATA_DIR:-}" ]; then
    _opphub_log_path "命中规则3: OPPHUB_DATA_DIR=$OPPHUB_DATA_DIR"
    echo "$OPPHUB_DATA_DIR"
    return 0
  fi

  # 4. 传统 HOME
  if [ -n "${HOME:-}" ] && _opphub_is_writable "$HOME"; then
    _opphub_log_path "命中规则4: HOME=$HOME/.opphub"
    echo "$HOME/.opphub"
    return 0
  fi

  # 5. 最后兜底（无 HOME / HOME 不可写）
  local uid="${UID:-$(id -u 2>/dev/null || echo 0)}"
  _opphub_log_path "命中规则5: /tmp/opphub-$uid (无 HOME 或 HOME 不可写)"
  echo "/tmp/opphub-$uid"
}

# 初始化：解析 + 建目录 + 派生 bin/config/log 路径
# 用法：opphub_init_home
opphub_init_home() {
  OPPHUB_HOME="$(opphub_resolve_home)"

  if [ -z "$OPPHUB_HOME" ]; then
    echo "[opphub] 错误：无法解析状态目录" >&2
    return 1
  fi

  # 建目录（不会重复建）
  mkdir -p "$OPPHUB_HOME" "$OPPHUB_HOME/bin" "$OPPHUB_HOME/config" "$OPPHUB_HOME/logs" 2>/dev/null || {
    echo "[opphub] 错误：无法创建 $OPPHUB_HOME（权限不足？）" >&2
    return 1
  }

  # 派生路径
  OPPHUB_BIN_DIR="$OPPHUB_HOME/bin"
  OPPHUB_CONFIG_DIR="$OPPHUB_HOME/config"
  OPPHUB_LOG_DIR="$OPPHUB_HOME/logs"

  export OPPHUB_HOME OPPHUB_BIN_DIR OPPHUB_CONFIG_DIR OPPHUB_LOG_DIR

  if [ "${OPPHUB_DEBUG:-0}" = "1" ]; then
    echo "[opphub] state dir:  $OPPHUB_HOME" >&2
    echo "[opphub] bin dir:    $OPPHUB_BIN_DIR" >&2
    echo "[opphub] config dir: $OPPHUB_CONFIG_DIR" >&2
    echo "[opphub] log dir:    $OPPHUB_LOG_DIR" >&2
  fi
}

# 兼容旧调用：如果调用方只设了 OPPHUB_HOME 但没初始化，照样能用
if [ -n "${OPPHUB_HOME:-}" ] && [ -z "${OPPHUB_BIN_DIR:-}" ]; then
  OPPHUB_BIN_DIR="$OPPHUB_HOME/bin"
  OPPHUB_CONFIG_DIR="$OPPHUB_HOME/config"
  OPPHUB_LOG_DIR="$OPPHUB_HOME/logs"
  export OPPHUB_BIN_DIR OPPHUB_CONFIG_DIR OPPHUB_LOG_DIR
fi
