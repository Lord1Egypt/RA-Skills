#!/bin/bash
# Hekouwang Terminal writes only these paths during a theme switch. Keep this list explicit.

hkw_transaction_paths() {
  local theme="$1" out="$2" bat_dir=""
  {
    printf '%s\n' "$ACTIVE" "$DP_DIR/catppuccin-mocha.json" "$RUNTIME/theme"
    printf '%s\n' "$AUTO_CONF" "$AGENT_PLIST"
    if [ -f "$THEMES_DIR/_apply_pro.sh" ]; then
      printf '%s\n' "$CURRENT"
      printf '%s\n' "$GHOSTTY_CFG" "$GHOSTTY_THEMES/hekouwang-$theme"
      printf '%s\n' "$WARP_THEMES/${theme//-/_}.yaml"
      printf '%s\n' "$HOME/.warp/settings.json" "$HOME/.warp/settings.toml"
      printf '%s\n' "$HOME/.config/cmux/cmux.json"
      printf '%s\n' "$HOME/Library/Application Support/tabby/config.yaml"
      printf '%s\n' "$HOME/Library/Preferences/com.apple.Terminal.plist"
      if command -v bat >/dev/null 2>&1; then
        bat_dir="$(bat --config-dir 2>/dev/null || true)"
        [ -n "$bat_dir" ] && printf '%s\n' "$bat_dir/themes/hekouwang-$theme.tmTheme"
      fi
    fi
  } > "$out"
}

hkw_transaction_snapshot() {
  local label="$1" theme="$2" list_file
  list_file="$(mktemp "${TMPDIR:-/tmp}/hkw-terminal-paths.XXXXXX")"
  hkw_transaction_paths "$theme" "$list_file"
  python3 "$SCRIPT_DIR/lib/transaction.py" snapshot --label "$label" --paths "$list_file"
  local rc=$?
  rm -f "$list_file"
  return "$rc"
}

hkw_transaction_plan() {
  local theme="$1" list_file
  list_file="$(mktemp "${TMPDIR:-/tmp}/hkw-terminal-paths.XXXXXX")"
  hkw_transaction_paths "$theme" "$list_file"
  python3 "$SCRIPT_DIR/lib/transaction.py" plan --paths "$list_file"
  local rc=$?
  rm -f "$list_file"
  return "$rc"
}

hkw_transaction_rollback() {
  python3 "$SCRIPT_DIR/lib/transaction.py" rollback "${1:-latest}"
}

hkw_transaction_history() {
  python3 "$SCRIPT_DIR/lib/transaction.py" history
}
