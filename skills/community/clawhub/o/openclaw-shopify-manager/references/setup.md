# Setup

## Goal

Get from skill install to a usable Shopify connection with the fewest moving parts:

1. bootstrap a canonical runtime directory
2. fill Shopify app values once
3. expose one HTTPS callback path
4. complete OAuth once
5. use Shopify commands normally after that

## Canonical runtime bootstrap

Use the bundled guided setup helper instead of copying files by hand:

```bash
node ./scripts/setup-runtime.mjs guided-setup --write-service
```

By default it creates:

- runtime root: `~/oc/shopify-runtime`
- config: `~/oc/shopify-runtime/config.json`
- secrets/env: `~/oc/shopify-runtime/.env`
- runtime script: `~/oc/shopify-runtime/shopify-connector.mjs`
- logs: `~/oc/shopify-runtime/logs/`
- state: `~/oc/shopify-runtime/state/`
- optional service file: `~/oc/shopify-runtime/shopify-connector.service`

Use non-interactive flags only for non-secret values when they are already known:

```bash
node ./scripts/setup-runtime.mjs guided-setup \
  --shop your-store.myshopify.com \
  --public-base-url https://YOUR-HOST/shopify-manager \
  --write-service
```

Paste Shopify secrets into the guided prompt or edit `.env` directly. Avoid passing secrets as CLI flags.

## Deployment shape decision

Choose one before exposing anything:

1. Host/VM deployment: connector on the host, managed by systemd
2. Docker OpenClaw + host connector: OpenClaw in Docker, connector on the host
3. Docker sidecar deployment: connector in a dedicated container with mounted persistent storage

For most Docker users, option 2 is the least fragile.

## Minimal setup sequence

1. Run `setup-runtime.mjs guided-setup`.
2. Verify `.env` has `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, and `SHOPIFY_SHOP`.
3. Verify `config.json` / `.env` contain the final public callback URL.
4. Start the local connector.
5. Expose it publicly over HTTPS.
6. Generate the install URL.
7. Complete app installation in Shopify.
8. Verify with a read-only API call.

## Starting the connector

```bash
cd ~/oc/shopify-runtime
node ./shopify-connector.mjs run-server
```

Health check:

```bash
curl http://127.0.0.1:8787/healthz
```

## Doctor mode

To confirm the runtime is complete enough for startup/OAuth:

```bash
node ./scripts/setup-runtime.mjs doctor
```

This checks whether the canonical runtime files exist, whether required Shopify values are still placeholders, whether the redirect URI matches the public base URL, whether a runtime `.gitignore` is protecting secrets, and whether Tailscale likely needs attention.

## Runtime configuration

Use `config.json` for non-secret values and `.env` for secrets/runtime state.

### Non-secret config

Expected keys:

- `shop`
- `apiVersion`
- `scopes`
- `redirectUri`
- `publicBaseUrl`
- `serverHost`
- `serverPort`
- `mode`
- `allowedMutations`

### Secret env

Expected keys:

- `SHOPIFY_API_KEY`
- `SHOPIFY_API_SECRET`
- `SHOPIFY_ACCESS_TOKEN`

Keep these in `.env` only. Do not move them into `config.json`, docs, screenshots, or committed files. The runtime directory should also keep `.env`, `state/`, and `logs/` ignored via `.gitignore`.

## Production notes

- Bind locally on `127.0.0.1`, not `0.0.0.0`, unless there is a specific reason not to.
- Use systemd if callbacks or webhooks must survive shell disconnects and reboots.
- Keep scopes lean.
- Verify the exact callback path before installing the Shopify app.

## Validation checklist

Before using the connector in production, verify:

- local `healthz` responds
- service stays up under systemd or container restart policy
- public HTTPS URL is reachable
- Shopify callback path matches exactly
- offline token is written locally after install
- at least one read-only API call succeeds
