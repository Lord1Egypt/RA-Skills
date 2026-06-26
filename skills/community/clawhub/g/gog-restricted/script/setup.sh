#!/bin/bash
set -euo pipefail

: "${HOME:?HOME must be set to install the wrapper}"

GOG_BIN="$(type -P gog || true)"
if [[ -z "$GOG_BIN" ]]; then
  echo "Error: gog binary not found in PATH" >&2
  exit 1
fi
if [[ ! -x "$GOG_BIN" ]]; then
  echo "Error: $GOG_BIN is not an executable file" >&2
  exit 1
fi

WRAPPER_VERSION=2

# --- Pick an install dir that's already on PATH and writable by the user ---
# Honours $GOG_RESTRICTED_INSTALL_DIR if set; otherwise scans PATH entries in
# this preference order. This sidesteps HOME/profile mismatches (e.g. agent
# runtimes that override HOME to a profile dir not reflected in PATH).
WRAPPER_DIR=""
if [[ -n "${GOG_RESTRICTED_INSTALL_DIR:-}" ]]; then
  WRAPPER_DIR="$GOG_RESTRICTED_INSTALL_DIR"
else
  for candidate in \
    "${HOME}/.local/bin" \
    "${HOME}/bin" \
    "/opt/homebrew/bin" \
    "/usr/local/bin"; do
    case ":$PATH:" in
      *":$candidate:"*) ;;
      *) continue ;;
    esac
    [[ -d "$candidate" && -w "$candidate" ]] || continue
    WRAPPER_DIR="$candidate"
    break
  done
fi

if [[ -z "$WRAPPER_DIR" ]]; then
  echo "Error: no writable, user-owned directory found on PATH." >&2
  echo "Candidates checked: \$HOME/.local/bin, \$HOME/bin, /opt/homebrew/bin, /usr/local/bin." >&2
  echo "Either add one of these to PATH and make it writable, or set" >&2
  echo "GOG_RESTRICTED_INSTALL_DIR=<dir> to install to a specific location." >&2
  exit 1
fi

WRAPPER_BIN="${WRAPPER_DIR}/gog-restricted"

mkdir -p "$WRAPPER_DIR"

if [[ ! -w "$WRAPPER_DIR" ]]; then
  echo "Error: ${WRAPPER_DIR} is not writable by $(whoami)." >&2
  exit 1
fi

# Verify the chosen dir is actually on PATH (catches GOG_RESTRICTED_INSTALL_DIR
# overrides that point somewhere PATH doesn't see).
case ":$PATH:" in
  *":$WRAPPER_DIR:"*) ;;
  *)
    echo "Error: ${WRAPPER_DIR} is not on your PATH." >&2
    echo "Add it to PATH and re-run, or choose a different install dir." >&2
    exit 1
    ;;
esac

# --- Idempotency / safety guard ---
# Anchored marker on line 2 of an existing wrapper; refuse to clobber anything else.
if [[ -L "$WRAPPER_BIN" ]]; then
  echo "Error: $WRAPPER_BIN is a symlink; refusing to write through it. Remove it manually." >&2
  exit 1
fi
if [[ -e "$WRAPPER_BIN" ]]; then
  if [[ ! -f "$WRAPPER_BIN" ]]; then
    echo "Error: $WRAPPER_BIN exists and is not a regular file." >&2
    exit 1
  fi
  if [[ ! -r "$WRAPPER_BIN" || ! -w "$WRAPPER_BIN" ]]; then
    echo "Error: $WRAPPER_BIN exists but is not readable/writable by $(whoami)." >&2
    exit 1
  fi
  if ! head -n 2 "$WRAPPER_BIN" | grep -q "^# GOG_RESTRICTED_WRAPPER v="; then
    echo "Error: $WRAPPER_BIN exists and is not a gog-restricted wrapper." >&2
    echo "Refusing to overwrite. Inspect or remove it manually." >&2
    exit 1
  fi
fi

# --- Atomic install: write to tmp, chmod, rename ---
TMP_BIN="$(mktemp "${WRAPPER_BIN}.XXXXXX")"
trap 'rm -f "$TMP_BIN"' EXIT

# Write shebang, marker line, and GOG_REAL (shell-escaped) with expansion.
{
  echo '#!/bin/bash'
  printf '# GOG_RESTRICTED_WRAPPER v=%d\n' "$WRAPPER_VERSION"
  echo 'set -euo pipefail'
  echo ''
  printf 'GOG_REAL=%q\n' "$GOG_BIN"
} > "$TMP_BIN"

cat >> "$TMP_BIN" << 'WRAPPER'
ORIG_ARGS=("$@")

# ---------------------------------------------------------------------------
# Parse positional args only — long flags consume their value, short flags do
# not. Bare `--` ends option processing. Allowlist is strict: every allowed
# (sub)command is enumerated by its full 3-word, 2-word, or help/version form.
# ---------------------------------------------------------------------------
POSITIONAL=()
HAS_HELP=false
HAS_VERSION=false
END_OF_OPTS=false

