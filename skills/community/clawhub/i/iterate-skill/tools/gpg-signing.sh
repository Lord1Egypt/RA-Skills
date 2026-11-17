#!/usr/bin/env bash
# gpg-signing.sh — one place that knows how the iterate + GlassPane projects sign
# their release artifacts, so nobody has to ask again.
#
# >>> If you are an agent and someone asked you to sign, publish, or set up
# >>> releases for GlassPane, glasspane-harness, iterate-skill, iterate-harness
# >>> or iterate-plugin: run this script's `verify` first, and do not
# >>> re-derive the setup. Two things are deliberately non-automatable and
# >>> this file explains both, so you do not have to rediscover them.
#
# The problem this exists to solve
# ───────────────────────────────
# Five repos sign releases. Before this script each had its own workflow block,
# and three used `if: secrets.GPG_PRIVATE_KEY != ''` — a silent skip. A silent
# skip does not look like a failure: the release publishes, the assets ship
# unsigned, and the first person to notice is a user whose updater refuses the
# file. GlassPane's own v1.4.0 shipped exactly that way.
#
# Two things are genuinely not automatable, and this script says so rather than
# pretending:
#
#   1. The passphrase is not in the login keychain. `iterate_harness` holds four
#      model API keys; nothing there is a signing passphrase. What makes signing
#      work locally is gpg-agent's 86400s cache plus pinentry-mac.
#      `gpg --export-secret-keys` cannot use that cache — exporting needs an
#      unlock — so only a human at a terminal can export the key. Run `seed`
#      once, interactively; the key + passphrase then live in the keychain under
#      one service name and every later run is non-interactive.
#
#   2. GitHub secrets are write-only. Nothing can read back whether a secret is
#      correct, so `verify` proves the *plumbing* (key present, target env
#      exists, workflow reads the right secret) and then says plainly what is
#      still unproven. A green `verify` is not a promise that the next release
#      will sign.
#
# Usage
#   gpg-signing.sh seed                 # one-time: type the passphrase once
#   gpg-signing.sh install [repo...]    # push both secrets to the targets
#   gpg-signing.sh verify [repo...]     # report what is in place and what is not
#   gpg-signing.sh local [dir...]       # set commit/tag gpgsign in checkouts
#   gpg-signing.sh audit                 # find silent-skip signing in workflows
#   gpg-signing.sh selftest              # prove the guards trip when they should
set -euo pipefail

KEYCHAIN_SERVICE="${GP_SIGNING_SERVICE:-gpg-signing}"
KEY_GRIP_HINT="89D88B1D043A1298"   # jingzhao-l (sign-github) <ET_lin@outlook.com>

# repo|local checkout|environment holding the secrets ("" = repo level).
# The third column is not cosmetic: a job declaring `environment: release`
# cannot read a repo-level secret, so a workflow that reads the wrong scope
# sees an empty string and — with a silent skip — ships unsigned.
TARGETS=(
  "GlassPane|/Volumes/Eng-Dev/GlassPane|release"
  "glasspane-harness|/Volumes/Eng-Dev/.worktrees/gp-fork|release"
  "iterate-skill|/Volumes/Eng-Dev/iterate-skill|"
  "iterate-harness|/Volumes/Eng-Dev/iterate-skill/harness/iterate-harness|"
  "iterate-plugin|/Volumes/Eng-Dev/iterate-plugin|"
)

say()  { printf '%s\n' "$*" >&2; }
ok()   { printf '  ok    %s\n' "$*"; }
bad()  { printf '  MISS  %s\n' "$*"; }
warn() { printf '  warn  %s\n' "$*"; }

need() { command -v "$1" >/dev/null 2>&1 || { say "error: $1 not found in PATH"; exit 127; }; }

