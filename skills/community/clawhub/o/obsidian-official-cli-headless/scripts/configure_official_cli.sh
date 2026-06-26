#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "Run as root." >&2
  exit 1
fi

VAULT_PATH="$(realpath -m "${1:-/root/obsidian-vault}")"
OBSIDIAN_USER="${OBSIDIAN_USER:-obsidian}"
WRAPPER_PATH="${WRAPPER_PATH:-/usr/local/bin/obs}"
CONFIG_DIR="/home/${OBSIDIAN_USER}/.config/obsidian"
CONFIG_FILE="${CONFIG_DIR}/obsidian.json"
VAULT_NAME="$(basename "$VAULT_PATH")"
TS="$(date +%s%3N 2>/dev/null || python3 - <<'PY'
import time
print(int(time.time()*1000))
PY
)"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

require_cmd setfacl
require_cmd su
require_cmd xvfb-run
require_cmd realpath

if ! id -u "$OBSIDIAN_USER" >/dev/null 2>&1; then
  echo "User ${OBSIDIAN_USER} does not exist. Run install script first." >&2
  exit 1
fi

if [[ ! -x /usr/bin/obsidian ]]; then
  echo "Official /usr/bin/obsidian not found. Run install script first." >&2
  exit 1
fi

mkdir -p "$VAULT_PATH" "$CONFIG_DIR"
chown -R "$OBSIDIAN_USER:$OBSIDIAN_USER" "/home/${OBSIDIAN_USER}/.config"

if [[ "$VAULT_PATH" == /root/* ]]; then
  setfacl -m u:${OBSIDIAN_USER}:--x /root
fi

setfacl -R -m u:${OBSIDIAN_USER}:rwx "$VAULT_PATH"
setfacl -R -m d:u:${OBSIDIAN_USER}:rwx "$VAULT_PATH"

cat > "$CONFIG_FILE" <<JSON
{
  "cli": true,
  "vaults": {
    "${VAULT_NAME}": {
      "path": "${VAULT_PATH}",
      "ts": ${TS},
      "open": true
    }
  }
}
JSON
chown "$OBSIDIAN_USER:$OBSIDIAN_USER" "$CONFIG_FILE"

cat > "$WRAPPER_PATH" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cmd=()
for arg in "\$@"; do
  cmd+=("\$(printf '%q' "\$arg")")
done
exec su - ${OBSIDIAN_USER} -c "cd ${VAULT_PATH} && xvfb-run -a /usr/bin/obsidian --disable-gpu \${cmd[*]}"
EOF
chmod +x "$WRAPPER_PATH"

echo "Configured official CLI."
echo "Vault: $VAULT_PATH"
echo "Wrapper: $WRAPPER_PATH"
echo "Vault name: $VAULT_NAME"
