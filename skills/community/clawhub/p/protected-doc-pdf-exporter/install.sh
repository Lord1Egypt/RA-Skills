#!/usr/bin/env bash
#
# Installer for protected-doc-pdf-exporter
# Installs the tool as an AI Agent Skill & system CLI command
#
set -euo pipefail

SKILL_NAME="protected-doc-pdf-exporter"
INSTALL_DIR="${HOME}/.gemini/config/skills/${SKILL_NAME}"
BIN_DIR="${HOME}/.local/bin"
REPO_URL="https://github.com/Nelson-zhou/protected-doc-pdf-exporter.git"

echo "============================================================"
echo "  Installing Protected Document PDF Exporter Skill"
echo "============================================================"

# 1. Ensure git & python3 are installed
if ! command -v git &>/dev/null; then
    echo "[-] Error: 'git' is required but not installed." >&2
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "[-] Error: 'python3' is required but not installed." >&2
    exit 1
fi

# 2. Clone or update repository in user's skills directory
mkdir -p "$(dirname "${INSTALL_DIR}")"
if [ -d "${INSTALL_DIR}/.git" ]; then
    echo "[*] Updating existing installation at ${INSTALL_DIR}..."
    git -C "${INSTALL_DIR}" pull --quiet
else
    echo "[*] Cloning repository to ${INSTALL_DIR}..."
    git clone --quiet "${REPO_URL}" "${INSTALL_DIR}"
fi

# 3. Install Python dependencies
echo "[*] Installing Python dependencies..."
python3 -m pip install --quiet -r "${INSTALL_DIR}/requirements.txt" || {
    echo "[!] Warning: pip install returned non-zero. Please verify dependencies manually."
}

# 4. Create symlink in ~/.local/bin for global CLI access
mkdir -p "${BIN_DIR}"
ln -sf "${INSTALL_DIR}/export_doc.py" "${BIN_DIR}/export-doc"
chmod +x "${INSTALL_DIR}/export_doc.py"

echo "============================================================"
echo "[✓] Installation completed successfully!"
echo ""
echo "  • AI Agent Skill: ${INSTALL_DIR}/SKILL.md (Active)"
echo "  • CLI Command:    export-doc --help"
echo ""
echo "  Try running: export-doc --help"
echo "============================================================"
