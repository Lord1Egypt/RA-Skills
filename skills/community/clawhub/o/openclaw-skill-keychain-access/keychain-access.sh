#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME=$(basename "$0")
DRY_RUN=false
ASSUME_YES=false
SHOW_RAW=false
KEYCHAIN=""
SERVICE=""
ACCOUNT=""
PASSWORD=""
PASSWORD_SET=false
PASSWORD_SOURCE=""
PASSWORD_ENV_VAR=""

error() {
  echo "$SCRIPT_NAME: $1" >&2
  exit 1
}

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME <operation> [options]
Operations:
  list    [--keychain PATH] [--service NAME] [--account NAME] [--dry-run]
  get     --service NAME --account NAME [--keychain PATH] [--raw] [--dry-run]
  set     --service NAME --account NAME --password VALUE [--keychain PATH] [--yes] [--dry-run]
  delete  --service NAME --account NAME [--keychain PATH] [--yes] [--dry-run]
Options:
  --keychain PATH    Specify a custom keychain file to target.
  --service NAME     Service name to match.
  --account NAME     Account name to match.
  --password VALUE   (Deprecated/insecure) Password for set; prefer --password-stdin, --password-env, or the hidden prompt.
  --password-stdin   Read the password from stdin (pipe the secret securely).
  --password-env VAR Read the named env var (then unset it) so the secret never appears on the command line.
  --raw              Reveal the password on get; otherwise the password line is redacted.
  --yes              Skip confirmation prompts for set (update) or delete.
  --dry-run          Display which security command would run without contacting the keychain.
  --help, -h         Show this message.
Hint: use --service/--account filters to keep the operation unambiguous, and only use --raw when the user explicitly needs the secret value.
EOF
}

command_exists() {
  command -v security >/dev/null 2>&1
}

warn_insecure_password_flag() {
  echo "$SCRIPT_NAME: Warning: --password passes secrets on the command line, which is insecure. Use --password-stdin, --password-env, or the prompt instead." >&2
}

prepare_password() {
  if $PASSWORD_SET; then
    return
  fi
  case "$PASSWORD_SOURCE" in
    stdin)
      if [[ -t 0 ]]; then
        error "--password-stdin requires piped input; stdin is a terminal."
      fi
      PASSWORD=$(cat)
      PASSWORD_SET=true
      ;;
    env)
      if [[ -z "${PASSWORD_ENV_VAR}" ]]; then
        error "--password-env requires a variable name."
      fi
      if [[ -z "${!PASSWORD_ENV_VAR+x}" ]]; then
        error "Environment variable '$PASSWORD_ENV_VAR' is not set."
      fi
      PASSWORD="${!PASSWORD_ENV_VAR}"
      unset "$PASSWORD_ENV_VAR" >/dev/null 2>&1 || true
      PASSWORD_SET=true
      ;;
    *)
      if [[ ! -t 0 ]]; then
        error "No password source provided; use --password-stdin with piped input or --password-env with a secure env var."
      fi
      read -rsp "Password: " PASSWORD
      echo
      PASSWORD_SET=true
      ;;
  esac
}

prompt_confirmation() {
  local prompt_message="$1"
  if $ASSUME_YES; then
    return 0
  fi
  read -rp "$prompt_message [y/N]: " response
  case "$response" in
    [yY][eE][sS]|[yY]) return 0 ;;
    *) return 1 ;;
  esac
}

require_service_account() {
  if [[ -z "$SERVICE" ]]; then
    error "--service is required for the '$OPERATION' operation."
  fi
  if [[ -z "$ACCOUNT" ]]; then
    error "--account is required for the '$OPERATION' operation."
  fi
}

list_command() {
  local keychain_args=()
  [[ -n "$KEYCHAIN" ]] && keychain_args+=("$KEYCHAIN")
  if $DRY_RUN; then
    printf "Dry run: security dump-keychain %s" "${keychain_args[*]:-<default search list>}"
    [[ -n "$SERVICE" ]] && printf " --service filter: %s" "$SERVICE"
    [[ -n "$ACCOUNT" ]] && printf " --account filter: %s" "$ACCOUNT"
    echo
    return 0
  fi

  local dump_output
  if ! dump_output=$(security dump-keychain "${keychain_args[@]}" 2>/dev/null); then
    echo "No entries found or keychain could not be read." >&2
    return 1
  fi

  local tmpfile
  tmpfile=$(mktemp)
  trap "rm -f '$tmpfile'" EXIT
  printf "%s" "$dump_output" > "$tmpfile"
  local rows
  rows=$(python3 - "$SERVICE" "$ACCOUNT" "$tmpfile" <<'PY'
import sys, re
filter_service = sys.argv[1]
filter_account = sys.argv[2]
filepath = sys.argv[3]
current_keychain = "(default search list)"
entry = None

def flush(entry):
    if not entry:
        return
    service = entry.get('srvr') or entry.get('svce') or entry.get('service')
    account = entry.get('acct')
    if not service and not account:
        return
    if filter_service and (not service or filter_service not in service):
        return
    if filter_account and (not account or filter_account not in account):
        return
    desc = entry.get('desc') or entry.get('labl') or ''
    keychain = entry.get('keychain') or current_keychain
    print(f"{service or 'n/a'} | {account or 'n/a'} | {desc or 'n/a'} | {keychain}")

def match_attr(line):
    m = re.match(r'"([^\"]+)"<blob>="(.*)"', line)
    if m:
        return m.group(1), m.group(2)
    return None, None

with open(filepath, 'r', encoding='utf-8', errors='ignore') as handle:
    for raw_line in handle:
        line = raw_line.strip()
        if line.startswith('keychain:'):
            current_keychain = line.split(':', 1)[1].strip().strip('"')
            continue
        if line.startswith('class:'):
            flush(entry)
            entry = {'keychain': current_keychain}
            continue
        if not line:
            continue
        name, value = match_attr(line)
        if not name:
            continue
        entry[name] = value
flush(entry)
PY
)
  trap - EXIT
  rm -f "$tmpfile"

  if [[ -z "$rows" ]]; then
    echo "No matching entries found."
    return 0
  fi
  echo "$rows"
}

