#!/bin/bash
# 词条表 · 英文 · theme.sh（换肤 / 画廊 / 预览 / 跟随系统深浅色）
#
# ⚠️ 回执那几行是「颜色 + 文字」拼出来的。颜色转义**不要**写进词条值里 ——
#    词条表在颜色变量定义之前就被 source 了，写进去只会是空串；
#    而且译者改一行文案要连着 \033[2m 一起抄，迟早抄错。
#    做法是：格式串留在 theme.sh 里带颜色，词条只出纯文字，用 %s 塞进去。

blk_theme_help() {
  cat <<'EOF'
hekouwang-terminal-skill — switch theme (terminal + the whole tool chain)

Usage:
  ./scripts/theme.sh                      with fzf: fuzzy pick + ANSI preview pane; else gallery
  ./scripts/theme.sh --pick               force fzf picker (falls back to gallery if no fzf)
  ./scripts/theme.sh --list               gallery only, no fzf
  ./scripts/theme.sh ember             switch to a theme
  ./scripts/theme.sh ember --p3        switch + Display P3 wide gamut (iTerm2 + Ghostty)
  ./scripts/theme.sh ember --plain     switch + drop eza icons in every terminal (no Nerd Font)
  ./scripts/theme.sh --preview ember   full preview of one theme (prompt / file list / git diff / syntax / log colors)
  ./scripts/theme.sh --gallery            full preview of every theme, one after another
  ./scripts/theme.sh --plan ember      show the managed files before writing anything
  ./scripts/theme.sh --rollback           restore the latest pre-switch snapshot
  ./scripts/theme.sh --history            list the five retained snapshots
  ./scripts/theme.sh --audit              palette audit: contrast floors / bright split / dim slot
  ./scripts/theme.sh --lang zh            run in Chinese

One command switches more than the terminal background: bat / fzf / eza /
delta (git diff) / tmux / Ghostty / Warp / cmux / Tabby / VS Code all come from the same
palette, so they can never drift apart.
EOF
}

M_THEME_LIST_TITLE="Available themes:"
M_THEME_CURRENT="← current"
M_THEME_TONE_DARK="dark"
M_THEME_TONE_LIGHT="light"
M_THEME_HINT_SWITCH="switch "
M_THEME_HINT_PREVIEW="    full preview "
M_THEME_HINT_GALLERY="    every theme "
M_THEME_HINT_PICK="fuzzy pick "
M_THEME_HINT_PICK_HOW="(when fzf is installed; ANSI preview on the right)"
M_THEME_PICK_PROMPT="theme ›"
M_THEME_PICK_HEADER="current: %s   Enter apply · Ctrl+/ toggle preview · Esc cancel"
M_THEME_PICK_NO_FZF="fzf not found — showing gallery. Install: brew install fzf"
M_THEME_PICK_NO_TTY="not a tty — showing gallery"
M_THEME_PICK_ABORT="cancelled; theme unchanged"

M_THEME_PREVIEW_WHICH="✗ Preview which one?"
M_THEME_PREVIEW_FAIL="✗ Preview renderer failed"
M_THEME_PREVIEW_NEED="  Needs python3 and config/themes/%s.json (run python3 _generate.py first)"