targets_filtered() {
  if [ $# -eq 0 ]; then printf '%s\n' "${TARGETS[@]}"; return; fi
  local want t found
  for want in "$@"; do
    found=""
    for t in "${TARGETS[@]}"; do
      [ "${t%%|*}" = "$want" ] && found="$t"
    done
    [ -n "$found" ] || { say "error: unknown target '$want'"; exit 2; }
    printf '%s\n' "$found"
  done
}

# Validate target arguments BEFORE they are consumed via process substitution.
#
# `targets_filtered` exits 2 on an unknown name, but every caller feeds it as
# `< <(targets_filtered ...)` — a subshell, so that `exit 2` kills only the
# subshell and the parent keeps going with an empty target list. The result was
# `gpg-signing.sh verify typo` printing a clean report for zero repos and
# exiting 0: the one invocation most likely to be mistyped was the one that
# silently succeeded. Call this first; it exits in the CURRENT shell.
require_known_targets() {
  local want t found
  for want in "$@"; do
    found=""
    for t in "${TARGETS[@]}"; do
      [ "${t%%|*}" = "$want" ] && found="$t"
    done
    if [ -z "$found" ]; then
      say "error: unknown target '$want'"
      say "known targets: $(printf '%s ' "${TARGETS[@]%%|*}")"
      exit 2
    fi
  done
}

secret_scope() {  # $1 = env column
  [ -n "$1" ] && printf -- '--env\n%s\n' "$1" || true
}


# ── seed ─────────────────────────────────────────────────────────────────────
# The one interactive step. Exports the secret key (which needs an unlock the
# agent cache cannot provide) and stores it with the passphrase in the keychain.
cmd_seed() {
  need gpg; need security
  say "This asks for your signing-key passphrase ONCE. It cannot be recovered"
  say "from gpg-agent's cache — only you can supply it."
  # Restore echo on ANY exit from this function. Without the trap, Ctrl-C (or
  # `set -e` firing) between `stty -echo` and `stty echo` left the operator's
  # terminal with echo off for the rest of the session — the password they
  # typed next was invisible, and nothing would turn it back on.
  trap 'stty echo 2>/dev/null || true' EXIT INT TERM
  printf 'passphrase (input hidden): '
  local pass
  stty -echo 2>/dev/null || true
  IFS= read -r pass
  stty echo 2>/dev/null || true
  trap - EXIT INT TERM
  printf '\n'
  [ -n "$pass" ] || { say "error: empty passphrase"; exit 2; }

  say "exporting the secret key…"
  local armored
  # Feed the passphrase on stdin instead of argv: `--passphrase "$pass"` puts
  # the secret in the process table, where every other local user can read it
  # with `ps` for the lifetime of the gpg process.
  armored="$(printf '%s' "$pass" | gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 \
                   --armor --export-secret-keys "$KEY_GRIP_HINT" 2>/dev/null || true)"
  # A failed unlock can still exit 0, so the only honest test is a non-empty
  # export that actually contains a private-key block.
  if [ -z "$armored" ] || ! printf '%s' "$armored" | grep -q 'BEGIN PGP PRIVATE KEY BLOCK'; then
    say "error: the export produced no private key block — passphrase probably wrong"
    exit 1
  fi
  security add-generic-password -U -s "$KEYCHAIN_SERVICE" -a private-key -w "$armored" >/dev/null
  # `security` has no stdin form for -w, so this one value necessarily appears
  # in argv. It is a single short-lived invocation; the gpg call above, which
  # runs much longer, no longer leaks the passphrase that way.
  security add-generic-password -U -s "$KEYCHAIN_SERVICE" -a passphrase  -w "$pass"     >/dev/null
  unset pass armored
  ok "private key + passphrase stored in keychain as service '$KEYCHAIN_SERVICE'"
  say "next: $0 install"
}

# ── install ──────────────────────────────────────────────────────────────────
cmd_install() {
  # Validate in THIS shell first: the target loop below runs
  # `targets_filtered` inside `< <(...)`, where its `exit 2` only kills the
  # subshell — `install typo` would print nothing and exit 0. Do it before the
  # `need` checks so a typo is reported identically on every platform (CI has
  # no macOS `security`).
  require_known_targets "$@"
  need gh; need security
  local key pass
  key="$(security find-generic-password -s "$KEYCHAIN_SERVICE" -a private-key -w 2>/dev/null || true)"
  pass="$(security find-generic-password -s "$KEYCHAIN_SERVICE" -a passphrase  -w 2>/dev/null || true)"
  if [ -z "$key" ] || [ -z "$pass" ]; then
    say "error: no keychain entry for '$KEYCHAIN_SERVICE' (private-key / passphrase)."
    say "run: $0 seed"
    exit 1
  fi
  local repo dir env
  while IFS='|' read -r repo dir env; do
    printf '%s\n' "$repo"
    local -a scope=()
    [ -n "$env" ] && scope=(--env "$env")
    printf '%s' "$key"  | gh secret set GPG_PRIVATE_KEY  "${scope[@]}" --repo "jingzhao-l/$repo" >/dev/null
    printf '%s' "$pass" | gh secret set GPG_PASSPHRASE "${scope[@]}" --repo "jingzhao-l/$repo" >/dev/null
    ok "GPG_PRIVATE_KEY + GPG_PASSPHRASE set${env:+ (environment '$env')}"
  done < <(targets_filtered "$@")
  unset key pass
}

# ── verify ───────────────────────────────────────────────────────────────────
# GitHub will not say whether a secret's value is right, so this reports
# presence and shape, and states the limit instead of implying more.
cmd_verify() {
  need gh; need gpg
  require_known_targets "$@"
  local fails=0
  printf '\n== local key ==\n'
  if gpg --list-secret-keys "$KEY_GRIP_HINT" >/dev/null 2>&1; then
    ok "secret key present ($KEY_GRIP_HINT)"
  else
    bad "no secret key $KEY_GRIP_HINT in the local keyring"; fails=1
  fi
  if security find-generic-password -s "$KEYCHAIN_SERVICE" -a private-key -w >/dev/null 2>&1; then
    ok "keychain entry '$KEYCHAIN_SERVICE' present"
  else
    warn "no keychain entry — run '$0 seed' before 'install'"
  fi

  printf '\n== per-repo ==\n'
  local repo dir env
  while IFS='|' read -r repo dir env; do
    printf '%s\n' "$repo"
    local names
    if [ -n "$env" ]; then
      names="$(gh api "repos/jingzhao-l/$repo/environments/$env/secrets" --jq '.secrets[].name' 2>/dev/null || true)"
    fi
    if [ -z "$names" ]; then
      names="$(gh api "repos/jingzhao-l/$repo/actions/secrets" --jq '.secrets[].name' 2>/dev/null || true)"
      if [ -n "$names" ] && [ -n "$env" ]; then
        warn "  secrets exist at repo level, but the workflow declares environment '$env'"
      fi
    fi
    for want in GPG_PRIVATE_KEY GPG_PASSPHRASE; do
      if printf '%s' "$names" | grep -qx "$want"; then ok "$want"; else bad "$want missing${env:+ (environment '$env')}"; fails=1; fi
    done
    # A subproject inside a monorepo (iterate-harness lives in iterate-skill)
    # is not a checkout of its own; the config belongs to the enclosing repo.
    local root
    root="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null || true)"
    if [ -n "$root" ]; then ok "git root $root"; else warn "not in a git checkout: $dir"; fi
  done < <(targets_filtered "$@")
  cat <<'NOTE'

  Unprovable from here: whether each secret's *value* is correct (GitHub secrets
  are write-only) and whether the passphrase matches the key. A clean run means
  the plumbing is right, not that the next release will sign.
NOTE
  # A checker nobody has watched fail is a checker nobody can trust: every
  # `bad` above used to be cosmetic, so `verify` exited 0 with missing secrets
  # and CI could not gate on it.
  if [ "$fails" -eq 0 ]; then
    printf '\nverify: all checks passed\n'
    return 0
  fi
  printf '\nverify: FAILED (see MISS lines above)\n' >&2
  return 1
}

