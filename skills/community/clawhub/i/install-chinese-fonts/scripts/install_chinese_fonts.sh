#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
VERIFY_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --verify-only) VERIFY_ONLY=1 ;;
    -h|--help)
      cat <<'EOF'
Usage: install_chinese_fonts.sh [--dry-run] [--verify-only]

Install Chinese/CJK fonts using the host package manager, then refresh and verify fontconfig.

Options:
  --dry-run      Show planned commands without executing them
  --verify-only  Skip installation; only show current CJK font status
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run]'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

show_current_fonts() {
  echo '=== current zh fonts ==='
  fc-list :lang=zh family file | head -20 || true
  echo
  echo '=== current CJK families ==='
  fc-list | grep -Ei 'Noto Sans CJK|Noto Serif CJK|Source Han Sans|Source Han Serif' | head -40 || true
}

pick_pkg_manager() {
  if command -v dnf >/dev/null 2>&1; then
    echo dnf
  elif command -v yum >/dev/null 2>&1; then
    echo yum
  elif command -v apt-get >/dev/null 2>&1; then
    echo apt-get
  else
    echo none
  fi
}

install_with_dnf_like() {
  local pm="$1"
  run "$pm" -y install \
    google-noto-cjk-fonts \
    google-noto-sans-cjk-ttc-fonts \
    google-noto-serif-cjk-ttc-fonts
}

install_with_apt() {
  run apt-get update
  run apt-get install -y fonts-noto-cjk
}

main() {
  local pm
  pm="$(pick_pkg_manager)"

  show_current_fonts

  if [[ "$VERIFY_ONLY" -eq 1 ]]; then
    exit 0
  fi

  case "$pm" in
    dnf|yum)
      install_with_dnf_like "$pm"
      ;;
    apt-get)
      install_with_apt
      ;;
    none)
      echo 'No supported package manager found. Fall back to manual font installation.' >&2
      exit 3
      ;;
  esac

  run fc-cache -f

  echo
  echo '=== verify after install ==='
  fc-list | grep -Ei 'Noto Sans CJK|Noto Serif CJK|Source Han Sans|Source Han Serif' | head -40 || true
}

main "$@"
