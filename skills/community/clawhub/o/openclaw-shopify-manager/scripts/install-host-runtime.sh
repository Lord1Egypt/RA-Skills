#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$ROOT/scripts"
RUNTIME_ROOT="${SHOPIFY_RUNTIME_ROOT:-$HOME/oc/shopify-runtime}"
WRITE_SERVICE="${WRITE_SERVICE:-1}"

cat <<EOF
OpenClaw Shopify Manager host installer

This script bootstraps the canonical host runtime directory and then prints the next host/systemd steps.
Secrets stay in: $RUNTIME_ROOT/.env
EOF

mkdir -p "$RUNTIME_ROOT"

if [ "$WRITE_SERVICE" = "1" ]; then
  node "$SCRIPTS_DIR/setup-runtime.mjs" guided-setup --runtime-root "$RUNTIME_ROOT" --write-service
else
  node "$SCRIPTS_DIR/setup-runtime.mjs" guided-setup --runtime-root "$RUNTIME_ROOT"
fi

cat <<EOF

Next recommended host steps:

1. Start the connector locally for first verification:
   cd "$RUNTIME_ROOT" && node ./shopify-connector.mjs run-server

2. Verify local health:
   curl http://127.0.0.1:8787/healthz

3. Expose over HTTPS (recommended with Tailscale):
   tailscale serve --https=443 /shopify-manager http://127.0.0.1:8787
   tailscale funnel --https=443 on

4. Complete OAuth:
   cd "$RUNTIME_ROOT" && node ./shopify-connector.mjs auth-url

5. Verify store access:
   cd "$RUNTIME_ROOT" && node ./shopify-connector.mjs shop-info

If you generated a service file, install it manually with your normal host/systemd flow.
EOF
