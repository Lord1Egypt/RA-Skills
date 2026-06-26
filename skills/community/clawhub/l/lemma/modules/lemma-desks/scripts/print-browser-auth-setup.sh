#!/bin/bash

set -euo pipefail

if [ -z "${LEMMA_TOKEN:-}" ]; then
  echo "Missing one or more required env vars:"
  echo "  LEMMA_TOKEN"
  exit 1
fi

node - <<'EOF' "$LEMMA_TOKEN" "${LEMMA_DESK_DEV_PORT:-5173}"
const [token, port] = process.argv.slice(2);
const baseUrl = `http://127.0.0.1:${port}/`;

console.log("Keep the desk app code unchanged.");
console.log("Default desk runtime is cookie auth.");
console.log("For browser testing, inject the token through localStorage.");
console.log("");
console.log(`Open: ${baseUrl}`);
console.log(`Then run in DevTools: localStorage.setItem("lemma_token", ${JSON.stringify(token)})`);
console.log("Reload after setting the token.");
console.log("");
console.log("Normal preview URL:");
console.log(baseUrl);
console.log("");
console.log("Do not put testing tokens in URLs or source files.");
EOF
