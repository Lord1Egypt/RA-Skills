#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_USER="${1:-${USER}}"
TARGET_UID="$(id -u "${TARGET_USER}")"

ROOT_LABEL="com.joseph.macos-connectivity-restore.root"
USER_LABEL="com.joseph.macos-connectivity-restore.user"
ROOT_PLIST="/Library/LaunchDaemons/${ROOT_LABEL}.plist"
USER_PLIST="/Users/${TARGET_USER}/Library/LaunchAgents/${USER_LABEL}.plist"
ROOT_TMP="/tmp/${ROOT_LABEL}.plist"
ROOT_INSTALL_SH="/tmp/${ROOT_LABEL}.install.sh"

mkdir -p "/Users/${TARGET_USER}/Library/LaunchAgents"
chmod +x "${SCRIPT_DIR}/restore-root.sh" "${SCRIPT_DIR}/restore-user.sh"

cat > "${ROOT_TMP}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${ROOT_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${SCRIPT_DIR}/restore-root.sh</string>
    <string>${TARGET_USER}</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/Users/${TARGET_USER}/Library/Logs/${ROOT_LABEL}.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/${TARGET_USER}/Library/Logs/${ROOT_LABEL}.log</string>
</dict>
</plist>
EOF

cat > "${USER_PLIST}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${USER_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${SCRIPT_DIR}/restore-user.sh</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>LimitLoadToSessionType</key>
  <array>
    <string>Aqua</string>
  </array>
  <key>StandardOutPath</key>
  <string>/Users/${TARGET_USER}/Library/Logs/${USER_LABEL}.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/${TARGET_USER}/Library/Logs/${USER_LABEL}.log</string>
</dict>
</plist>
EOF

cat > "${ROOT_INSTALL_SH}" <<EOF
#!/bin/zsh
set -euo pipefail
cp "${ROOT_TMP}" "${ROOT_PLIST}"
chown root:wheel "${ROOT_PLIST}"
chmod 644 "${ROOT_PLIST}"
launchctl bootout system "${ROOT_PLIST}" >/dev/null 2>&1 || true
launchctl bootstrap system "${ROOT_PLIST}"
launchctl kickstart -k "system/${ROOT_LABEL}" >/dev/null 2>&1 || true
EOF

chmod 700 "${ROOT_INSTALL_SH}"

osascript -e "do shell script \"/bin/zsh '${ROOT_INSTALL_SH}'\" with administrator privileges"

launchctl bootout "gui/${TARGET_UID}/${USER_LABEL}" >/dev/null 2>&1 || true
launchctl bootstrap "gui/${TARGET_UID}" "${USER_PLIST}"
launchctl kickstart -k "gui/${TARGET_UID}/${USER_LABEL}" >/dev/null 2>&1 || true

"${SCRIPT_DIR}/restore-user.sh" >/dev/null

echo "Installed startup restore jobs:"
echo "  ${ROOT_PLIST}"
echo "  ${USER_PLIST}"
