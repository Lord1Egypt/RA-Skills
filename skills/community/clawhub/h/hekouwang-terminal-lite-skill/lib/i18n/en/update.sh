#!/bin/bash
# 词条表 · 英文 · update.sh

blk_update_help() {
  cat <<'EOF'
hekouwang-terminal-skill — update to the latest version

Usage:
  ./scripts/update.sh              pull updates → regenerate themes → redeploy the current theme
  ./scripts/update.sh --check      only show whether there is a new version and what changed
  ./scripts/update.sh --lang zh    run in Chinese

Why this exists: "updating" used to mean someone posts a new zip, you download and
reinstall it by hand, and you never really know whether you are on the latest version
or what changed. This script answers both.

It does not touch your ~/.zshrc.local or GUI settings you changed yourself; it only
regenerates the theme files and redeploys the theme you are currently using.
EOF
}

M_UP_HEAD="═══ hekouwang-terminal-skill update ═══"
M_UP_CURRENT="current version %s"
M_UP_UNKNOWN="unknown"
M_UP_NOT_GIT="This is not a git repo (probably an unzipped release)."
M_UP_NOT_GIT_1="How to update: grab the latest zip, unpack it over this same folder, then run ./scripts/install.sh once."
M_UP_NOT_GIT_2="Your ~/.zshrc.local and GUI settings will not be overwritten."
M_UP_S1="1. Checking the remote"
M_UP_NO_NET="⚠ cannot reach the remote (network?), nothing changed locally"
M_UP_UP_TO_DATE="✓ already on the latest version, nothing to do"
M_UP_N_COMMITS="%s new commits"
M_UP_S2="2. What changed"
M_UP_CHANGELOG="CHANGELOG additions:"
M_UP_CHECK_ONLY="--check mode, nothing was touched. To really update: ./scripts/update.sh"
M_UP_S3="3. Checking local changes"
M_UP_DIRTY="⚠ You have changed things in this folder:"
M_UP_ASK_STASH="Stash them before updating? (n aborts the update)"
M_UP_ABORTED="Aborted. Commit or stash them yourself and run this again."
M_UP_STASHED="✓ stashed (restore with: git stash pop)"
M_UP_STASH_MSG="update.sh auto-stash %s"
M_UP_S4="4. Pulling"
M_UP_PULLED="✓ code updated"
M_UP_PULL_FAIL="⚠ pull failed (conflicts?). Sort it out by hand: git pull"
M_UP_BRAND_GONE="⚠ The brand palette is gone — that should not happen. Copy brand.py back from your paid pack."
M_UP_S5="5. Regenerating themes"
M_UP_S6="6. Refreshing the prompt config"
M_UP_SS_NEW="✓ prompt config installed"
M_UP_SS_SAME="· prompt config unchanged"
M_UP_SS_UPDATED="✓ prompt config updated"
M_UP_SS_BAK="old copy backed up at %s"
M_UP_SS_NOTE="if you had edited it, pick your changes back out of the backup"
M_UP_S7="7. Redeploying the current theme"
M_UP_NO_THEME="· no current theme on record, skipped (run ./scripts/theme.sh <theme> yourself)"
M_UP_BAT="✓ bat themes refreshed"
M_UP_DONE="═══ Update complete ═══"
M_UP_DONE_NOTE="Open a new terminal window for it to take effect. Trouble? Run ./scripts/doctor.sh."
