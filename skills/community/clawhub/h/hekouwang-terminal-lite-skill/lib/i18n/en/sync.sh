#!/bin/bash
# 词条表 · 英文 · sync.sh

blk_sync_help() {
  cat <<'EOF'
hekouwang-terminal-skill — machine migration / config drift / pinned-state migrate

Usage:
  ./scripts/sync.sh                        check: is what is deployed still identical to the repo (read-only)
  ./scripts/sync.sh --pull                 redeploy from the repo, pulling drifted files back into line
  ./scripts/sync.sh --export <path>        build a package you can carry to a second machine (whole tree)
  ./scripts/sync.sh --state-export [file]  export pinned state (theme / auto / node / optical / scene / badge)
  ./scripts/sync.sh --state-import <file>  restore pinned state on a new machine from the manifest
  ./scripts/sync.sh --lang zh              run in Chinese

The problem it solves: you hand-edited the Ghostty config on machine A, machine B is
still on the old config, and six months later you have no idea which one is right.
This makes "where did it drift" something you can see in one line.

For "what did I pin" across machines use --state-export / --state-import;
--export still packs the whole skill.
EOF
}

M_SY_EXPORT_HEAD="Packing for a second machine…"
M_SY_EXPORT_COUNT="  %s files → %s"
M_SY_EXPORT_OK="✓ packed"
M_SY_EXPORT_NEXT="On the second machine: unzip → cd into it → ./scripts/install.sh"
M_SY_EXPORT_BRAND="(includes the brand theme pack — for your own machines only, do not pass it on)"
M_SY_EXPORT_NO_BRAND="(without the brand theme pack, so it installs with the 3 community themes)"

M_SY_STATE_EXPORT_HEAD="Exporting pinned state…"
M_SY_STATE_EXPORT_OK="✓ wrote %s"
M_SY_STATE_EXPORT_NEXT="On the new machine (kit installed): ./scripts/sync.sh --state-import <this json>"
M_SY_STATE_IMPORT_NEED="✗ usage: ./scripts/sync.sh --state-import <manifest.json>"
M_SY_STATE_IMPORT_HEAD="Restoring from manifest: %s"
M_SY_STATE_APPLIED_LANG="lang → %s"
M_SY_STATE_APPLIED_NODE="Node → %s"
M_SY_STATE_APPLIED_THEME="theme → %s"
M_SY_STATE_APPLIED_OPTICAL="optical → %s"
M_SY_STATE_APPLIED_SCENE="scene → %s"
M_SY_STATE_APPLIED_BADGE="badge → %s"
M_SY_STATE_APPLIED_BADGE_FILE="badge written to runtime file"
M_SY_STATE_FAIL_NODE="Node restore failed"
M_SY_STATE_FAIL_THEME="theme restore failed (theme may be missing on this machine)"
M_SY_STATE_FAIL_OPTICAL="optical restore failed"
M_SY_STATE_FAIL_SCENE="scene restore failed"
M_SY_STATE_SKIP_PAID="skip paid item %s (script not in open-source tree)"
M_SY_STATE_IMPORT_DONE="✓ pinned state restored as far as this build allows"
M_SY_STATE_IMPORT_NEXT="Suggested: ./scripts/doctor.sh --status"
M_SY_HEAD="═══ Config drift check ═══"
M_SY_CURRENT="current theme: %s"
M_SY_NOT_DEPLOYED="not deployed"
M_SY_GEN_HEAD="Generated files (should match the repo byte for byte)"
M_SY_PROFILE_MISSING="iTerm2 profile: not deployed"
M_SY_PROFILE_NO_SRC="iTerm2 profile: no matching file in the repo"
M_SY_PROFILE_SAME="iTerm2 profile   [font detected on this Mac: %s]"
M_SY_PROFILE_DIFF="iTerm2 profile has been edited (in fields other than the font)"
M_SY_COMPARE="compare with: diff '%s' '%s'"
M_SY_ECO_COLORS="ecosystem colors colors.sh"
M_SY_ECO_DELTA="git diff colors"
M_SY_ECO_TMUX="tmux colors"
M_SY_ECO_GHOSTTY="Ghostty theme"
M_SY_NO_THEME="no theme deployed yet (run ./scripts/theme.sh <theme>)"
M_SY_TPL_HEAD="Templates (editing these is normal — this only tells you that you did)"
M_SY_TPL_STARSHIP="starship.toml"
M_SY_TPL_GHOSTTY="Ghostty config"
M_SY_TPL_ZSHRC=".zshrc"
M_SY_LOCAL_HEAD="Machine-local only (must never go into the repo)"
M_SY_LOCAL_OK="~/.zshrc.local is here (%s lines)"
M_SY_LOCAL_MISSING="~/.zshrc.local does not exist (SSH aliases / proxies belong there)"
M_SY_NOT_DEPLOYED_ITEM="%s: not deployed"
M_SY_NO_SRC_ITEM="%s: no matching file in the repo"
M_SY_EDITED_ITEM="%s has been edited"
M_SY_RESULT="═══ Verdict ═══"
M_SY_NO_DRIFT="No drift — this machine matches the repo."
M_SY_DRIFT="%d files differ from the repo."
M_SY_DRIFT_KEEP="  want to keep the local changes → do nothing (except generated files: the generator overwrites those next run)"
M_SY_DRIFT_PULL="  want the repo version back → ./scripts/sync.sh --pull"
M_SY_PULL_HEAD="Redeploying from the repo…"
M_SY_PULL_SS="✓ starship.toml pulled back into line"
M_SY_PULL_SS_SAME="· starship.toml already matches the repo; left untouched"
M_SY_PULL_SS_BAK="old copy backed up at %s"
M_SY_PULL_NOTE="Note: ~/.zshrc was left alone — it may contain what you migrated into it."
M_SY_PULL_NOTE2="To pull that back too: cp %s/config/zshrc.template ~/.zshrc (back it up first)"
