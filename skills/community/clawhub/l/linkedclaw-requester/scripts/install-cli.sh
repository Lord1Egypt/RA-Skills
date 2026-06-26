#!/usr/bin/env bash
# scripts/install-cli.sh — self-healing installer for @linkedclaw/cli.
#
# Short-circuits if a recent-enough `linkedclaw` is already on PATH.
# Otherwise tries: default npm prefix → ~/.npm-global → opt-in sudo.
# Also detects "older binary still wins PATH after upgrade" — a common
# multi-install conflict on macOS where `/usr/local/bin/linkedclaw` (old)
# shadows `~/.nvm/.../bin/linkedclaw` (new) — and reports it explicitly so
# the agent can surface the cleanup step to the user.
#
# Emits a single JSON line on stdout that the agent can parse:
#
#   Already up-to-date (>= MIN_VERSION and no newer version published, or the
#   registry was unreachable so we kept what works):
#     {"installed": true, "method": "already-installed", "version": "0.2.6"}
#
#   Already usable, but npm had a newer version — upgraded in place (silent;
#   the agent treats this exactly like already-installed):
#     {"installed": true, "method": "updated", "from": "0.2.8", "version": "0.2.9"}
#
#   Freshly installed (or upgraded) and now usable:
#     {"installed": true, "method": "global"|"npm-global"|"sudo",
#      "version": "0.2.6" [, "path_hint": "..."]}
#
#   Newer version landed in some prefix, but an older `linkedclaw` still
#   wins PATH-resolution order (multi-install conflict):
#     {"installed": false, "method": "stale-on-path",
#      "version": "0.2.0", "min_version": "0.2.6",
#      "found_paths": ["/usr/local/bin/linkedclaw", "~/.nvm/.../linkedclaw"],
#      "error": "An older @linkedclaw/cli still wins on PATH after upgrade.
#               Remove the older path (first entry of found_paths) so the
#               new one wins."}
#
#   Hard failure (npm itself errored everywhere):
#     {"installed": false, "method": "none", "error": "<npm stderr summary>"}
#
# Exit 0 on installed:true, 1 otherwise. The agent should inspect `method` to
# distinguish "ready" from "needs human action" (stale-on-path needs a `rm`
# from the user before the new CLI is usable).
#
# Why a script instead of inlining shell in the agent's reasoning:
#   The fallback chain (default prefix → ~/.npm-global → optional sudo) plus
#   the version-floor check + multi-install detection are mechanical but easy
#   to mis-implement under agent token pressure. Encoded once here so every
#   runtime (Claude Code, OpenClaw, Codex) gets the same correct chain with
#   a single tool call.

set -u
LANG=C
LC_ALL=C

# Version floor — bump this whenever the skill starts relying on a newer CLI
# flag. Currently 0.2.6 because `--intent` (semantic search, the skill's
# default discovery path) was added in 0.2.6. Operator can override with
# the LINKEDCLAW_MIN_VERSION env var for downgrade scenarios.
MIN_VERSION="${LINKEDCLAW_MIN_VERSION:-0.2.6}"

current_version() {
  # `linkedclaw --version` prints something like "cli 0.2.6".
  linkedclaw --version 2>/dev/null | awk '{print $NF}' | tr -d '\r\n'
}

# Newest version published to npm. Prints the version, or empty on ANY
# failure (offline, registry down, npm error). Callers MUST treat empty as
# "can't tell — keep what we have"; this is the fail-open contract that lets
# the CLI keep working without network access.
latest_version() {
  npm view @linkedclaw/cli version 2>/dev/null | tr -d '\r\n'
}

# Return 0 (true) if $1 >= $2, by semver-ish compare via `sort -V`.
version_ge() {
  [ "$1" = "$2" ] && return 0
  local smaller
  smaller=$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -1)
  [ "$smaller" = "$2" ]
}

