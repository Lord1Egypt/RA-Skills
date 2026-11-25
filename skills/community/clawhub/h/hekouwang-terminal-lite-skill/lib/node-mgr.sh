#!/bin/bash
# ============================================================
# Shared Node-manager helpers (sourced by install.sh / node-mgr.sh).
# Choice is persisted in ~/.config/hekouwang-terminal/node-manager;
# the live shell snippet is ~/.config/hekouwang-terminal/node.sh
# (sourced from the zshrc template). Only one manager at a time.
# ============================================================

# Caller must set SCRIPT_DIR and RUNTIME before sourcing.
HKW_NODE_CHOICES="fnm nvm brew vfox"
HKW_NODE_DEFAULT="fnm"

hkw_node_normalize() {
  case "$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')" in
    fnm|fast)           echo fnm ;;
    nvm)                echo nvm ;;
    brew|brew-node|node) echo brew ;;
    vfox|version-fox|versionfox) echo vfox ;;
    *)                  echo "" ;;
  esac
}

hkw_node_snip_src() {
  local id="$1"
  echo "$SCRIPT_DIR/config/node/${id}.sh"
}

hkw_node_read_saved() {
  local f="$RUNTIME/node-manager" v=""
  [ -f "$f" ] || return 1
  v="$(hkw_node_normalize "$(head -1 "$f" 2>/dev/null)")"
  [ -n "$v" ] || return 1
  printf '%s\n' "$v"
}

hkw_node_brew_pkg() {
  case "$1" in
    fnm)  echo fnm ;;
    nvm)  echo nvm ;;
    brew) echo node ;;
    vfox) echo vfox ;;
    *)    echo "" ;;
  esac
}

# Write node-manager + node.sh. Does not brew-install (caller does that).
hkw_node_write() {
  local id="$1" src dest="$RUNTIME/node.sh"
  id="$(hkw_node_normalize "$id")"
  [ -n "$id" ] || return 1
  src="$(hkw_node_snip_src "$id")"
  [ -f "$src" ] || return 1
  mkdir -p "$RUNTIME"
  printf '%s\n' "$id" > "$RUNTIME/node-manager"
  # Header so doctor / humans know it is generated
  {
    echo "# hekouwang-terminal-skill · Node manager snippet (do not edit by hand)"
    echo "# Active: $id    Switch: ./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
    echo "#"
    cat "$src"
  } > "$dest"
}
