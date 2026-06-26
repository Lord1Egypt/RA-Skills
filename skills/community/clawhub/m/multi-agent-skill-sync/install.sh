#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_name="skill-sync"

declare -a targets=()
mode="link"
force="false"

usage() {
  cat <<'EOF'
Install skill-sync into local AI agent skill directories.

Usage:
  ./install.sh [options]

Targets:
  --codex       Install into ~/.codex/skills
  --agents      Install into ~/.agents/skills
  --claude      Install into ~/.claude/skills
  --opencode    Install into ~/.config/opencode/skills
  --openclaw    Install into ~/.openclaw/skills
  --all         Install into all primary targets above

Options:
  --copy        Copy files instead of creating a symlink
  --force       Replace an existing destination
  --help        Show this help

Examples:
  ./install.sh --codex
  ./install.sh --codex --claude --openclaw
  ./install.sh --all
  ./install.sh --codex --copy
EOF
}

append_target() {
  local name="$1"
  for existing in "${targets[@]:-}"; do
    if [[ "$existing" == "$name" ]]; then
      return 0
    fi
  done
  targets+=("$name")
}

target_root() {
  case "$1" in
    codex) printf '%s\n' "${HOME}/.codex/skills" ;;
    agents) printf '%s\n' "${HOME}/.agents/skills" ;;
    claude) printf '%s\n' "${HOME}/.claude/skills" ;;
    opencode) printf '%s\n' "${HOME}/.config/opencode/skills" ;;
    openclaw) printf '%s\n' "${HOME}/.openclaw/skills" ;;
    *)
      printf 'Unknown target: %s\n' "$1" >&2
      exit 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --codex) append_target "codex" ;;
    --agents) append_target "agents" ;;
    --claude) append_target "claude" ;;
    --opencode) append_target "opencode" ;;
    --openclaw) append_target "openclaw" ;;
    --all)
      append_target "codex"
      append_target "agents"
      append_target "claude"
      append_target "opencode"
      append_target "openclaw"
      ;;
    --copy) mode="copy" ;;
    --force) force="true" ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

if [[ ${#targets[@]} -eq 0 ]]; then
  printf 'No install target selected.\n\n' >&2
  usage >&2
  exit 1
fi

for target in "${targets[@]}"; do
  root="$(target_root "$target")"
  destination="${root}/${skill_name}"

  mkdir -p "$root"

  if [[ -L "$destination" || -e "$destination" ]]; then
    if [[ "$force" != "true" ]]; then
      printf 'Skip %s: %s already exists (use --force to replace)\n' "$target" "$destination"
      continue
    fi
    rm -rf "$destination"
  fi

  if [[ "$mode" == "copy" ]]; then
    cp -R "$repo_root" "$destination"
    printf 'Copied to %s: %s\n' "$target" "$destination"
  else
    ln -s "$repo_root" "$destination"
    printf 'Linked to %s: %s -> %s\n' "$target" "$destination" "$repo_root"
  fi
done
