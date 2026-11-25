#!/bin/bash
# 词条表 · 英文 · migrate.sh

blk_migrate_help() {
  cat <<'EOF'
hekouwang-terminal-skill — adopt your existing .zshrc instead of overwriting it

Usage:
  ./scripts/migrate.sh              show the report first, decide afterwards
  ./scripts/migrate.sh --apply      do it (still makes a backup first)
  ./scripts/migrate.sh --lang zh    run in Chinese

Why this exists: install.sh replaces ~/.zshrc with a template. That is fine on a new
Mac, but if you have used yours for years — aliases, PATH entries, work env vars —
replacing it loses all of that at once (there is a .bak, but you would have to fish
every line back out by hand).

What this script does: it moves the lines that are *yours* into ~/.zshrc.local and
drops the lines the template provides anyway (oh-my-zsh init, starship, the fzf /
zoxide / atuin init lines, plugin sourcing), because the template gives you those
back in a better order.

It errs on the safe side: anything ambiguous counts as yours. The template sources
~/.zshrc.local at the end, so nothing of yours goes missing.
EOF
}

M_MIG_HEAD="═══ Adopting your existing .zshrc ═══"
M_MIG_NO_ZSHRC="No ~/.zshrc — this is a fresh environment, just run ./scripts/install.sh, no migration needed."
M_MIG_OVERLAP="Your ~/.zshrc shares %s%% of its code lines with this skill's template"
M_MIG_OVERLAP_1="  — which means it already is this template (most likely an older version you now want to update)."
M_MIG_OVERLAP_2="This is not a case for migrating"
M_MIG_OVERLAP_3=": template lines would be treated as yours and moved into ~/.zshrc.local,"
M_MIG_OVERLAP_4="  leaving a copy on both sides — plugins loaded twice, aliases defined twice, possibly a shell that will not start."
M_MIG_OVERLAP_5="Just run ./scripts/install.sh"
M_MIG_OVERLAP_6=" (it backs ~/.zshrc up under ~/.hekouwang-terminal-backups/ first)."
M_MIG_OVERLAP_7="Really have a few customisations scattered in there? Diff it yourself first:"
M_MIG_OVERLAP_8="Move the lines that are yours into ~/.zshrc.local, then run ./scripts/install.sh."
M_MIG_OVERLAP_9="To force the migration anyway: ./scripts/migrate.sh --force --apply"

M_MIG_SYNTAX_FAIL="⚠ The automatic split does not parse, aborting — it will not write a broken .zshrc.local"
M_MIG_SYNTAX_FIX1="Please migrate by hand: copy your own aliases / exports / functions from ~/.zshrc into ~/.zshrc.local,"
M_MIG_SYNTAX_FIX2="then run: cp %s/config/zshrc.template ~/.zshrc"

M_MIG_TOTAL="Your old ~/.zshrc has %s lines"
M_MIG_KEPT="%s lines are yours → moved into ~/.zshrc.local"
M_MIG_DROPPED="%s lines the template provides → dropped"
M_MIG_DROP_HEAD="What gets dropped (and why)"
M_MIG_KEEP_HEAD="What gets moved (first 30 lines)"
M_MIG_KEEP_MORE="…and %s more lines"
M_MIG_KEEP_NONE="(nothing needs moving)"
M_MIG_PREVIEW_ONLY="That was a preview, nothing has been touched."
M_MIG_PREVIEW_NEXT="Happy with it? Run: ./scripts/migrate.sh --apply"
M_MIG_PREVIEW_WHAT="(--apply will: back up your .zshrc → append the lines above to ~/.zshrc.local → deploy the template)"

M_MIG_RUNNING="Applying"
M_MIG_BAK="your old .zshrc was backed up → %s"
M_MIG_LOCAL_BAK="your old .zshrc.local was backed up → %s"
M_MIG_APPENDED="your config was appended to %s"
M_MIG_TEMPLATE="the template is deployed as ~/.zshrc (it sources ~/.zshrc.local at the end)"
M_MIG_BANNER1="the block below was moved here from your old ~/.zshrc by migrate.sh on %s"
M_MIG_BANNER2="the original file is backed up at %s"

M_MIG_VERIFY="Verifying: can the new config actually start a shell"
M_MIG_VERIFY_SLOW="⚠ It starts, but took %ss (slow)"
M_MIG_VERIFY_SLOW_FIX="run ./scripts/doctor.sh --profile to see what is eating the time."
M_MIG_VERIFY_OK="✓ fine (under %ss)"
M_MIG_VERIFY_FAIL="✗ will not start, or took over 25 seconds — rolling back automatically"
M_MIG_ROLLED_BOTH="~/.zshrc and ~/.zshrc.local are both back to how they were before the migration"
M_MIG_ROLLED_ONE="~/.zshrc is back to how it was before the migration"
M_MIG_ROLLED_NOTE="You have not been left in a broken state. Please migrate by hand:"
M_MIG_ROLLED_NOTE2="copy your own aliases / exports / functions from ~/.zshrc into ~/.zshrc.local,"
M_MIG_ROLLED_NOTE3="then run: cp %s/config/zshrc.template ~/.zshrc"

M_MIG_DONE="Done."
M_MIG_DONE_NOTE="Open a new terminal window to check. Something wrong? One command to roll back:"
M_MIG_DONE_DOCTOR="Worth running ./scripts/doctor.sh once to check the load order."