M_THEME_NO_SUCH="✗ No theme called '%s'"
M_THEME_TX_SNAPSHOT="Safety snapshot: %s"
M_THEME_TX_SNAPSHOT_FAIL="✗ Could not create the safety snapshot; nothing was changed"
M_THEME_TX_APPLY_FAIL="✗ Theme apply failed"
M_THEME_TX_AUTO_ROLLBACK="Restored the pre-switch snapshot automatically"
M_THEME_TX_ROLLBACK_FAIL="Automatic rollback failed; snapshot: %s"
M_THEME_PLAN_HEAD="Change plan for %s"
M_THEME_PLAN_NOTE="Read-only plan. Run ./scripts/theme.sh <name> to apply it."
M_THEME_ROLLBACK_OK="✓ Restored snapshot %s"
M_THEME_ROLLBACK_NOTE="Open a new tab; Ghostty may also need Cmd+Shift+,"
M_THEME_ROLLBACK_NONE="✗ No usable snapshot found"
M_THEME_SEC_TERMINAL="Terminal"
M_THEME_SEC_MULTI="Other terminals"
M_THEME_SEC_TOOLCHAIN="Tool chain"
M_THEME_ITERM_FONT="font %s"
M_THEME_ITERM_NOTE="Live on save; in windows that are already open, press Cmd+T for a new tab to see it"
M_THEME_MULTI_ITEMS="Ghostty / Warp / cmux / Tabby / macOS Terminal"
M_THEME_PAID_ONLY="paid pack"
M_THEME_ECO_ITEMS="bat / fzf / eza / git diff / tmux"
M_THEME_ECO_SAME="same colors"
M_THEME_ECO_NOTE="Apply to this shell right now: source ~/.config/hekouwang-terminal/current/colors.sh"
M_THEME_ECO_TMUX="tmux reloaded"
M_THEME_ECO_DEFAULT="left on their own default colors"
M_THEME_ECO_PAID_NOTE="One palette driving the whole tool chain is a paid-pack feature; the open-source build syncs iTerm2 only"
M_THEME_WS_OK="Project workspace variants"
M_THEME_WS_REBUILT="rebuilt along with it"
M_THEME_SEE_IT="See what this theme looks like:"
# Printed only when the paid pack is absent — the receipt above already says those
# rows were skipped, this is the one line that says where to get them. %s = landing page.
M_THEME_PAID_WHERE="Make this palette walk out of iTerm2: %s"

M_THEME_NO_LIGHT="✗ No light theme available"
M_THEME_NO_LIGHT_NOTE1="  The light themes (parchment / ledger) live in the paid pack;"
M_THEME_NO_LIGHT_NOTE2="  you can also add your own palette with light=True in config/themes/palettes/."

# ---- 付费半边（config/themes/_apply_pro.sh，被 theme.sh 的 apply() source 进去）----
M_THEME_PRO_BAT_CACHE="  First run on this theme — building bat's cache (a few seconds)…"
M_THEME_PRO_GHOSTTY_NOTE="No auto-reload — press Cmd+Shift+, in Ghostty"
M_THEME_PRO_GHOSTTY_PAID="multi-terminal sync is a paid-pack feature, the open-source build handles iTerm2 only"
M_THEME_PRO_GHOSTTY_ABSENT="not installed on this Mac, or never configured"
M_THEME_PRO_WARP_NOTE="settings.toml updated; restart Warp if nothing changed"
M_THEME_PRO_WARP_FAIL="could not rewrite settings.toml — the theme file is in place but Warp did not switch"
M_THEME_PRO_WARP_MANUAL="no ~/.warp/settings.toml found; pick it once in Settings → Appearance"
M_THEME_PRO_APPLE="macOS Terminal"
M_THEME_PRO_APPLE_PAID="multi-terminal sync is a paid-pack feature"
M_THEME_PRO_APPLE_INSIDE="this script is running inside it — changes get overwritten when it quits"
M_THEME_PRO_APPLE_INSIDE_NOTE="run ./scripts/theme.sh %s from another terminal to sync it"
M_THEME_PRO_APPLE_ICONS="policy icons: it supports one font only, so it gets the one with Nerd icons built in"
M_THEME_PRO_APPLE_ICONS2="want %s here too? set APPLE_TERMINAL_FONT=match in config/font.conf"
M_THEME_PRO_APPLE_MATCH="policy match: same font as everywhere else; that font has no Nerd icons, so ls shows none here (not a bug)"
M_THEME_PRO_APPLE_RUNNING="⚠ macOS Terminal is open — it overwrites these settings when it quits, so Cmd+Q it fully and reopen"
M_THEME_PRO_APPLE_NEXT="live next time you open it (set as the default profile)"
M_THEME_PRO_APPLE_FAIL="sync failed (other terminals unaffected)"
