#!/usr/bin/env bash
# _lib_exclude.sh — 发布前自动清理"不该进发布包"的派生产物
# 参考 skill-release-plus 的 config/exclude.json 排除机制，适配 osg 的 bash 脚本链。
#
# 用法（在 publish 类脚本里）：
#   . "$(dirname "$0")/_lib_exclude.sh"
#   osg_clean_fork "$FORK"
#
# 设计约束：
# - 默认清单只含【可再生的派生缓存产物】（pyc/__pycache__/.DS_Store 等），
#   物理删除绝对安全——它们由 py_compile / pytest / Finder 等随手生成，
#   典型坑：audit 阶段 py_compile 复活 __pycache__ → skillhub.cn 拒收 .pyc。
# - 源码/文档/LICENSE 等一律不动；目录类排除（tests/output）不在这里删，
#   由各 publish 脚本的文件收集白名单负责跳过。
# - 可选扩展：fork 根目录放 `.osg-exclude`（每行一个 find -name 模式，# 注释），
#   该文件本身不会被发布（publish 脚本已跳过）。
# - bash 3.2 兼容（无 mapfile / 无关联数组）。

osg_clean_fork() {
  local dir="${1:-}"
  [[ -n "$dir" && -d "$dir" ]] || return 0

  local removed=0 n d f

  # 目录类缓存（整目录删）
  for d in __pycache__ .pytest_cache .mypy_cache .ruff_cache .tox .hypothesis htmlcov; do
    n="$(find "$dir" -type d -name "$d" 2>/dev/null | wc -l | tr -d ' ')"
    [[ "$n" -gt 0 ]] && removed=$((removed + n))
    find "$dir" -type d -name "$d" -exec rm -rf {} + 2>/dev/null || true
  done

  # 文件类缓存
  for f in '*.pyc' '*.pyo' '.DS_Store' '._.DS_Store' 'Thumbs.db' '.coverage'; do
    n="$(find "$dir" -type f -name "$f" 2>/dev/null | wc -l | tr -d ' ')"
    [[ "$n" -gt 0 ]] && removed=$((removed + n))
    find "$dir" -type f -name "$f" -delete 2>/dev/null || true
  done

  # 用户自定义追加模式（可选）
  if [[ -f "$dir/.osg-exclude" ]]; then
    local pat
    while IFS= read -r pat || [[ -n "$pat" ]]; do
      pat="${pat%%#*}"
      # trim 首尾空白
      pat="$(printf '%s' "$pat" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
      [[ -z "$pat" ]] && continue
      # 防呆：拒绝会误伤源码的过宽模式
      case "$pat" in
        '*'|'*.*'|'.'|'..'|'/'|'*.py'|'*.md'|'*.sh'|SKILL.md|LICENSE|README.md)
          echo "⚠️  .osg-exclude 忽略危险模式: $pat" >&2
          continue ;;
      esac
      n="$(find "$dir" -name "$pat" 2>/dev/null | wc -l | tr -d ' ')"
      [[ "$n" -gt 0 ]] && removed=$((removed + n))
      find "$dir" -name "$pat" -exec rm -rf {} + 2>/dev/null || true
    done < "$dir/.osg-exclude"
  fi

  if [[ "$removed" -gt 0 ]]; then
    echo "🧹 已清理 $removed 个缓存/派生产物（__pycache__/*.pyc/.DS_Store 等）"
  fi
  return 0
}