while [[ $# -gt 0 ]]; do
  if [[ "$END_OF_OPTS" == true ]]; then
    POSITIONAL+=("$1")
    shift
    continue
  fi
  case "$1" in
    --)
      END_OF_OPTS=true
      shift
      ;;
    --help|-h)
      HAS_HELP=true
      shift
      ;;
    --version)
      HAS_VERSION=true
      shift
      ;;
    --*=*)
      shift
      ;;
    --*)
      shift
      [[ $# -gt 0 ]] && shift
      ;;
    -*)
      # Unknown short flag; refuse rather than guess whether it consumes a value.
      echo "BLOCKED: short flag '$1' is not allowed (use the long form)." >&2
      exit 1
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

NPOS=${#POSITIONAL[@]}
P0="${POSITIONAL[0]:-}"
P1="${POSITIONAL[1]:-}"
P2="${POSITIONAL[2]:-}"

ALLOWED=false

# --- 3-word allowlist (strict; no namespace fall-through for these) ---
if [[ $NPOS -ge 3 ]]; then
  case "$P0 $P1 $P2" in
    "gmail messages search"|\
    "gmail thread modify"|\
    "gmail thread attachments"|\
    "gmail batch modify"|\
    "gmail labels list"|\
    "gmail labels get"|\
    "gmail labels create"|\
    "gmail labels add"|\
    "gmail labels remove"|\
    "gmail labels modify"|\
    "calendar acl list")
      ALLOWED=true ;;
  esac
fi

# --- 2-word allowlist (only for namespaces with no destructive verbs) ---
if [[ "$ALLOWED" == false && $NPOS -ge 2 ]]; then
  case "$P0 $P1" in
    "auth status"|\
    "auth list"|\
    "auth services"|\
    "gmail search"|\
    "gmail read"|\
    "gmail get"|\
    "gmail attachment"|\
    "gmail url"|\
    "gmail history"|\
    "calendar create"|\
    "calendar list"|\
    "calendar get"|\
    "calendar event"|\
    "calendar events"|\
    "calendar calendars"|\
    "calendar search"|\
    "calendar freebusy"|\
    "calendar conflicts"|\
    "calendar colors"|\
    "calendar time"|\
    "calendar users"|\
    "calendar team")
      ALLOWED=true ;;
  esac
fi

# --- Block known-destructive verbs under 2-word allowlist namespaces ---
# Even though the 2-word allows for `calendar event[s]` are needed for the
# documented get/list shape, write verbs nested there must be refused.
if [[ "$ALLOWED" == true && $NPOS -ge 3 ]]; then
  case "$P0 $P1 $P2" in
    "calendar event update"|\
    "calendar event delete"|\
    "calendar event patch"|\
    "calendar event insert"|\
    "calendar event move"|\
    "calendar event import"|\
    "calendar events update"|\
    "calendar events delete"|\
    "calendar events patch"|\
    "calendar events insert"|\
    "calendar events move"|\
    "calendar events import"|\
    "gmail attachment upload"|\
    "gmail attachment delete")
      echo "BLOCKED: '$P0 $P1 $P2' is a destructive subcommand and is not allowed." >&2
      exit 1 ;;
  esac
fi

# --- --help for known group prefixes (exact positional count) ---
if [[ "$ALLOWED" == false && "$HAS_HELP" == true ]]; then
  case "$NPOS" in
    0) ALLOWED=true ;;
    1) case "$P0" in
         gmail|auth|calendar) ALLOWED=true ;;
       esac ;;
    2) case "$P0 $P1" in
         "gmail messages"|"gmail labels"|"gmail batch"|"gmail thread"|"calendar acl") ALLOWED=true ;;
       esac ;;
  esac
fi

# --- --version (top-level only) ---
if [[ "$ALLOWED" == false && "$HAS_VERSION" == true && $NPOS -eq 0 ]]; then
  ALLOWED=true
fi

# --- calendar create flag allowlist (fail-closed) ---
# Only the flags documented in SKILL.md may be passed. Anything else (including
# argparse-prefix variants like --att, undocumented egress flags like
# --conference-data, or capitalised variants) is refused.
# Allowlisted flags: SKILL.md "Safe flags" + general-purpose --json/--no-input/--account.
# Non-flag tokens (positionals and values consumed by long flags) are passed through.
if [[ "$ALLOWED" == true && "$P0" == "calendar" && "$P1" == "create" ]]; then
  for arg in "${ORIG_ARGS[@]}"; do
    case "$arg" in
      --summary|--summary=*|\
      --from|--from=*|\
      --to|--to=*|\
      --description|--description=*|\
      --location|--location=*|\
      --all-day|\
      --rrule|--rrule=*|\
      --reminder|--reminder=*|\
      --event-color|--event-color=*|\
      --visibility|--visibility=*|\
      --transparency|--transparency=*|\
      --json|\
      --no-input|\
      --account|--account=*|\
      ''|[!-]*)
        ;;
      *)
        echo "BLOCKED: flag '$arg' is not in the calendar-create allowlist." >&2
        exit 1
        ;;
    esac
  done
fi

if [[ "$ALLOWED" == true ]]; then
  exec "$GOG_REAL" "${ORIG_ARGS[@]}"
fi

echo "BLOCKED: this command is not in the allowlist." >&2
exit 1
WRAPPER

chmod +x "$TMP_BIN"
mv -f "$TMP_BIN" "$WRAPPER_BIN"
trap - EXIT

echo "Security wrapper v${WRAPPER_VERSION} installed at $WRAPPER_BIN"
echo "Wraps real gog at $GOG_BIN"
