#!/bin/bash
# 词条表 · 英文 · install.sh
# ⚠️ 值里的 % 一律写 %%（整串走 printf 格式串）。

# ---- 长块：help / dry-run 清单 ----------------------------------
# 这两块以前是「打印脚本自己的头部注释」（sed -n '3,13p' $0）。
# 双语之后那条路走不通了，正文搬到这里 —— 一个语言一份、单一同源，-h 和文档不会漂。
blk_install_help() {
  cat <<'EOF'
hekouwang-terminal-skill — one-shot install

Usage:
  ./scripts/install.sh              install everything
  ./scripts/install.sh --dry-run    list every file and setting it would touch, write nothing
  ./scripts/install.sh --lang zh    run in Chinese (remembered for later runs)
  ./scripts/install.sh --node fnm   pick a Node manager: fnm / nvm / brew / vfox (remembered)
  CN=1 ./scripts/install.sh         use China mirrors (Tsinghua TUNA) end to end

Idempotent: safe to re-run, anything already installed is skipped.
Your ~/.zshrc is backed up under ~/.hekouwang-terminal-backups/ before it gets replaced.
Already using your own .zshrc? Run ./scripts/migrate.sh first — it moves your aliases /
PATH / env vars into ~/.zshrc.local instead of overwriting them.
Changed your mind: ./scripts/uninstall.sh (restores .zshrc, resets the GUI settings)
EOF
}

M_INSTALL_DRY_HEAD="═══ DRY-RUN — nothing below is actually executed ═══"
M_INSTALL_DRY_TAIL="Drop --dry-run to run it for real."

blk_install_dryrun() {
  cat <<EOF

Will install (skipped if already there)
  Homebrew (if missing) · iTerm2
  Fonts: Maple Mono NF CN (SIL OFL, free for commercial use) + Symbols Nerd Font
  CLI: starship eza bat fzf fd zoxide ripgrep atuin tmux git-delta
       zsh-autosuggestions zsh-syntax-highlighting
       + the brew package for your Node choice (fnm / nvm / node / vfox)
  oh-my-zsh (if missing) · iTerm2 Shell Integration

Will write these files
  ~/.zshrc                                    <- backed up under ~/.hekouwang-terminal-backups/ first
  ~/.zshrc.local                              <- created only if absent, never overwritten
  ~/.config/hekouwang-terminal/node.sh         <- Node manager snippet (switch with ./scripts/node-mgr.sh)
  ~/.hekouwang-terminal-backups/               <- .zshrc backup folder (not scattered in $HOME)
  ~/.config/starship.toml
  ~/.config/hekouwang-terminal/current/        <- ecosystem colors (colors.sh/delta/tmux)
  ~/Library/Application Support/iTerm2/DynamicProfiles/hekouwang-active-theme.json
  ~/.config/bat/themes/hekouwang-*.tmTheme    <- plus one bat cache --build
  ~/.config/ghostty/{config,themes/hekouwang-*}   <- only if Ghostty is installed; old config backed up
  ~/.warp/themes/*.yaml                        <- only if Warp is installed
  ~/.vscode|.cursor/extensions/hekouwang-terminal-themes-*/  <- only if that editor is installed

Will append one line to config you already own (each is backed up first)
  ~/.gitconfig    adds [include] path=.../delta.gitconfig   (git diff colors)
  ~/.tmux.conf    adds source-file .../tmux.conf            (tmux colors)

Will write these system settings (defaults)
  com.googlecode.iterm2: Minimal theme, no scrollbar, default profile,
                         Shift+Enter for newline, status bar position, toolbelt
  global: ApplePressAndHoldEnabled=false (key repeat on hold — vim users need it)

Will not touch
  your ~/.ssh/, an existing ~/.zshrc.local, other Homebrew packages you installed

Default theme: $DEFAULT_THEME
How to undo: ./scripts/uninstall.sh (has --dry-run too)
EOF
}

