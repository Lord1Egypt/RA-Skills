---
name: mcp-oauth
description: "Add OAuth 2.0 PKCE authentication to a remote MCP server. Use this skill whenever the user wants to add authentication to an MCP server, protect MCP tools with OAuth, implement login flow for an MCP connector, add user auth to an MCP endpoint, or set up token-based access for MCP. Also triggers on: 'MCP OAuth', 'MCP authentication', 'withMcpAuth', 'MCP login flow', 'protect MCP endpoint', 'MCP token auth', 'dynamic client registration MCP', 'Claude connector OAuth'. Even if the user just says 'add auth to my MCP server' or 'my MCP server needs login', use this skill."
license: MIT
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F512"
    homepage: https://github.com/lucaperret/agent-skills
---

# OAuth 2.0 PKCE for MCP Servers

Add production-ready OAuth authentication to a remote MCP server. This implements the full MCP authorization spec — discovery, dynamic client registration, PKCE authorization, token exchange, and refresh.

## When you need this

Your MCP server accesses user-specific data (their account, their files, their playlists). Without auth, anyone with your server URL could access anyone's data. OAuth lets each user authenticate with their own credentials and get their own token.

## Architecture overview

Your MCP server plays two roles:
1. **OAuth server** for MCP clients (Claude, Smithery) — issues your own tokens
2. **OAuth client** to the upstream service (Tidal, GitHub, Slack, etc.) — exchanges for their tokens

```
MCP Client (Claude) → Your OAuth Server → Upstream Service (e.g., Tidal)
     │                      │                        │
     │  1. Discover OAuth   │                        │
     │  2. Register client  │                        │
     │  3. Authorize        │──→ 4. Redirect to      │
     │                      │      upstream login ──→ │
     │                      │  ←── 5. Callback ──────│
     │  ←── 6. Auth code    │                        │
     │  7. Exchange token   │                        │
     │  8. Call tools ─────→│──→ 9. API calls ──────→│
```

## Required endpoints

### 1. OAuth Discovery

`app/.well-known/oauth-authorization-server/route.ts`:

```typescript
import { NextResponse } from 'next/server';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://your-domain.com';

export async function GET() {
  return NextResponse.json({
    issuer: SITE_URL,
    authorization_endpoint: `${SITE_URL}/api/authorize`,
    token_endpoint: `${SITE_URL}/api/token`,
    registration_endpoint: `${SITE_URL}/api/register`,
    response_types_supported: ['code'],
    grant_types_supported: ['authorization_code', 'refresh_token'],
    code_challenge_methods_supported: ['S256'],
    token_endpoint_auth_methods_supported: ['none'],
  }, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
    },
  });
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

### 2. Protected Resource Metadata

`app/.well-known/oauth-protected-resource/route.ts`:

```typescript
import { protectedResourceHandler, metadataCorsOptionsRequestHandler } from 'mcp-handler';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://your-domain.com';

export const GET = protectedResourceHandler({
  authServerUrls: [SITE_URL],
  resourceUrl: SITE_URL,
});

