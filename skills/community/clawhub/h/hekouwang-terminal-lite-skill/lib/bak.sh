#!/bin/bash
# ============================================================
# Shared backup helpers for ~/.zshrc / ~/.zshrc.local
#
# Why a folder: install/migrate used to drop ~/.zshrc.bak.<ts> in $HOME,
# and after a few reinstalls the home root looked like a landfill.
#
# Path: ~/.hekouwang-terminal-backups/zshrc.bak.<ts>
# (Kept outside ~/.config/hekouwang-terminal/ so uninstall's rm -rf of the
#  runtime dir does not wipe restore history.)
# ============================================================

HKW_BAK_DIR="${HKW_BAK_DIR:-$HOME/.hekouwang-terminal-backups}"

hkw_bak_dir() {
  mkdir -p "$HKW_BAK_DIR"
  printf '%s\n' "$HKW_BAK_DIR"
}

# Copy $1 → backups/<stem>.bak.<timestamp>; print the new path.
# stem examples: zshrc / zshrc.local / zshrc.uninstall
hkw_bak_copy() {
  local src="$1" stem="$2" dest dir ts
  [ -f "$src" ] || return 1
  dir="$(hkw_bak_dir)"
  ts="$(date +%Y%m%d%H%M%S)"
  dest="$dir/${stem}.bak.$ts"
  cp "$src" "$dest"
  printf '%s\n' "$dest"
}

# One-time tidy: move legacy ~/.zshrc.bak.* (and .zshrc.local.bak.*) here.
# Renames ".zshrc.bak.TS" → "zshrc.bak.TS" so the folder listing is not all-dotfiles.
# Also sweeps an older mistaken path under ~/.config/hekouwang-terminal/backups/.
# ⚠️ 用 find 不用裸 glob：zsh 默认 nomatch，家目录没有旧 bak 时会直接报错退出。
hkw_bak_sweep_legacy() {
  local dir f base legacy_rt
  dir="$(hkw_bak_dir)"
  while IFS= read -r f; do
    [ -n "$f" ] && [ -f "$f" ] || continue
    base="$(basename "$f")"
    base="${base#.}"   # drop leading dot
    mv "$f" "$dir/$base" 2>/dev/null || true
  done <<EOF
$(find "$HOME" -maxdepth 1 \( -name '.zshrc.bak.*' -o -name '.zshrc.local.bak.*' -o -name '.zshrc.uninstall.bak' \) -type f -print 2>/dev/null)
EOF
  legacy_rt="${RUNTIME:-$HOME/.config/hekouwang-terminal}/backups"
  if [ -d "$legacy_rt" ]; then
    while IFS= read -r f; do
      [ -n "$f" ] && [ -f "$f" ] || continue
      mv "$f" "$dir/$(basename "$f")" 2>/dev/null || true
    done <<EOF
$(find "$legacy_rt" -maxdepth 1 -type f -print 2>/dev/null)
EOF
    rmdir "$legacy_rt" 2>/dev/null || true
  fi
}

# Latest zshrc backup: prefer this folder, fall back to legacy home-root files.
hkw_bak_latest_zshrc() {
  local latest="" dir
  dir="$(hkw_bak_dir)"
  latest="$(find "$dir" -maxdepth 1 \( -name 'zshrc.bak.*' -o -name '.zshrc.bak.*' \) -type f -print 2>/dev/null | sort | tail -1)"
  if [ -z "$latest" ]; then
    latest="$(find "$HOME" -maxdepth 1 -name '.zshrc.bak.*' -type f -print 2>/dev/null | sort | tail -1)"
  fi
  printf '%s\n' "$latest"
}
