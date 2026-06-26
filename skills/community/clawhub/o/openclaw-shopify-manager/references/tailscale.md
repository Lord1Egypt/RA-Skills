# Tailscale

## When to use Tailscale here

Use Tailscale when the user wants a simple, production-friendly HTTPS endpoint for Shopify callbacks and webhooks without introducing a separate reverse proxy stack.

Good fit:

- single-host OpenClaw install
- wants stable public HTTPS quickly
- okay using a Tailscale hostname or custom domain later
- wants Serve/Funnel instead of Caddy/Nginx

## What Tailscale provides

- a stable machine identity
- HTTPS path serving/proxying via `tailscale serve`
- public internet reachability via `tailscale funnel`

## Detection workflow

Use `scripts/check-tailscale.sh` first.

If OpenClaw is running in Docker, prefer checking Tailscale on the host, not assuming it exists inside the application container.

It reports:

- whether `tailscale` is installed
- whether the daemon appears reachable
- whether the machine is logged in
- whether Serve/Funnel commands are present

## If Tailscale is not installed

Advise the user to install it using the official Tailscale instructions for their OS.

Do not recommend piping a remote installer script into the shell here.
Prefer the official package-manager or platform-specific installation path from Tailscale's docs, then bring the node up with:

```bash
sudo tailscale up
```

## Recommended path-prefix layout

Example:

- OpenClaw UI remains on `/`
- Shopify connector is exposed on `/shopify-manager`

Then the connector can serve:

- `/shopify-manager/healthz`
- `/shopify-manager/shopify/callback`
- `/shopify-manager/shopify/webhooks/...`

## Example Serve/Funnel commands

If the local connector listens on `127.0.0.1:8787`:

```bash
tailscale serve --https=443 /shopify-manager http://127.0.0.1:8787
tailscale funnel --https=443 on
```

After that, verify the public health endpoint using the assigned Tailscale HTTPS hostname.

## Shopify app values

If the public base URL is:

- `https://example-tailnet.ts.net/shopify-manager`

Then the Shopify app should typically use:

- App URL: `https://example-tailnet.ts.net/shopify-manager`
- Allowed redirection URL: `https://example-tailnet.ts.net/shopify-manager/shopify/callback`
- Webhook base: `https://example-tailnet.ts.net/shopify-manager/shopify/webhooks`

## Operational notes

- Verify local health first, then public health.
- Keep the connector on localhost; let Tailscale proxy to it.
- If the user does not want Tailscale, fall back to a conventional reverse proxy and custom domain.
