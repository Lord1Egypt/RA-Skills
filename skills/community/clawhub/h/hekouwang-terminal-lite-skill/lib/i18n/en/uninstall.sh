#!/bin/bash
# 词条表 · 英文 · uninstall.sh

blk_uninstall_help() {
  cat <<'EOF'
hekouwang-terminal-skill — uninstall / restore

Usage:
  ./scripts/uninstall.sh              interactive: asks item by item, removes only this skill's files
  ./scripts/uninstall.sh --dry-run    print what it would do, write nothing
  ./scripts/uninstall.sh --yes        no questions, run the default set (keeps brew packages and oh-my-zsh)
  ./scripts/uninstall.sh --lang zh    run in Chinese

Design rules (this file and install.sh are a pair — never change just one):
  1. Only removes what this skill installed. Homebrew itself, oh-my-zsh, your
     ~/.zshrc.local and your own git config are left alone unless you say otherwise.
  2. ~/.zshrc is restored from the timestamped .bak install.sh left behind, not deleted.
     If no backup is found it says so instead of pretending it worked.
  3. iTerm2 GUI settings are reset with defaults delete, back to iTerm2's own factory
     defaults — not to values we think are sensible (that would just be more meddling).
  4. It prints the list before removing anything; --dry-run prints the very same list.
EOF
}

M_UN_HEAD="═══ hekouwang-terminal-skill uninstall ═══"
M_UN_DRY="DRY-RUN: prints only, touches no files"
M_UN_S1="1. ~/.zshrc"
M_UN_BAK_FOUND="Backup found: "
M_UN_ASK_RESTORE="Restore it as ~/.zshrc? (the current one is kept as .zshrc.uninstall.bak)"
M_UN_RESTORED="Restored ~/.zshrc ← %s"
M_UN_KEEP_ZSHRC="Keeping the current ~/.zshrc (its line sourcing the ecosystem colors will go stale; remove it by hand)"
M_UN_NO_BAK="No zshrc backup found (~/.hekouwang-terminal-backups/ or home-root legacy) — this script will not guess your content, please check ~/.zshrc yourself"
M_UN_NO_BAK_NOTE="What this skill added to .zshrc was: source ~/.config/hekouwang-terminal/current/colors.sh"

M_UN_S2="2. Files this skill wrote"
M_UN_RM_DP="remove the iTerm2 Dynamic Profile"
M_UN_NO_DP="no iTerm2 Dynamic Profile"
M_UN_RM_RUNTIME="remove the runtime folder ~/.config/hekouwang-terminal/"
M_UN_NO_RUNTIME="no runtime folder"
M_UN_ASK_STARSHIP="Handle ~/.config/starship.toml? (restore from the install backup first, remove only if none; say n if you edited it yourself)"
M_UN_ASK_ITEM="Run this item? %s"
M_UN_KEEP_ITEM="skipped"
M_UN_RM_APPLE="remove this tool's profiles from macOS Terminal"
M_UN_RM_GIT="remove this tool's include from ~/.gitconfig"
M_UN_RM_TMUX="remove this tool's source-file from ~/.tmux.conf"
M_UN_RM_STARSHIP="remove starship.toml"
M_UN_RESTORE_STARSHIP="restore starship.toml from backup: %s"
M_UN_KEEP_STARSHIP="keeping starship.toml"
M_UN_RM_GHOSTTY_THEMES="remove Ghostty's hekouwang-* themes"
M_UN_ASK_GHOSTTY="Ghostty config has a backup — restore it?"
M_UN_RESTORE_GHOSTTY="restore Ghostty config ← %s"
M_UN_RM_GHOSTTY_CFG="remove the Ghostty config this skill wrote"
M_UN_RM_BAT="remove bat's hekouwang-* themes"
M_UN_RM_VSC="remove the editor theme extension (%s)"

