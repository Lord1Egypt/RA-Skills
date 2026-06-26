#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
mkdir -p "${BIN_DIR}"
cat > "${BIN_DIR}/ostrom-energy" <<EOF
#!/usr/bin/env bash
exec bash "${ROOT}/run.sh" "\$@"
EOF
chmod +x "${BIN_DIR}/ostrom-energy"
printf 'Installed ostrom-energy wrapper at %s\n' "${BIN_DIR}/ostrom-energy"
case ":${PATH}:" in
  *":${BIN_DIR}:"*) ;;
  *) printf 'Note: %s is not currently on PATH. Add it to your shell profile if needed.\n' "${BIN_DIR}" ;;
esac
