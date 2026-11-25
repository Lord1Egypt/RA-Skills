#!/bin/bash
# 词条表 · 英文 · unlock.sh（装付费包）

blk_unlock_help() {
  cat <<'EOF'
hekouwang-terminal-skill — install the paid pack in one command

  ./scripts/unlock.sh ~/Downloads/hekouwang-terminal-skill-paid-20260723.zip
  ./scripts/unlock.sh <zip> --dry-run     say what it would do, touch nothing
  ./scripts/unlock.sh <zip> --no-apply    unpack and regenerate, but do not redeploy the theme
  ./scripts/unlock.sh --rollback          restore the latest pre-update snapshot
  ./scripts/unlock.sh <zip> --allow-downgrade  explicitly install an older build
  ./scripts/unlock.sh <zip> --lang zh     run in Chinese
EOF
}
M_UL_ROLLBACK_OK="Restored paid update snapshot %s"
M_UL_ROLLBACK_NONE="No paid update snapshot found"
M_UL_DOWNGRADE_BLOCKED="Refusing downgrade: installed %s, package %s"
M_UL_DOWNGRADE_HINT="Use --allow-downgrade only when you intentionally need an older build"
M_UL_SNAPSHOT_FAIL="Could not create the paid-update safety snapshot"
M_UL_SNAPSHOT_OK="Safety snapshot: %s"
M_UL_AUTO_ROLLBACK="Update failed; restored the pre-update product files automatically"
M_UL_AUTO_ROLLBACK_FAIL="Automatic update rollback failed; snapshot: %s"

M_UL_USAGE="Usage: ./scripts/unlock.sh <paid-pack.zip> [--dry-run] [--no-apply] [--allow-downgrade]"
M_UL_USAGE_1="  No paid pack yet? The open-source build is complete on its own — not having it"
M_UL_USAGE_2="  takes nothing away from what already works."
M_UL_USAGE_3="  The paid pack unlocks: 4 brand themes (2 of them light) + Ghostty/Warp/macOS Terminal sync"
M_UL_USAGE_4="  + bat/fzf/eza/git diff/tmux/VS Code all in the same colors + the font priority table + the cheat sheet."
M_UL_UNKNOWN_ARG="unknown argument: %s"

M_UL_S1="1. Checking the paid pack"
M_UL_NO_FILE="no such file: %s"
M_UL_FILE_OK="file exists (%s)"
M_UL_ZIP_OK="archive is intact (unzip -t passed)"
M_UL_ZIP_BAD="archive is damaged or truncated — download it again"
M_UL_IS_PAID="confirmed as the paid pack (contains %s)"
M_UL_NOT_PAID="this does not look like this skill's paid pack — it has no %s"
M_UL_YOUR_ZIP="  the zip you picked: %s"

M_UL_S2="2. Checking where it is being installed"
M_UL_DIR_OK="this folder is hekouwang-terminal-lite-skill: %s"
M_UL_DIR_BAD="this does not look like a hekouwang-terminal-lite-skill folder (no theme.sh, or no config/themes/_generate.py)"
M_UL_DIR_FIX="  put unlock.sh and the paid pack inside the hekouwang-terminal-lite-skill folder you cloned, then run it there."
M_UL_ALREADY="! The paid pack is already installed; this run will overwrite it with the new version"

M_UL_S3="3. Unpacking (%s files)"
M_UL_DRY_HEAD="═══ DRY-RUN — nothing below is actually executed ═══"
M_UL_DRY_1="These files would be unpacked into %s (overwriting matching names):"
M_UL_DRY_MORE="…… and %s more"
M_UL_DRY_THEN="Then it would run:"
M_UL_DRY_GEN="# regenerate every theme"
M_UL_DRY_APPLY="# redeploy + build the bat cache"
M_UL_DRY_KEEP="Will not touch: your ~/.zshrc, ~/.zshrc.local, ~/.ssh/"
M_UL_DRY_TAIL="Drop --dry-run to run it for real."

M_UL_UNPACKED="unpacked %s files"
M_UL_UNPACK_FAIL="unpacking failed"
M_UL_MARKER_MISSING="still cannot find %s after unpacking — please send me the output above"
M_UL_MARKER_OK="the marker file is in place"
M_UL_S4="4. Regenerating themes"
M_UL_GEN_OK="generated"
M_UL_GEN_FAIL="the generator failed"
M_UL_S5_SKIP="5. Skipping deployment (--no-apply)"
M_UL_S5_SKIP_NOTE="  to apply it: ./scripts/theme.sh ember"
M_UL_S5="5. Redeploying the theme"
M_UL_KEEP_THEME="  your current theme is %s; redeploying it so the new ecosystem colors take effect"
M_UL_SWITCH_THEME="  switching to the default brand theme %s (want another? run ./scripts/theme.sh with no arguments to see all seven)"
M_UL_DONE="═══ Done ═══"
M_UL_DONE_1="  switch theme: ./scripts/theme.sh            (no arguments shows all seven)"
M_UL_DONE_3="  project workspaces: ./scripts/workspace.sh"
M_UL_DONE_4="  derive your own theme from one brand color: ./scripts/palette.sh --from '#e08a5f' --name mytheme"
M_UL_DONE_5="  cheat sheet: docs/cheatsheet.pdf (A4, ready to print)"
M_UL_DONE_6="  something off: ./scripts/doctor.sh"
M_UL_APPLY_FAIL="deploying the theme failed — run ./scripts/doctor.sh to see which step"
# 版本比对：老免费仓 + 新付费包 = 树里两个版本号不一致
M_UL_VER_SKEW="your open-source tree is %s, this paid pack is %s"
M_UL_VER_SKEW_FIX="run 'git pull' first, then unlock — otherwise the free-tier scripts stay one version behind the paid parts"
