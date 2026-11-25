#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — pick / switch the Node version manager
#
# ⚠️ 对外文案在 lib/i18n/{en,zh}/node-mgr.sh。这里只留逻辑。
#
# Only one of: fnm · nvm · brew node · vfox.
# Writes ~/.config/hekouwang-terminal/{node-manager,node.sh};
# ~/.zshrc sources node.sh (template block 4).
# ============================================================
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$HOME/.config/hekouwang-terminal"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init node-mgr "$@"
eval set -- "$HKW_ARGS"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/node-mgr.sh"

say()  { printf "\033[1;35m%s\033[0m\n" "$(t "$@")"; }
dim()  { printf "\033[2m  %s\033[0m\n" "$(t "$@")"; }
info() { printf "  %s\n" "$(t "$@")"; }

brew_ensure() {
  local pkg="$1"
  [ -n "$pkg" ] || return 0
  if ! command -v brew >/dev/null 2>&1; then
    info M_NODE_NO_BREW "$pkg"
    return 0
  fi
  if brew list --formula "$pkg" >/dev/null 2>&1; then
    info M_NODE_PKG_SKIP "$pkg"
    return 0
  fi
  say M_NODE_PKG_INSTALL "$pkg"
  if brew install "$pkg"; then
    info M_NODE_PKG_OK "$pkg"
  else
    info M_NODE_PKG_FAIL "$pkg"
  fi
}

show_status() {
  local cur=""
  cur="$(hkw_node_read_saved 2>/dev/null || true)"
  printf "\n"
  if [ -n "$cur" ]; then
    say M_NODE_CURRENT "$cur"
  else
    say M_NODE_NONE
  fi
  dim M_NODE_CHOICES
  dim M_NODE_HOW
  dim M_NODE_RULE
  echo
}

apply_choice() {
  local id raw="$1" pkg
  id="$(hkw_node_normalize "$raw")"
  if [ -z "$id" ]; then
    printf "\033[1;35m%s\033[0m\n" "$(t M_NODE_BAD "$raw")"
    dim M_NODE_CHOICES
    exit 1
  fi
  pkg="$(hkw_node_brew_pkg "$id")"
  brew_ensure "$pkg"
  # nvm via brew still needs NVM_DIR; curl-installed nvm is fine as-is
  if [ "$id" = "nvm" ] && [ ! -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ] \
     && ! [ -s "${HOMEBREW_PREFIX:-/opt/homebrew}/opt/nvm/nvm.sh" ] \
     && ! [ -s /usr/local/opt/nvm/nvm.sh ]; then
    info M_NODE_NVM_HINT
  fi
  if [ "$id" = "vfox" ]; then
    info M_NODE_VFOX_HINT
  fi
  hkw_node_write "$id" || { printf "%s\n" "$(t M_NODE_WRITE_FAIL)"; exit 1; }
  if [ -f "$HOME/.zshrc" ] && ! grep -q 'hekouwang-terminal/node.sh' "$HOME/.zshrc" 2>/dev/null; then
    info M_NODE_ZSHRC_HINT
  fi
  say M_NODE_DONE "$id"
  dim M_NODE_REOPEN
  echo
}

case "${1:-}" in
  ""|-h|--help|status|--status)
    [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ] && { blk_node_help; exit 0; }
    show_status
    ;;
  *)
    apply_choice "$1"
    ;;
esac
