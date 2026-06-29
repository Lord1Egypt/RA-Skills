# Oi MCP Authentication for OpenClaw

The hosted Oi MCP server at `https://api.oioioi.ai/mcp` supports two auth paths.

## OAuth (recommended)

Use OAuth when OpenClaw can open a browser for sign-in. **No organization API key is required beforehand.**

1. Register the server (if not already done):

```bash
openclaw mcp add oi \
  --url https://api.oioioi.ai/mcp \
  --transport streamable-http \
  --auth oauth
```

2. Sign in and approve the connection:

```bash
openclaw mcp login oi
```

OpenClaw may print an authorization URL and ask you to complete login manually:

```bash
openclaw mcp login oi --code <code-from-callback-url>
```

After browser approval, copy the `code=` value from the redirect URL (for example `http://127.0.0.1:8989/oauth/callback?code=...`). A "connection refused" page on localhost is normal for the manual flow.

OpenClaw stores OAuth tokens under `~/.openclaw/`. Complete sign-in and approval on `app.oioioi.ai` when prompted.

3. Verify:

```bash
openclaw mcp configure oi --timeout 120 --connect-timeout 30
openclaw mcp doctor oi --probe
```

Oi can expose many connection tools (for example Zoho CRM). The first probe may be slow; longer timeouts avoid false `-32001: Request timed out` errors.

Or run the repo installer from a local clone:

```bash
bash scripts/install-to-openclaw.sh
```

ClawHub installs should use the `openclaw mcp` commands above instead of the repo script.

## Organization API key (fallback)

Use a bearer token when OAuth is unavailable (headless environments, no browser, or clients that only accept static headers).

1. In the Oi app, open **Organization → API Keys** (`/dashboard/organization/api-keys`).
2. Create and copy an organization API key. Store it in a secret field or environment variable such as `OI_ORG_API_KEY`.
3. Register or update the MCP server with a bearer header:

```bash
openclaw mcp add oi \
  --url https://api.oioioi.ai/mcp \
  --transport streamable-http \
  --header "Authorization=Bearer ${OI_ORG_API_KEY}"
```

Or configure an existing server:

```bash
openclaw mcp configure oi --header "Authorization=Bearer ${OI_ORG_API_KEY}"
```

4. Verify:

```bash
openclaw mcp doctor oi --probe
```

Or install with the key in your environment:

```bash
export OI_ORG_API_KEY="your-key-here"
bash scripts/install-to-openclaw.sh
```

## Bearer auth shape

```text
Authorization: Bearer <token>
```

Accepted token types:

- OAuth access token issued by Oi
- Exported Oi organization API key

## Good practices

- Prefer OAuth for interactive OpenClaw setups.
- Prefer an organization API key only when bearer-token configuration is required.
- Store bearer tokens in OpenClaw secret or environment fields, not in prompts or logs.
- Rotate organization API keys if access should change or a token is exposed.

## Further reading

- [Oi MCP authentication guide](https://www.oioioi.ai/resources/authentication)
- [OpenClaw MCP CLI](https://docs.openclaw.ai/cli/mcp)
- Manual config snippet: `config/mcp-server.json5`