# ── local ────────────────────────────────────────────────────────────────────
cmd_local() {
  local gpg_bin=""
  if command -v gpg >/dev/null 2>&1; then
    gpg_bin="$(command -v gpg)"
  else
    for c in /opt/homebrew/bin/gpg /usr/local/bin/gpg /usr/bin/gpg; do
      [ -x "$c" ] && { gpg_bin="$c"; break; }
    done
    warn "gpg not on PATH; looked in the usual Homebrew locations"
  fi
  local -a dirs=()
  if [ $# -eq 0 ]; then
    local repo dir env
    while IFS='|' read -r repo dir env; do dirs+=("$dir"); done < <(targets_filtered)
  else
    dirs=("$@")
  fi
  local d
  for d in "${dirs[@]}"; do
    # `.git` is a directory in a normal clone and a *file* in a linked worktree,
    # so -d alone silently skips exactly the checkouts that need this most.
    # Resolve the enclosing repo: for a monorepo subproject this is the root,
    # and that is where git config has to be written. `.git` is a directory in
    # a clone and a file in a linked worktree, so never test it with -d alone.
    local root label
    root="$(git -C "$d" rev-parse --show-toplevel 2>/dev/null || true)"
    if [ -z "$root" ]; then warn "$d is not in a git checkout"; continue; fi
    label="$(basename "$d")"
    [ "$root" != "$d" ] && label="$(basename "$root") (for $label)"
    git -C "$root" config commit.gpgsign true
    git -C "$root" config tag.gpgsign true
    git -C "$root" config gpg.format openpgp
    git -C "$root" config user.signingkey "$KEY_GRIP_HINT"
    # gpg.program must be absolute. Homebrew's gpg is not on the default PATH,
    # and `git commit` then fails with the unhelpful "cannot run gpg: No such
    # file or directory" — which reads like a missing key, not a missing PATH.
    if [ -n "$gpg_bin" ]; then
      git -C "$root" config gpg.program "$gpg_bin"
    fi
    ok "$label: commit.gpgsign/tag.gpgsign=true signingkey=$KEY_GRIP_HINT${gpg_bin:+ gpg.program=$gpg_bin}"
  done
}

# ── audit ────────────────────────────────────────────────────────────────────
# The failure that started this: `if: secrets.GPG_PRIVATE_KEY != ''` turns an
# unsigned release into a release that looks successful.
cmd_audit() {
  need gh
  require_known_targets "$@"
  printf '\n== silent-skip signing in release workflows ==\n'
  local repo dir env any=0 inspected=0 fails=0 wf
  while IFS='|' read -r repo dir env; do
    for wf in release.yml publish.yml; do
      # Capture gh's exit status *and* stderr. The old `gh ... 2>/dev/null |
      # base64 -d || true` collapsed "file absent" (a normal skip) and "network
      # down / auth expired / rate limited" (the audit is blind) into the same
      # empty string, then `[ -n "$body" ] || continue` skipped both and printed
      # "audit: passed" without having inspected a single workflow.
      local out rc=0
      out="$(gh api "repos/jingzhao-l/$repo/contents/.github/workflows/$wf" --jq '.content' 2>&1)" || rc=$?
      if [ "$rc" -ne 0 ]; then
        if printf '%s' "$out" | grep -qE 'HTTP 404|Not Found'; then
          continue
        fi
        bad "$repo/$wf: could not read workflow (gh exit $rc)"
        printf '%s\n' "$out" | sed 's/^/      /' >&2
        fails=1
        continue
      fi
      local body
      if ! body="$(printf '%s' "$out" | base64 -d 2>/dev/null)"; then
        bad "$repo/$wf: workflow content is not valid base64"
        fails=1
        continue
      fi
      if [ -z "$body" ]; then
        bad "$repo/$wf: workflow content is empty"
        fails=1
        continue
      fi
      inspected=$((inspected + 1))
      # Strip comment lines first. A workflow that documents *why* it removed
      # the silent-skip still contains the string, and reporting that as a live
      # skip trains people to ignore this command — the same mistake a linter
      # makes when it greps its own explanation.
      local live
      live="$(printf '%s\n' "$body" | grep -vE '^[[:space:]]*#' || true)"
      if printf '%s' "$live" | grep -qE 'if: *\$\{\{ *secrets\.GPG_PRIVATE_KEY'; then
        printf '  %s/%s\n' "$repo" "$wf"
        printf '%s' "$live" | grep -nE 'if: *\$\{\{ *secrets\.GPG_PRIVATE_KEY' | sed 's/^/      /'
        any=1
      fi
    done
  done < <(targets_filtered "$@")
  # Zero inspected workflows is never a pass: it means every read failed, or
  # every repo legitimately has no release workflow. Both deserve a look, and
  # the second is a target-list bug rather than a green result.
  if [ "$inspected" -eq 0 ] && [ "$fails" -eq 0 ]; then
    bad "no release workflows were inspected — refusing to report a pass"
    fails=1
  fi
  [ "$any" -eq 1 ] || ok "no silent-skip signing found"
  cat <<'NOTE'

  Each line above means: when the secret is missing, the whole signing step
  vanishes and the release still publishes. GlassPane's release.yml is the
  reference shape — it fails with a remedy instead. That difference is why its
  commits verify and the others' do not.
NOTE
  # Exit non-zero when a silent-skip was found, so CI/a pre-push hook can gate
  # on it. Finding one and exiting 0 made `audit` a report nobody had to read —
  # exactly the class of silent success the audit itself exists to catch.
  if [ "$any" -eq 1 ]; then
    printf '\naudit: FAILED (silent-skip signing found)\n' >&2
    return 1
  fi
  if [ "$fails" -ne 0 ]; then
    printf '\naudit: FAILED (could not inspect every target)\n' >&2
    return 1
  fi
  printf '\naudit: passed (%d workflow(s) inspected)\n' "$inspected"
  return 0
}

# ── selftest ─────────────────────────────────────────────────────────────────
# A checker nobody has watched fail is a checker nobody can trust. These assert
# the guards actually trip.
cmd_selftest() {
  local fails=0 repo dir env
  printf '\n== selftest ==\n'
  while IFS='|' read -r repo dir env; do
    if [ -z "$repo" ] || [ -z "$dir" ]; then bad "malformed target row: '$repo|$dir|$env'"; fails=1; fi
  done < <(targets_filtered)
  [ "$fails" -eq 0 ] && ok "every target row parses as repo|dir|env"

  # the env column must be either empty (repo-level) or a bare name — a value
  # with a stray space would silently build a bogus --env argument
  while IFS='|' read -r repo dir env; do
    case "$env" in
      ""|release) ;;
      *) bad "$repo: unexpected environment '$env'"; fails=1 ;;
    esac
  done < <(targets_filtered)
  [ "$fails" -eq 0 ] && ok "environment column is repo-level or 'release'"

  # An unknown repo must produce no target row, not a silent empty install.
  # Note: this cannot be written as `if ! targets_filtered ...` — that runs in a
  # subshell where the function's `exit 2` never reaches us, so the test would
  # pass for the wrong reason. Assert on the output instead.
  # `set -e` is on, and a command substitution that fails inside an assignment
  # aborts the script even with `|| true` appended to the substitution — so each
  # call is wrapped in its own subshell whose failure is the test's subject.
  local rows
  rows="$( ( targets_filtered definitely-not-a-repo 2>/dev/null ) || true )"
  if [ -z "$rows" ]; then ok "unknown target yields no target row"
  else bad "unknown target produced a row: $rows"; fails=1; fi
  rows="$( ( targets_filtered GlassPane 2>/dev/null ) || true )"
  case "$rows" in GlassPane\|*) ok "a known target resolves to its row" ;;
                *) bad "known target did not resolve (got '$rows')"; fails=1 ;; esac

  # `require_known_targets` is what actually guards the CALLERS: targets_filtered
  # runs inside `< <(...)` process substitution, so its `exit 2` only killed the
  # subshell and the parent carried on with zero repos — `verify typo` printed a
  # clean report and exited 0. Assert it exits 2 in the current shell.
  # `|| rc=$?` is required: under `set -e` a bare failing command aborts the
  # selftest before `rc` is ever assigned (the file already documents this trap).
  local rc
  rc=0; ( require_known_targets definitely-not-a-repo ) >/dev/null 2>&1 || rc=$?
  if [ "$rc" -eq 2 ]; then ok "require_known_targets rejects an unknown target with exit 2"
  else bad "require_known_targets exited $rc for an unknown target (want 2)"; fails=1; fi
  rc=0; ( require_known_targets GlassPane ) >/dev/null 2>&1 || rc=$?
  if [ "$rc" -eq 0 ]; then ok "require_known_targets accepts a known target"
  else bad "require_known_targets rejected known target (exit $rc)"; fails=1; fi

  # The audit pattern must match a real silent-skip and NOT match the fixed
  # form. Built with printf rather than hand-escaped quoting: the YAML
  # expression is full of quotes and braces, and escaping it by hand is
  # itself a bug source (it broke this file once already).
  local skip fixed
  skip=$(printf '        if: ${{ secrets.GPG_PRIVATE_KEY != %s }}' "''")
  fixed='          if [ -z "${GPG_INPUT_KEY:-}" ]; then'
  if printf '%s' "$skip"   | grep -qE 'if: *\$\{\{ *secrets\.GPG_PRIVATE_KEY'; then ok "audit matches the silent-skip form"
  else bad "audit fails to match the silent-skip form"; fails=1; fi
  if printf '%s' "$fixed" | grep -qE 'if: *\$\{\{ *secrets\.GPG_PRIVATE_KEY'; then bad "audit false-positives on the fail-loud form"; fails=1
  else ok "audit does not flag the fail-loud form"; fi

  # A comment that merely quotes the old pattern must not count as a live skip.
  # This guard exists because it bit once: glasspane-harness's release.yml
  # explains *why* the silent-skip was removed, and the audit reported that
  # explanation as a violation.
  local commented
  commented=$(printf '      # the old\n      # if: ${{ secrets.GPG_PRIVATE_KEY != %s }}\n' "''")
  if printf '%s' "$commented" | grep -vE '^[[:space:]]*#' | grep -qE 'if: *\$\{\{ *secrets\.GPG_PRIVATE_KEY'; then
    bad "audit counts commented-out lines as violations"; fails=1
  else ok "audit ignores the pattern when it appears only in comments"; fi

  [ "$fails" -eq 0 ] && printf '\nselftest passed\n' || { printf '\nselftest FAILED\n'; exit 1; }
}

case "${1:-}" in
  seed)     shift; cmd_seed "$@" ;;
  install)  shift; cmd_install "$@" ;;
  verify)   shift; cmd_verify "$@" ;;
  local)    shift; cmd_local "$@" ;;
  audit)    shift; cmd_audit "$@" ;;
  selftest) shift; cmd_selftest "$@" ;;
  *) sed -n '2,34p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
esac
