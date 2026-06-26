#!/bin/bash
# kb-scope.sh — KB 作用域解析公共库（source 使用）
#
# 设计：
# - scope=agent（默认）：per-agent 隔离 KB，数据在 $AGENT_DIR/kb/
# - scope=shared：跨 agent 共享 KB，数据在 ~/.openclaw/kb/shared/
#
# 用法（在 kb-* 脚本里）：
#   SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
#   source "$SCRIPT_DIR/kb-scope.sh"
#   kb_parse_scope "$@"
#   set -- "${KB_ARGS[@]}"   # 恢复剩余参数
#
# 副作用：
#   KB_SCOPE       = agent | shared
#   KB_DATA_DIR    = $AGENT_DIR/kb 或 ~/.openclaw/kb/shared
#   AGENT_DIR      = $HOME/.openclaw/agents/<id>/agent（shared scope 下仍会推断）
#   KB_ARGS=()     = 除 --scope/--shared 外的剩余参数

kb_resolve_agent_dir() {
  if [ -n "$AGENT_DIR" ]; then return 0; fi
  if [[ "$PWD" =~ agents/([^/]+)/ ]]; then
    AGENT_DIR="$HOME/.openclaw/agents/${BASH_REMATCH[1]}/agent"
  else
    AGENT_DIR="$HOME/.openclaw/agents/main/agent"
  fi
}

kb_parse_scope() {
  local scope="${KB_SCOPE:-agent}"
  local explicit="${KB_SCOPE_EXPLICIT:-0}"
  KB_ARGS=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --scope)
        scope="$2"; explicit=1; shift 2 ;;
      --scope=*)
        scope="${1#--scope=}"; explicit=1; shift ;;
      --shared)
        scope="shared"; explicit=1; shift ;;
      --agent-scope)
        scope="agent"; explicit=1; shift ;;
      *)
        KB_ARGS+=("$1"); shift ;;
    esac
  done

  kb_resolve_agent_dir

  case "$scope" in
    shared)
      KB_DATA_DIR="$HOME/.openclaw/kb/shared"
      ;;
    agent)
      KB_DATA_DIR="$AGENT_DIR/kb"
      ;;
    *)
      echo "❌ 未知 --scope: $scope（支持: agent | shared）" >&2
      return 1
      ;;
  esac

  KB_SCOPE="$scope"
  KB_SCOPE_EXPLICIT="$explicit"
  export KB_SCOPE KB_SCOPE_EXPLICIT KB_DATA_DIR AGENT_DIR
}

# 返回所有已初始化 scope 的数据目录（用于 kb-search 跨域搜索）
# 输出格式: "<scope>\t<dir>"，逐行
kb_list_initialized_scopes() {
  kb_resolve_agent_dir
  local agent_kb="$AGENT_DIR/kb"
  local shared_kb="$HOME/.openclaw/kb/shared"
  [ -d "$agent_kb/wiki" ] && printf "agent\t%s\n" "$agent_kb"
  [ -d "$shared_kb/wiki" ] && printf "shared\t%s\n" "$shared_kb"
}

# 确保 scope 对应目录存在（raw/wiki/cache），首次使用自动创建
kb_ensure_scope_dirs() {
  local dir="${1:-$KB_DATA_DIR}"
  mkdir -p "$dir/raw" "$dir/wiki" "$dir/cache"
  touch "$dir/raw/.gitkeep" "$dir/wiki/.gitkeep" "$dir/cache/.gitkeep"
}
