## Developer Apps & OAuth

Build third-party integrations with Orshot using OAuth 2.0. Register an app, authenticate users, and access their workspaces on their behalf.

For detailed setup: fetch `https://orshot.com/docs/developers/oauth-overview.md`

### Register an App

1. Go to **Workspace Settings → Developer Apps** in the Orshot dashboard
2. Create a new app with a name, redirect URI, and the scopes it needs
3. Use the app's `client_id` in the flows below. Orshot OAuth clients are public clients: PKCE (`S256`) is required and no client secret is used.

Discovery: `https://api.orshot.com/.well-known/oauth-authorization-server` (dynamic client registration is available at `registration_endpoint`).

### OAuth 2.0 Flows

**Authorization Code + PKCE** (web and desktop apps):
```
GET https://orshot.com/oauth/authorize?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=https://yourapp.com/callback&
  code_challenge=BASE64URL_SHA256_OF_VERIFIER&
  code_challenge_method=S256&
  scope=workspace:templates:read workspace:templates:write render:generate
```

**Device Flow** (CLI/headless):
```
POST https://api.orshot.com/v1/oauth/device/code
  client_id=YOUR_CLIENT_ID&
  scope=workspace:templates:read render:generate
```

### Token Exchange

```
POST https://api.orshot.com/v1/oauth/token
  grant_type=authorization_code&
  code=AUTH_CODE&
  client_id=YOUR_CLIENT_ID&
  code_verifier=THE_PKCE_VERIFIER&
  redirect_uri=https://yourapp.com/callback
```

Refresh with `grant_type=refresh_token` when the `offline_access` scope was granted. Store tokens server-side or in the user's own environment; never place them in prompts, logs, or shared files.

### Available Scopes

| Scope | Description |
|-------|-------------|
| `workspace:read` | List and read workspace details |
| `workspace:templates:read` | List and read templates |
| `workspace:templates:write` | Update template modifications via API |
| `render:generate` | Generate images, PDFs, and videos |
| `mcp:access` | Access via Model Context Protocol |
| `offline_access` | Long-lived refresh tokens |

For endpoint details: fetch `https://orshot.com/docs/developers/oauth-endpoints.md`

