#!/bin/zsh
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "restore-root.sh must run as root" >&2
  exit 1
fi

TARGET_USER="${1:-${SUDO_USER:-}}"
if [[ -z "${TARGET_USER}" || "${TARGET_USER}" == "root" ]]; then
  TARGET_USER="$(stat -f '%Su' /dev/console 2>/dev/null || true)"
fi

if [[ -z "${TARGET_USER}" || "${TARGET_USER}" == "root" ]]; then
  echo "Unable to determine the logged-in user" >&2
  exit 1
fi

BACKUP_ROOT="/Users/${TARGET_USER}/Desktop/.codex-backups/macos-connectivity-restore"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${BACKUP_ROOT}/${STAMP}"
mkdir -p "${BACKUP_DIR}"

create_empty_plist() {
  local path="$1"
  mkdir -p "$(dirname "${path}")"
  cat > "${path}" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
</dict>
</plist>
EOF
}

backup_file() {
  local source_path="$1"
  local backup_name="$2"
  if [[ -f "${source_path}" ]]; then
    cp -p "${source_path}" "${BACKUP_DIR}/${backup_name}"
  fi
}

set_bool_key() {
  local path="$1"
  local key="$2"
  local value="$3"

  if [[ ! -f "${path}" ]]; then
    create_empty_plist "${path}"
  fi

  if /usr/libexec/PlistBuddy -c "Print :${key}" "${path}" >/dev/null 2>&1; then
    /usr/libexec/PlistBuddy -c "Set :${key} ${value}" "${path}"
  else
    /usr/libexec/PlistBuddy -c "Add :${key} bool ${value}" "${path}"
  fi
}

GLOBAL_UC="/Library/Managed Preferences/com.apple.universalcontrol.plist"
USER_UC="/Library/Managed Preferences/${TARGET_USER}/com.apple.universalcontrol.plist"
GLOBAL_ACCESS="/Library/Managed Preferences/com.apple.applicationaccess.plist"
USER_ACCESS="/Library/Managed Preferences/${TARGET_USER}/com.apple.applicationaccess.plist"
GLOBAL_BROWSER="/Library/Managed Preferences/com.apple.NetworkBrowser.plist"
USER_BROWSER="/Library/Managed Preferences/${TARGET_USER}/com.apple.NetworkBrowser.plist"

backup_file "${GLOBAL_UC}" "global.com.apple.universalcontrol.plist"
backup_file "${USER_UC}" "user.com.apple.universalcontrol.plist"
backup_file "${GLOBAL_ACCESS}" "global.com.apple.applicationaccess.plist"
backup_file "${USER_ACCESS}" "user.com.apple.applicationaccess.plist"
backup_file "${GLOBAL_BROWSER}" "global.com.apple.NetworkBrowser.plist"
backup_file "${USER_BROWSER}" "user.com.apple.NetworkBrowser.plist"

set_bool_key "${GLOBAL_UC}" "Disable" false
set_bool_key "${USER_UC}" "Disable" false

set_bool_key "${GLOBAL_ACCESS}" "allowUniversalControl" true
set_bool_key "${USER_ACCESS}" "allowUniversalControl" true
set_bool_key "${GLOBAL_ACCESS}" "allowAirDrop" true
set_bool_key "${USER_ACCESS}" "allowAirDrop" true

set_bool_key "${GLOBAL_BROWSER}" "DisableAirDrop" false
set_bool_key "${USER_BROWSER}" "DisableAirDrop" false

killall cfprefsd >/dev/null 2>&1 || true
killall "System Settings" >/dev/null 2>&1 || true

echo "Managed preferences restored for ${TARGET_USER}"
echo "Backup saved to ${BACKUP_DIR}"