# JSON-array of every `linkedclaw` PATH currently resolves, in PATH order.
# Uses `which -a` (BSD + GNU both ship it; we don't rely on `command -v -a`
# which is bash-only).
which_all_json() {
  local first=1
  printf '['
  if command -v which >/dev/null 2>&1; then
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      [ "$first" = 0 ] && printf ', '
      first=0
      local esc
      esc=$(printf '%s' "$p" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')
      printf '"%s"' "$esc"
    done < <(which -a linkedclaw 2>/dev/null)
  fi
  printf ']'
}

# Sanitize npm stderr into a one-line JSON value: '"error": "..."'.
err_field() {
  local raw="$1"
  local short
  short=$(printf '%s' "$raw" | tail -c 200 | tr '\n' ' ' \
            | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')
  printf '"error": "%s"' "$short"
}

emit_installed() {
  # $1 = method, $2 = optional extras (e.g. '"path_hint": "..."')
  local method="$1" extras="${2:-}"
  local version
  version=$(current_version)
  [ -z "$version" ] && version="unknown"
  printf '{"installed": true, "method": "%s", "version": "%s"%s}\n' \
    "$method" "$version" "${extras:+, $extras}"
}

emit_failed() {
  local method="$1" extras="${2:-}"
  printf '{"installed": false, "method": "%s"%s}\n' \
    "$method" "${extras:+, $extras}"
}

emit_stale_on_path() {
  local version paths
  version=$(current_version)
  [ -z "$version" ] && version="unknown"
  paths=$(which_all_json)
  printf '{"installed": false, "method": "stale-on-path", "version": "%s", "min_version": "%s", "found_paths": %s, "error": "An older @linkedclaw/cli still wins on PATH after upgrade. Remove the older path (first entry of found_paths) so the new one wins."}\n' \
    "$version" "$MIN_VERSION" "$paths"
}

# Run after a successful `npm install` step. Decides ready / stale-on-path /
# install-but-not-on-path, and emits the right JSON. Returns 0 if ready, 1
# otherwise.
post_install_check() {
  local method="$1" extras="${2:-}"
  hash -r 2>/dev/null || true  # refresh bash's command-resolution cache
  local cur
  cur=$(current_version)
  if [ -z "$cur" ]; then
    emit_failed "$method" \
      "$(err_field "install succeeded but linkedclaw not on PATH; check npm prefix vs shell PATH")"
    return 1
  fi
  if version_ge "$cur" "$MIN_VERSION"; then
    emit_installed "$method" "$extras"
    return 0
  fi
  emit_stale_on_path
  return 1
}

# 0. Already installed AND >= floor: the CLI is usable right now. Before
#    short-circuiting, opportunistically chase the newest published version.
#    Everything here is FAIL-OPEN: a network hiccup or a failed optional
#    upgrade must never break a working install — we fall back to the binary
#    we already have. (The "once per conversation" throttle lives in the
#    skill, not here: the agent runs this script once during env detection
#    and not again that conversation.)
if command -v linkedclaw >/dev/null 2>&1; then
  cur=$(current_version)
  if [ -n "$cur" ] && version_ge "$cur" "$MIN_VERSION"; then
    latest=$(latest_version)
    if [ -z "$latest" ] || version_ge "$cur" "$latest"; then
      # Offline / registry down / already newest → use what we have.
      emit_installed "already-installed" ""
      exit 0
    fi
    # A newer version exists — upgrade in place (silent; the skill treats
    # "updated" exactly like "already-installed").
    upd_out=$(npm install -g @linkedclaw/cli@latest 2>&1)
    if [ $? -eq 0 ]; then
      hash -r 2>/dev/null || true
      new=$(current_version)
      if [ -n "$new" ] && version_ge "$new" "$latest"; then
        emit_installed "updated" "\"from\": \"$cur\""
        exit 0
      fi
    fi
    # Upgrade didn't take (EACCES, stale-on-path, npm flake) but the existing
    # version still works → proceed on it rather than blocking the task.
    emit_installed "already-installed" \
      "\"update_skipped\": \"newer version $latest available but in-place upgrade did not take effect\""
    exit 0
  fi
  # Outdated below floor (or unreadable) — fall through to the install path,
  # which runs @latest with the full EACCES/sudo fallback chain.
fi

# Precondition: npm must exist.
if ! command -v npm >/dev/null 2>&1; then
  emit_failed "none" "$(err_field "npm not found on PATH; install Node.js first")"
  exit 1
fi

# 1. Default global install (uses npm's default prefix). `@latest` forces npm
#    to fetch the newest published version even if a stale one is already at
#    that prefix.
npm_out=$(npm install -g @linkedclaw/cli@latest 2>&1)
npm_status=$?
if [ "$npm_status" -eq 0 ] && command -v linkedclaw >/dev/null 2>&1; then
  if post_install_check "global" ""; then exit 0; else exit 1; fi
fi

# 2. EACCES (or any failure where the global prefix is the suspect): retry
#    under ~/.npm-global. Harmless when the global prefix wasn't the issue.
NPM_GLOBAL_DIR="$HOME/.npm-global"
mkdir -p "$NPM_GLOBAL_DIR"
npm_out=$(npm install --prefix "$NPM_GLOBAL_DIR" -g @linkedclaw/cli@latest 2>&1)
npm_status=$?
export PATH="$NPM_GLOBAL_DIR/bin:$PATH"
if [ "$npm_status" -eq 0 ] && command -v linkedclaw >/dev/null 2>&1; then
  path_hint='"path_hint": "Add ~/.npm-global/bin to PATH for future shells: export PATH=\"$HOME/.npm-global/bin:$PATH\""'
  if post_install_check "npm-global" "$path_hint"; then exit 0; else exit 1; fi
fi

# 3. Optional sudo escalation — only if the operator explicitly opted in.
if [ "${ALLOW_SUDO:-0}" = "1" ] && command -v sudo >/dev/null 2>&1; then
  npm_out=$(sudo -n npm install -g @linkedclaw/cli@latest 2>&1)
  npm_status=$?
  if [ "$npm_status" -eq 0 ] && command -v linkedclaw >/dev/null 2>&1; then
    if post_install_check "sudo" ""; then exit 0; else exit 1; fi
  fi
fi

# All attempts exhausted at the npm level.
emit_failed "none" "$(err_field "$npm_out")"
exit 1
