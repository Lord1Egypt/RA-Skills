---
name: openclaw-shopify-manager
description: Connect OpenClaw to Shopify with guided setup, local `.env` secret storage, Shopify OAuth, webhook validation, product and content operations, and host or Docker-sidecar deployment support. Use when connecting a Shopify store to OpenClaw, completing Shopify app setup, reading store information, listing or finding products, updating approved Shopify content, or running a small local Shopify connector for OpenClaw.
metadata:
  {
    "openclaw":
      {
        "primaryEnv": "SHOPIFY_API_KEY",
        "requires":
          {
            "env":
              [
                "SHOPIFY_API_KEY",
                "SHOPIFY_API_SECRET",
                "SHOPIFY_SHOP",
                "SHOPIFY_REDIRECT_URI",
              ],
          },
      },
  }
---

# OpenClaw Shopify Manager

Use this skill to connect OpenClaw to Shopify with a guided setup flow, local secret storage, and a small local connector for OAuth, webhooks, and Shopify Admin API operations.

## Core workflow

1. Read `references/setup.md` for the canonical setup path.
2. Use `scripts/setup-runtime.mjs guided-setup` to create the runtime directory, config files, `.env`, logs/state folders, and optional systemd unit template.
3. Read `references/tailscale.md` when using Tailscale for public HTTPS callback exposure.
4. Read `references/systemd.md` for host/systemd operation.
5. Read `references/docker.md` for Docker or sidecar deployment.
6. Use `scripts/shopify-connector.mjs` for auth URL generation, callback handling, webhook validation, and Shopify API calls.
7. Use `scripts/setup-runtime.mjs doctor` to verify runtime completeness.
8. Use `scripts/install-host-runtime.sh` when the user wants the canonical host-oriented setup flow.

## Safety rules

- Keep Shopify secrets and tokens in `.env`, not in tracked config files.
- Default to read-first behavior unless the user clearly asks for mutations.
- Before any store-changing action, restate the intended change briefly and get confirmation.
- Prefer least-privilege scopes.
- Verify callback URLs and health endpoints after setup changes.

## Common user-facing tasks

### Connect a store

- Run `scripts/setup-runtime.mjs guided-setup`.
- Fill Shopify app credentials into `.env`.
- Start the connector.
- Expose the callback path publicly over HTTPS.
- Generate the auth URL with `scripts/shopify-connector.mjs auth-url`.
- Complete OAuth.
- Verify with `shop-info`.

### Read Shopify data

Supported helper commands include:

- `shop-info`
- `list-products`
- `find-products`
- `get-product`
- `list-blogs`
- `list-articles`

Use `get-product --id ...` for exact lookup and `get-product --title ...` or `find-products --query ...` for title-based lookup.

### Update Shopify data

Supported mutation helpers include:

- `update-product`
- `create-article`
- `update-article`

Use write commands only after user confirmation.

## Resource map

- Setup guide: `references/setup.md`
- Tailscale guide: `references/tailscale.md`
- systemd guide: `references/systemd.md`
- Docker guide: `references/docker.md`
- Shopify scopes and safety: `references/scopes-and-safety.md`
- Runtime bootstrap: `scripts/setup-runtime.mjs`
- Canonical host installer: `scripts/install-host-runtime.sh`
- Connector runtime: `scripts/shopify-connector.mjs`
- Service template: `assets/shopify-connector.service.txt`
- Tailscale checker: `scripts/check-tailscale.sh`