M_UN_S2B="2b. macOS Terminal"
M_UN_INSIDE_APPLE="This script is running inside the macOS Terminal, skipping it (changes would be overwritten when it quits, and it might close on you)"
M_UN_INSIDE_APPLE_FIX="run this script once from a different terminal to restore it"
M_UN_APPLE_DRY="remove this skill's profiles from the macOS Terminal and restore the previous default profile"
M_UN_APPLE_NONE="the macOS Terminal has no profile from this skill"
M_UN_APPLE_RUNNING="macOS Terminal is open — it overwrites settings when it quits, so Cmd+Q it once"
M_UN_APPLE_BAK="A full backup from before the first change is at ~/.hekouwang-AppleTerminal-prefs.bak.plist (to fully restore: defaults import com.apple.Terminal <that file>)"

M_UN_S3="3. References inside your own config"
M_UN_GIT_DRY="remove the hekouwang-terminal [include] from ~/.gitconfig"
M_UN_GIT_DONE="Removed the include from ~/.gitconfig (the original was backed up)"
M_UN_GIT_NONE="~/.gitconfig has no include from this skill"
M_UN_TMUX_DRY="remove the source-file line from ~/.tmux.conf"
M_UN_TMUX_DONE="Removed the source-file line from ~/.tmux.conf (the original was backed up)"
M_UN_TMUX_NONE="~/.tmux.conf has no reference to this skill"


M_UN_S5="5. iTerm2 GUI settings (back to iTerm2's factory defaults)"
M_UN_INSIDE_ITERM="This script is running inside iTerm2, skipping the GUI settings reset"
M_UN_INSIDE_ITERM_WHY="why: resetting those requires quitting iTerm2 first, and quitting here would close the terminal you are using and abort the uninstall"
M_UN_INSIDE_ITERM_FIX="how to finish: run %s/uninstall.sh from the built-in Terminal app"
M_UN_INSIDE_ITERM_WHAT="what was skipped: Minimal theme / default profile / Shift+Enter / hidden scrollbar and other appearance items"
M_UN_ASK_GUI="Delete the iTerm2 settings this skill wrote and go back to factory defaults?"
M_UN_ITERM_RUNNING="iTerm2 is running, quitting it first (otherwise its in-memory config overwrites what we write)"
M_UN_DEFAULT_KEPT="the default profile is no longer this skill's, leaving it alone"
M_UN_KEYMAP_DRY="remove the Shift+Enter key mapping (your other mappings are kept)"
M_UN_ASK_PRESSHOLD="Also restore press-and-hold accent menu? (this skill turned it off for vim)"
M_UN_KEEP_GUI="keeping the iTerm2 GUI settings"

M_UN_S6="6. Command line tools (kept by default — they are probably part of your daily setup now)"
M_UN_INSTALLED_HERE="installed here: %s"
M_UN_ASK_BREW="Uninstall those brew packages too? (most people should say n)"
M_UN_KEEP_BREW="kept (they do not depend on this skill and keep working after uninstall)"
M_UN_NO_BREW="no brew install record from this skill (older installs left no record, so nothing is removed here)"
M_UN_ASK_OMZ="Delete oh-my-zsh? (not part of this skill, it just builds on it)"
M_UN_RM_OMZ="remove ~/.oh-my-zsh"
M_UN_KEEP_OMZ="keeping oh-my-zsh"

M_UN_DONE="═══ Done ═══"
M_UN_DONE_DRY="That was a dry run, nothing was touched. Drop --dry-run to do it for real."
M_UN_DONE_REAL_A="Restored."
M_UN_DONE_REAL_B="Close this terminal window and open a new one for the change to take effect."
M_UN_DONE_KEPT="Never touched: Homebrew itself, ~/.zshrc.local, your own ssh/git config,"
M_UN_DONE_KEPT2="  the fonts in ~/Library/Fonts (to remove: brew uninstall --cask font-maple-mono-nf-cn)."
