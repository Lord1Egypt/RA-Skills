#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

tmp="$(mktemp -d)"
install_dir="${tmp}/GrayMatter"
mkdir -p "${install_dir}"

cp "${ROOT}/SKILL.md" "${install_dir}/SKILL.md"
cp "${ROOT}/graymatter.skill" "${install_dir}/graymatter.skill"
cp "${ROOT}/graymatter-bootstrap" "${install_dir}/graymatter-bootstrap"
chmod +x "${install_dir}/graymatter-bootstrap"

[[ ! -e "${install_dir}/scripts/gm-activate" ]] || fail "fixture should start as a root-only sparse install"

(cd "${install_dir}" && ./graymatter-bootstrap >/tmp/graymatter-bootstrap.out)

[[ -x "${install_dir}/scripts/gm-activate" ]] || fail "graymatter-bootstrap should restore runtime scripts from graymatter.skill"
[[ -x "${install_dir}/scripts/graymatter_api.sh" ]] || fail "graymatter-bootstrap should restore graymatter_api.sh"
[[ -f "${install_dir}/mcp-server/index.js" ]] || fail "graymatter-bootstrap should restore MCP server files"

printf 'PASS: end_user_install_test.sh\n'