export const OPTIONS = metadataCorsOptionsRequestHandler();
```

### 3. Dynamic Client Registration (RFC 7591)

MCP clients register themselves before starting the auth flow.

`app/api/register/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}));
  const clientId = crypto.randomBytes(16).toString('hex');

  return NextResponse.json({
    client_id: clientId,
    client_name: body.client_name || 'MCP Client',
    redirect_uris: body.redirect_uris || [],
    grant_types: ['authorization_code', 'refresh_token'],
    response_types: ['code'],
    token_endpoint_auth_method: 'none',
  }, { status: 201 });
}
```

### 4. Authorization Endpoint

Validates the request, stores session in Redis, redirects to upstream OAuth.

`app/api/authorize/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
  const params = req.nextUrl.searchParams;
  const redirectUri = params.get('redirect_uri');
  const state = params.get('state');
  const codeChallenge = params.get('code_challenge');

  if (!redirectUri || !state || !codeChallenge) {
    return NextResponse.json(
      { error: 'invalid_request', error_description: 'Missing required parameters' },
      { status: 400 },
    );
  }

  // Validate redirect_uri — allow known MCP clients
  const url = new URL(redirectUri);
  const isAllowed =
    url.hostname === 'claude.ai' ||
    url.hostname === 'claude.com' ||
    url.hostname === 'api.smithery.ai' ||
    url.hostname === 'localhost' ||
    url.hostname === '127.0.0.1';

  if (!isAllowed) {
    return NextResponse.json(
      { error: 'invalid_request', error_description: 'redirect_uri not allowed' },
      { status: 400 },
    );
  }

  // Generate PKCE for upstream OAuth
  const upstreamVerifier = crypto.randomBytes(32).toString('base64url');
  const upstreamChallenge = crypto
    .createHash('sha256')
    .update(upstreamVerifier)
    .digest('base64url');
  const sessionId = crypto.randomBytes(16).toString('hex');

  // Store in Redis (10 min TTL)
  await redis.set(`session:${sessionId}`, JSON.stringify({
    redirectUri, state, codeChallenge,
    upstreamVerifier, upstreamState: sessionId,
  }), { ex: 600 });

  // Redirect to upstream OAuth (replace with your service)
  const upstreamUrl = new URL('https://upstream-service.com/authorize');
  upstreamUrl.searchParams.set('client_id', 'YOUR_CLIENT_ID');
  upstreamUrl.searchParams.set('response_type', 'code');
  upstreamUrl.searchParams.set('redirect_uri', `${SITE_URL}/api/callback`);
  upstreamUrl.searchParams.set('code_challenge', upstreamChallenge);
  upstreamUrl.searchParams.set('code_challenge_method', 'S256');
  upstreamUrl.searchParams.set('state', sessionId);

  return NextResponse.redirect(upstreamUrl.toString());
}
```

### 5. Callback (from upstream)

`app/api/callback/route.ts`:

```typescript
export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get('code');
  const state = req.nextUrl.searchParams.get('state');

  // Look up session from Redis
  const session = JSON.parse(await redis.get(`session:${state}`));
  if (!session) return NextResponse.json({ error: 'Session expired' }, { status: 400 });

  // Exchange code for upstream tokens
  const tokens = await exchangeUpstreamCode(code, session.upstreamVerifier);

  // Store upstream tokens in Redis (30 day TTL)
  const userId = crypto.randomBytes(16).toString('hex');
  await redis.set(`user:${userId}:tokens`, JSON.stringify(tokens), { ex: 2592000 });

  // Generate our auth code for the MCP client
  const mcpAuthCode = crypto.randomBytes(16).toString('hex');
  await redis.set(`auth_code:${mcpAuthCode}`, userId, { ex: 300 });

  // Clean up and redirect back to MCP client
  await redis.del(`session:${state}`);
  const redirect = new URL(session.redirectUri);
  redirect.searchParams.set('code', mcpAuthCode);
  redirect.searchParams.set('state', session.state);
  return NextResponse.redirect(redirect.toString());
}
```

### 6. Token Exchange

`app/api/token/route.ts`:

```typescript
export async function POST(req: NextRequest) {
  const body = Object.fromEntries(await req.formData());

  if (body.grant_type === 'authorization_code') {
    const userId = await redis.get(`auth_code:${body.code}`);
    if (!userId) return NextResponse.json({ error: 'invalid_grant' }, { status: 400 });
    await redis.del(`auth_code:${body.code}`);

    const accessToken = crypto.randomBytes(16).toString('hex');
    const refreshToken = crypto.randomBytes(16).toString('hex');
    await redis.set(`mcp_token:${accessToken}`, userId, { ex: 86400 });
    await redis.set(`refresh:${refreshToken}`, userId, { ex: 2592000 });

    return NextResponse.json({
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: 86400,
      refresh_token: refreshToken,
    });
  }

  if (body.grant_type === 'refresh_token') {
    const userId = await redis.get(`refresh:${body.refresh_token}`);
    if (!userId) return NextResponse.json({ error: 'invalid_grant' }, { status: 400 });

    // Optionally refresh upstream tokens here too
    const newAccess = crypto.randomBytes(16).toString('hex');
    const newRefresh = crypto.randomBytes(16).toString('hex');
    await redis.set(`mcp_token:${newAccess}`, userId, { ex: 86400 });
    await redis.set(`refresh:${newRefresh}`, userId, { ex: 2592000 });

    return NextResponse.json({
      access_token: newAccess,
      token_type: 'Bearer',
      expires_in: 86400,
      refresh_token: newRefresh,
    });
  }

  return NextResponse.json({ error: 'unsupported_grant_type' }, { status: 400 });
}
```

## Wrapping the MCP handler

Use `withMcpAuth` from `mcp-handler` to enforce auth on tool calls while allowing unauthenticated discovery:

```typescript
import { createMcpHandler, withMcpAuth } from 'mcp-handler';
import type { AuthInfo } from '@modelcontextprotocol/sdk/server/auth/types.js';

const mcpHandler = createMcpHandler(/* ... */);

const verifyToken = async (_req: Request, bearerToken?: string): Promise<AuthInfo | undefined> => {
  if (!bearerToken) return undefined;
  const userId = await redis.get(`mcp_token:${bearerToken}`);
  if (!userId) return undefined;
  return { token: bearerToken, clientId: 'my-server', scopes: [], extra: { userId } };
};

// required: false allows initialize/tools/list without auth
// Tools check auth themselves via extra.authInfo
const handler = withMcpAuth(mcpHandler, verifyToken, {
  required: false,
  resourceUrl: SITE_URL,
});
```

Setting `required: false` is important — it allows MCP clients to discover tools without authenticating first. Auth is enforced at the tool level when the tool tries to access user data.

## Redis token storage schema

| Key | Value | TTL |
|-----|-------|-----|
| `session:<id>` | OAuth session (redirect_uri, state, PKCE) | 10 min |
| `auth_code:<code>` | user ID | 5 min |
| `user:<id>:tokens` | upstream access/refresh tokens | 30 days |
| `mcp_token:<token>` | user ID | 24 hours |
| `refresh:<token>` | user ID | 30 days |

## Redirect URI allowlist

At minimum, allow these hostnames in your `/api/authorize` validation:

- `claude.ai` — Claude web
- `claude.com` — Claude web (alternate)
- `api.smithery.ai` — Smithery scanning
- `localhost` / `127.0.0.1` — local development

Add more as needed for other MCP clients. Keep the validation hostname-based (not exact URL match) because clients may use different callback paths.

## Token storage with Upstash Redis

```bash
npm install @upstash/redis
```

```typescript
import { Redis } from '@upstash/redis';
const redis = new Redis({
  url: process.env.KV_REST_API_URL!,
  token: process.env.KV_REST_API_TOKEN!,
});
```

Set up Upstash via Vercel Marketplace: Project Settings → Storage → Create → Upstash Redis. The env vars are automatically added to your project.