# ---- 正常安装流程 ----------------------------------------------
M_INSTALL_CN_MIRROR="China mirrors enabled (Tsinghua TUNA) — Homebrew will use domestic sources..."
M_INSTALL_BREW="Installing Homebrew..."
M_INSTALL_ITERM_FONTS="Installing iTerm2 + fonts (Maple Mono NF CN / Symbols Nerd Font / JetBrains Mono fallback)..."
M_INSTALL_CASK_SKIP_MANUAL="%s already installed (installed by hand, not tracked by brew), skipped"
M_INSTALL_CASK_FAIL="⚠ %s failed to install (on a China network try CN=1 ./scripts/install.sh)"
M_INSTALL_CLI="Installing the CLI set (one by one — a single failure will not abort the run)..."
M_INSTALL_PKG_FAIL="⚠ %s failed to install, skipping it for now"
M_INSTALL_PKG_FAILED_SUM="⚠ These did not install, run brew install for them later:%s"
M_INSTALL_OMZ="Installing oh-my-zsh..."
M_INSTALL_CONFIG="Deploying config files..."
M_INSTALL_GHOSTTY_BAK="Backed up your Ghostty config → ~/.config/ghostty/config.bak.*"
M_INSTALL_GHOSTTY_OK="✓ Ghostty themes and config deployed (press Cmd+Shift+, in Ghostty to reload)"
M_INSTALL_WARP_OK="✓ Warp themes deployed (pick the matching name in Warp → Settings → Appearance)"
M_INSTALL_BAT="Installing bat syntax themes (all of them, once)..."
M_INSTALL_BAT_OK="✓ %s bat themes installed and cached"
M_INSTALL_BAT_CACHE_FAIL="⚠ bat cache --build failed (cat highlighting falls back to default colors, nothing else affected)"
M_INSTALL_BAT_MISSING="⚠ bat is not installed, skipping its themes"
M_INSTALL_THEME="Deploying theme + ecosystem colors (default: %s)..."
M_INSTALL_GIT_SKIP="git diff colors already wired up, skipped"
M_INSTALL_GIT_OK="✓ git diff colors wired into ~/.gitconfig (delta)"
M_INSTALL_TMUX_SKIP="tmux colors already wired up, skipped"
M_INSTALL_TMUX_OK="✓ tmux colors wired into ~/.tmux.conf"
M_INSTALL_TMUX_MARK="# hekouwang-terminal-skill colors (content updates itself when you switch themes)"
M_INSTALL_VSC_OK="✓ Editor theme installed → %s (restart the editor, then pick it in the theme list)"
M_INSTALL_ZSHRC_BAK="Backed up your ~/.zshrc → %s"
M_INSTALL_ZSHRC_HINT_MIGRATE="💡 Your old .zshrc has alias/export lines — to keep them, hit Ctrl+C and run ./scripts/migrate.sh instead"
M_INSTALL_SI="Installing iTerm2 Shell Integration (imgcat / it2copy and friends)..."
M_INSTALL_SI_OK="✓ Shell Integration installed"
M_INSTALL_SI_FAIL="⚠ Shell Integration failed to install (no imgcat/it2copy, nothing else affected)"
M_INSTALL_DEFAULTS="System setting: key repeat on press-and-hold (vim users need this)..."
M_INSTALL_GUI="Writing the iTerm2 GUI settings (Minimal theme / default profile / Shift+Enter newline)..."
M_INSTALL_DOCTOR="Running the environment check..."
M_INSTALL_DONE="✅ All done!"
M_INSTALL_TAIL_LOCAL="Put private config (SSH aliases, proxies) in ~/.zshrc.local"
M_INSTALL_TAIL_OPEN="Open iTerm2 and it is live."
# ⛔ Do not put "bat/fzf/git diff follow along" back into this line. That is a
#    paid-pack capability; the open-source build syncs iTerm2 only, and this text
#    is printed by both builds. Advertising it here is the same fishing mistake
#    that was once in the public repo's GitHub description.
M_INSTALL_TAIL_THEME="Switch theme: ./scripts/theme.sh"
M_INSTALL_TAIL_NODE="Switch Node manager: ./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
M_INSTALL_TAIL_UNDO="Changed your mind: ./scripts/uninstall.sh (supports --dry-run)"
M_INSTALL_TAIL_CN="💡 On a China network, if it dies on portable-ruby / download errors, use: CN=1 ./scripts/install.sh"
# Printed only when the paid pack is absent. %s = landing page.
M_INSTALL_TAIL_BUY="Unified terminal workbench — buy on platforms (SkillPay ¥59.9/yr · SkillHub ¥2.99/call): %s"
M_INSTALL_GUI_FAIL="! GUI setup did not finish (everything else is installed). Run it later: ./scripts/setup-gui.sh"

# ---- Node manager choice ------------------------------------
M_INSTALL_NODE_PROMPT="Pick one Node version manager (keep exactly one — do not mix):"
M_INSTALL_NODE_OPT_FNM="  1) fnm   — Fast Node Manager (recommended, default)"
M_INSTALL_NODE_OPT_NVM="  2) nvm"
M_INSTALL_NODE_OPT_BREW="  3) brew  — Homebrew node (single version, not a version manager)"
M_INSTALL_NODE_OPT_VFOX="  4) vfox  — version-fox (multi-language SDKs)"
M_INSTALL_NODE_ASK="Which one? [1]: "
M_INSTALL_NODE_PICKED="Node manager: %s"
M_INSTALL_NODE_BAD="✗ Unknown Node manager '%s'"
M_INSTALL_NODE_CHOICES="Choices: fnm · nvm · brew · vfox (or ./scripts/install.sh --node fnm)"
M_INSTALL_NODE_DEPLOYED="✓ Node snippet written (%s)"
M_INSTALL_NODE_SWITCH_HINT="To switch later: ./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
M_INSTALL_NODE_WRITE_FAIL="⚠ Could not write the Node snippet (check config/node/)"
M_INSTALL_FETCH_FAIL="✗ Download failed: %s"
M_INSTALL_FETCH_SAVED="Downloaded to %s (SHA-256: %s)"
M_INSTALL_FETCH_SOURCE="Source: %s"
M_INSTALL_FETCH_HOW="Review, then run: bash %s  — or set HKW_ASSUME_YES=1 to let the installer run it automatically"
M_INSTALL_FETCH_STOP="Homebrew is still missing: run the downloaded installer above, then rerun this command"
M_INSTALL_FETCH_STOP_OMZ="oh-my-zsh is still missing: run the downloaded installer above, then rerun this command (no .zshrc was written)"
