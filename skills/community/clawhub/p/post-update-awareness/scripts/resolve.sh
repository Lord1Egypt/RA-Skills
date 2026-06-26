#!/usr/bin/env bash
# resolve.sh
#
# Stable resolver for locating this skill's script directory from outside
# the skill (e.g. from a safe-update wrapper, a cron job, a CI runner).
#
# Source this file, then call resolve_pua_scripts. It echoes the absolute
# path to the script directory on stdout and returns 0; returns 1 if the
# skill isn't installed in any known location.
#
# Usage:
#   source /path/to/post-update-awareness/scripts/resolve.sh
#   PUA_SCRIPTS=$(resolve_pua_scripts) || PUA_SCRIPTS=""
#   if [ -n "$PUA_SCRIPTS" ]; then
#     "$PUA_SCRIPTS/check-plugin-drift.sh" "$GATEWAY_VERSION"
#   fi
#
# Search order (first match wins):
#   1. $OPENCLAW_PROFILE_DIR/skills/post-update-awareness/scripts
#   2. $HOME/.openclaw-$OPENCLAW_PROFILE/skills/...   (when OPENCLAW_PROFILE set)
#   3. $HOME/.openclaw-noura/skills/...               (legacy default)
#   4. $HOME/.openclaw/skills/...
#   5. $HOME/openclaw-soul/skills/...
#   6. $HOME/clawhub-skills/...

resolve_pua_scripts() {
  local candidates=()

  if [ -n "${OPENCLAW_PROFILE_DIR:-}" ]; then
    candidates+=("$OPENCLAW_PROFILE_DIR/skills/post-update-awareness/scripts")
  fi

  if [ -n "${OPENCLAW_PROFILE:-}" ]; then
    candidates+=("$HOME/.openclaw-$OPENCLAW_PROFILE/skills/post-update-awareness/scripts")
  fi

  candidates+=(
    "$HOME/.openclaw-noura/skills/post-update-awareness/scripts"
    "$HOME/.openclaw/skills/post-update-awareness/scripts"
    "$HOME/openclaw-soul/skills/post-update-awareness/scripts"
    "$HOME/clawhub-skills/post-update-awareness/scripts"
  )

  # NB: we check -r (readable) not -x (executable) because clawhub install
  # does not preserve exec bits, and callers should invoke via `bash <script>`
  # regardless.
  for c in "${candidates[@]}"; do
    if [ -d "$c" ] && [ -r "$c/check-plugin-drift.sh" ]; then
      echo "$c"
      return 0
    fi
  done

  return 1
}

# When sourced this just defines the function. When executed directly,
# act as a one-shot resolver so callers can use either pattern.
if [ "${BASH_SOURCE[0]:-$0}" = "$0" ]; then
  resolve_pua_scripts
  exit $?
fi