get_command() {
  require_service_account
  local keychain_args=()
  [[ -n "$KEYCHAIN" ]] && keychain_args+=("$KEYCHAIN")
  local cmd=(security find-generic-password -s "$SERVICE" -a "$ACCOUNT" -g)
  cmd+=("${keychain_args[@]}")
  if $DRY_RUN; then
    printf "Dry run: %s" "${cmd[*]}"
    echo
    return 0
  fi
  local output
  if ! output=$("${cmd[@]}" 2>&1); then
    echo "$output" >&2
    error "Unable to read the requested credential (ensure the service/account exists and the keychain is unlocked)."
  fi
  if ! $SHOW_RAW; then
    output=$(printf "%s" "$output" | sed -E 's/(password: ).*/\1[REDACTED]/I')
  fi
  echo "$output"
}

set_command() {
  require_service_account
  local keychain_args=()
  [[ -n "$KEYCHAIN" ]] && keychain_args+=("$KEYCHAIN")
  if $DRY_RUN; then
    printf "Dry run: security add-generic-password -s '%s' -a '%s' -w '[REDACTED]'" "$SERVICE" "$ACCOUNT"
    [[ -n "$KEYCHAIN" ]] && printf " %s" "$KEYCHAIN"
    echo
    return 0
  fi
  prepare_password
  if ! $PASSWORD_SET; then
    error "A password is required for the set operation. Provide one via --password-stdin, --password-env, or the hidden prompt."
  fi
  if security find-generic-password -s "$SERVICE" -a "$ACCOUNT" "${keychain_args[@]}" >/dev/null 2>&1; then
    if ! prompt_confirmation "An entry for service '$SERVICE' account '$ACCOUNT' already exists and will be updated. Continue?"; then
      echo "Update aborted."
      exit 0
    fi
  fi
  local cmd=(security add-generic-password -s "$SERVICE" -a "$ACCOUNT" -w "$PASSWORD" -U)
  cmd+=("${keychain_args[@]}")
  if ! "${cmd[@]}"; then
    error "Failed to store the credential."
  fi
  echo "Stored credential for '$SERVICE' / '$ACCOUNT'."
}

delete_command() {
  require_service_account
  local keychain_args=()
  [[ -n "$KEYCHAIN" ]] && keychain_args+=("$KEYCHAIN")
  if $DRY_RUN; then
    printf "Dry run: security delete-generic-password -s '%s' -a '%s'" "$SERVICE" "$ACCOUNT"
    [[ -n "$KEYCHAIN" ]] && printf " %s" "$KEYCHAIN"
    echo
    return 0
  fi
  if ! security find-generic-password -s "$SERVICE" -a "$ACCOUNT" "${keychain_args[@]}" >/dev/null 2>&1; then
    error "No entry found for service '$SERVICE' account '$ACCOUNT'."
  fi
  if ! prompt_confirmation "Delete the entry for '$SERVICE' / '$ACCOUNT'?"; then
    echo "Deletion aborted."
    exit 0
  fi
  if ! security delete-generic-password -s "$SERVICE" -a "$ACCOUNT" "${keychain_args[@]}" >/dev/null 2>&1; then
    error "Failed to delete the credential."
  fi
  echo "Deleted credential for '$SERVICE' / '$ACCOUNT'."
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

OPERATION="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keychain)
      [[ $# -lt 2 ]] && error "--keychain requires a value"
      KEYCHAIN="$2"
      shift 2
      ;;
    --service)
      [[ $# -lt 2 ]] && error "--service requires a value"
      SERVICE="$2"
      shift 2
      ;;
    --account)
      [[ $# -lt 2 ]] && error "--account requires a value"
      ACCOUNT="$2"
      shift 2
      ;;
    --password)
      [[ $# -lt 2 ]] && error "--password requires a value"
      if [[ -n "$PASSWORD_SOURCE" && "$PASSWORD_SOURCE" != "flag" ]]; then
        error "Password source already specified; remove the conflicting option."
      fi
      PASSWORD="$2"
      PASSWORD_SET=true
      PASSWORD_SOURCE="flag"
      warn_insecure_password_flag
      shift 2
      ;;
    --password-stdin)
      if [[ -n "$PASSWORD_SOURCE" ]]; then
        error "Password source already specified; remove the conflicting option."
      fi
      PASSWORD_SOURCE="stdin"
      shift
      ;;
    --password-env)
      [[ $# -lt 2 ]] && error "--password-env requires a variable name"
      if [[ -n "$PASSWORD_SOURCE" ]]; then
        error "Password source already specified; remove the conflicting option."
      fi
      PASSWORD_SOURCE="env"
      PASSWORD_ENV_VAR="$2"
      shift 2
      ;;
    --raw)
      SHOW_RAW=true
      shift
      ;;
    --yes)
      ASSUME_YES=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      error "Unknown option: $1"
      ;;
  esac
done

if ! command_exists; then
  error "The security CLI is required but was not found in PATH."
fi

case "$OPERATION" in
  list)
    list_command
    ;;
  get)
    get_command
    ;;
  set)
    set_command
    ;;
  delete)
    delete_command
    ;;
  *)
    error "Unknown operation: $OPERATION"
    ;;
esac
