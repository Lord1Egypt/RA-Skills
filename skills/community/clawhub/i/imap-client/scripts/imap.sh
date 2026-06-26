#!/usr/bin/env bash
# imap.sh — wrap `myl` with credentials sourced from the environment.
#
# Lookup order for credentials:
#   1. Process env vars (set by OpenClaw skills.entries.imap-client.env, or
#      manually via `export` in the user's shell).
#   2. ~/.config/imap-client/credentials  (must be chmod 600 or 400).
#   3. $IMAP_CREDENTIALS_FILE             (override path; same perms required).
#
# Variables consumed:
#   IMAP_USER          required — login (full email address)
#   IMAP_PASSWORD      required — app-specific password
#   IMAP_PROVIDER      optional — auto (default) | gmail | yandex | mailru | manual
#   IMAP_SERVER        required when IMAP_PROVIDER=manual
#   IMAP_PORT          optional — default 993
#   IMAP_STARTTLS      optional — set to 1 to add --starttls (use only with port 143)
#
# All other arguments are forwarded verbatim to `myl`.

set -euo pipefail

err() { printf '%s\n' "imap.sh: $*" >&2; }

# ---------- 1. Load credentials file if env is incomplete ----------

CRED_FILE="${IMAP_CREDENTIALS_FILE:-$HOME/.config/imap-client/credentials}"

if [[ ( -z "${IMAP_USER:-}" || -z "${IMAP_PASSWORD:-}" ) && -f "$CRED_FILE" ]]; then
  # Refuse to source a world-readable creds file. Permissions check works on
  # both GNU stat (Linux) and BSD stat (macOS).
  perms=$(stat -c '%a' "$CRED_FILE" 2>/dev/null || stat -f '%A' "$CRED_FILE" 2>/dev/null || echo "?")
  case "$perms" in
    600|400)
      # shellcheck disable=SC1090
      . "$CRED_FILE"
      ;;
    *)
      err "WARNING — $CRED_FILE has perms $perms (expected 600 or 400). Ignoring."
      err "Run: chmod 600 \"$CRED_FILE\""
      ;;
  esac
fi

# ---------- 2. Validate ----------

if [[ -z "${IMAP_USER:-}" || -z "${IMAP_PASSWORD:-}" ]]; then
  cat >&2 <<'EOF'
imap.sh: missing credentials.

Set IMAP_USER and IMAP_PASSWORD by ONE of these methods (pick whichever fits
your runtime):

  A. OpenClaw — ~/.openclaw/openclaw.json
     {
       "skills": {
         "entries": {
           "imap-client": {
             "enabled": true,
             "env": {
               "IMAP_USER": "you@example.com",
               "IMAP_PASSWORD": "app-specific-password",
               "IMAP_PROVIDER": "auto"
             }
           }
         }
       }
     }
     Restart the agent session. OpenClaw injects these into env per turn.

  B. Generic shell — export in your terminal (or in ~/.bashrc / ~/.zshrc):
     export IMAP_USER='you@example.com'
     export IMAP_PASSWORD='app-specific-password'
     export IMAP_PROVIDER='auto'    # optional

  C. Credentials file — ~/.config/imap-client/credentials  (chmod 600):
     IMAP_USER='you@example.com'
     IMAP_PASSWORD='app-specific-password'
     IMAP_PROVIDER='auto'           # optional

For provider-specific details (Gmail, Yandex, Mail.ru, iCloud, Fastmail),
see references/authentication.md.
EOF
  exit 2
fi

# ---------- 3. Build connection flags from IMAP_PROVIDER ----------

flags=()

case "${IMAP_PROVIDER:-auto}" in
  gmail|google)
    flags+=(--google)
    ;;

  yandex)
    # Yandex Mail. .com works for both yandex.com and yandex.ru accounts.
    # Override via IMAP_SERVER if you need imap.yandex.ru explicitly.
    flags+=(--server "${IMAP_SERVER:-imap.yandex.com}" --port "${IMAP_PORT:-993}")
    ;;

  mailru|mail.ru)
    flags+=(--server "${IMAP_SERVER:-imap.mail.ru}" --port "${IMAP_PORT:-993}")
    ;;

  manual)
    if [[ -z "${IMAP_SERVER:-}" ]]; then
      err "IMAP_PROVIDER=manual requires IMAP_SERVER to be set."
      exit 2
    fi
    flags+=(--server "$IMAP_SERVER" --port "${IMAP_PORT:-993}")
    [[ "${IMAP_STARTTLS:-0}" == "1" ]] && flags+=(--starttls)
    ;;

  auto|"")
    flags+=(--auto)
    ;;

  *)
    err "Unknown IMAP_PROVIDER='$IMAP_PROVIDER'."
    err "Valid values: auto, gmail, yandex, mailru, manual."
    exit 2
    ;;
esac

flags+=(--username "$IMAP_USER" --password "$IMAP_PASSWORD")

# ---------- 4. Dispatch ----------

if ! command -v myl >/dev/null 2>&1; then
  err "\`myl\` is not on PATH. See references/installation.md."
  exit 127
fi

exec myl "${flags[@]}" "$@"
