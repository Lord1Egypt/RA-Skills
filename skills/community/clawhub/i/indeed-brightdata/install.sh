#!/usr/bin/env bash
set -euo pipefail

# install.sh — Install indeed-brightdata skill for supported AI coding platforms.

# Constants
readonly SKILL_NAME="indeed-brightdata"
readonly REQUIRED_BINS=("curl" "jq")
readonly MIN_BASH_VERSION=4
readonly SYMLINK_PLATFORMS=("claude-code" "cursor" "codex" "openclaw")

PROJECT_ROOT=""
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT

FORCE=false

# Platform directory map (populated in init_platform_dirs, after bash 4+ check)
init_platform_dirs() {
  declare -gA PLATFORM_DIRS
  PLATFORM_DIRS=(
    [claude-code]="${HOME}/.claude/skills"
    [cursor]="${HOME}/.cursor/skills"
    [codex]="${HOME}/.codex/skills"
    [openclaw]="${HOME}/.openclaw/skills"
  )
}

show_help() {
  cat >&2 <<EOF
Usage: $(basename "$0") [OPTIONS]

Install the $SKILL_NAME skill for AI coding platforms.

Options:
  --help                Show this help message and exit
  --platform <name>     Install for a specific platform
                        Platforms: claude-code, cursor, codex, openclaw, claude-desktop
  --all                 Install for all platforms
  --force               Overwrite existing installation

Examples:
  $(basename "$0") --platform claude-code
  $(basename "$0") --all
  $(basename "$0") --platform claude-code --force
EOF
}

check_deps() {
  for bin in "${REQUIRED_BINS[@]}"; do
    if ! command -v "$bin" >/dev/null 2>&1; then
      echo "Error: required dependency '$bin' not found in PATH." >&2
      echo "Install $bin and try again." >&2
      return 1
    fi
  done

  if [[ "${BASH_VERSINFO[0]}" -lt "$MIN_BASH_VERSION" ]]; then
    echo "Error: bash version $MIN_BASH_VERSION+ required (found ${BASH_VERSION})." >&2
    return 1
  fi
}

check_api_key() {
  if [[ -n "${BRIGHTDATA_API_KEY:-}" ]]; then
    echo "API key detected in environment." >&2
  else
    echo "Note: BRIGHTDATA_API_KEY is not set." >&2
    echo "Set it before using the skill:" >&2
    echo "  export BRIGHTDATA_API_KEY=\"your-key-here\"" >&2
  fi
}

install_symlink() {
  local platform_name="$1"
  local target_dir="$2"
  local install_path="$target_dir/$SKILL_NAME"

  if [[ -e "$install_path" && "$FORCE" != true ]]; then
    echo "Installation already exists at $install_path — skipping." >&2
    echo "Use --force to overwrite." >&2
    return 0
  fi

  if [[ -L "$install_path" ]]; then
    rm -f "$install_path"
  elif [[ -d "$install_path" ]]; then
    echo "Warning: replacing directory at $install_path" >&2
    rm -rf "$install_path"
  elif [[ -e "$install_path" ]]; then
    rm -f "$install_path"
  fi

  mkdir -p "$target_dir"
  ln -s "$PROJECT_ROOT" "$install_path"
  echo "Installed $SKILL_NAME for $platform_name at $install_path" >&2
}

install_desktop() {
  local package_script="$PROJECT_ROOT/scripts/package.sh"
  if [[ ! -x "$package_script" ]]; then
    echo "Error: scripts/package.sh not found or not executable." >&2
    return 1
  fi
  "$package_script"
  echo "" >&2
  echo "Upload indeed-brightdata.zip via Claude Desktop:" >&2
  echo "  Settings > Features > Skills > Upload skill" >&2
}

install_platform() {
  local platform="$1"

  if [[ "$platform" == "claude-desktop" ]]; then
    install_desktop
    return 0
  fi

  if [[ -z "${PLATFORM_DIRS[$platform]+x}" ]]; then
    echo "Error: unknown platform '$platform'." >&2
    echo "Supported platforms: ${SYMLINK_PLATFORMS[*]}, openclaw, claude-desktop" >&2
    return 1
  fi

  install_symlink "$platform" "${PLATFORM_DIRS[$platform]}"
}

install_all() {
  for platform in "${SYMLINK_PLATFORMS[@]}"; do
    install_symlink "$platform" "${PLATFORM_DIRS[$platform]}"
  done
  echo "" >&2
  install_desktop
}

main() {
  init_platform_dirs

  local platform=""
  local do_all=false

  if [[ $# -eq 0 ]]; then
    show_help
    exit 0
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help)
        show_help
        exit 0
        ;;
      --platform)
        platform="${2:?Error: --platform requires a value}"
        shift 2
        ;;
      --all)
        do_all=true
        shift
        ;;
      --force)
        FORCE=true
        shift
        ;;
      *)
        echo "Error: unknown option '$1'" >&2
        show_help
        exit 1
        ;;
    esac
  done

  check_deps
  check_api_key

  if [[ "$do_all" == true ]]; then
    install_all
  elif [[ -n "$platform" ]]; then
    install_platform "$platform"
  else
    show_help
    exit 0
  fi
}

main "$@"
