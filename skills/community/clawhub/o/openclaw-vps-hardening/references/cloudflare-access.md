# Cloudflare Access Setup — Per-Agent Identity Gate

Lock each OpenClaw agent behind Cloudflare's identity gate. Every request requires authentication before traffic reaches the VPS.

## Table of Contents
1. [Architecture](#architecture)
2. [Prerequisites](#prerequisites)
3. [Create a Cloudflare Access Application](#create-a-cloudflare-access-application)
4. [Configure Identity Providers](#configure-identity-providers)
5. [Access Policies — Who Can Connect](#access-policies)
6. [Phone App Integration](#phone-app-integration)
7. [Per-Agent Policy Examples](#per-agent-policy-examples)
8. [Pricing Tiers](#pricing-tiers)

---

## Architecture

```
User/App
  │
  ▼
Cloudflare Edge (dash.cloudflare.com)
  │
  ├── Cloudflare Access Policy check ──── BLOCKED if not authenticated
  │   (Google SSO / email OTP / GitHub)
  │
  ▼ (authenticated)
Cloudflare Tunnel (outbound-only from VPS)
  │
  ▼
localhost:18789 (OpenClaw — loopback only)
  │
  ▼
OpenClaw token auth (second factor)
```

Zero traffic reaches the VPS unless it passes the Cloudflare Access identity check.

---

## Prerequisites

- Domain added to Cloudflare (nameservers pointing to Cloudflare)
- Cloudflare Zero Trust account (free tier: up to 50 users)
- Cloudflare Tunnel active for each agent (see `cloudflare-agent-tunnel` skill)
- OpenClaw running on loopback (`bind: "loopback"`)

---

## Create a Cloudflare Access Application

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → **Zero Trust** → **Access** → **Applications**
2. Click **Add an application** → **Self-hosted**
3. Fill in:
   - **Application name:** `OpenClaw - Koda`
   - **Session duration:** `24 hours` (or shorter for higher security)
   - **Application domain:** `koda.yourdomain.com`
4. Click **Next** → configure identity providers (see below)
5. Click **Next** → add access policy (see below)
6. **Save**

Repeat for each agent: one Cloudflare Access application per subdomain.

---

## Configure Identity Providers

In **Zero Trust → Settings → Authentication**, add one or more identity providers:

### Google SSO (recommended for teams)
1. Add **Google** as identity provider
2. Follow OAuth app setup in Google Cloud Console
3. Allows login with any Google account or restrict to specific domains (e.g. `@yourdomain.com`)

### One-Time PIN (email OTP — simplest)
1. Enable **One-time PIN** provider (requires no external OAuth setup)
2. Users enter their email → receive a 6-digit code → logged in
3. Good for external clients with no shared Google workspace

### GitHub
1. Add **GitHub** as identity provider
2. Restrict to specific GitHub organizations or individual users

---

## Access Policies

Each application has one or more policies that define who can access it.

### Example: Owner-only access
```
Policy name: Owner Only
Action:      Allow
Rules:
  - Selector: Emails
    Value:    charles@enspyredigital.com
```

### Example: Team access by email domain
```
Policy name: Team Access
Action:      Allow
Rules:
  - Selector: Emails ending in
    Value:    @yourdomain.com
```

### Example: Specific users + owner
```
Policy name: Client + Owner
Action:      Allow
Rules:
  - Selector: Emails
    Value:    charles@enspyredigital.com, client@theirdomain.com
```

### Block everyone except allowlist
Set the **default policy** to `Block` and add explicit `Allow` rules. Any email not in the allow list is rejected at the Cloudflare edge — the VPS never sees the request.

---

## Phone App Integration

Cloudflare Access uses a standard OAuth/OIDC flow. Your native mobile app can integrate it:

### Flow
1. App opens a browser/WebView to `https://koda.yourdomain.com`
2. Cloudflare Access redirects to identity provider login
3. User authenticates (Google, OTP, etc.)
4. Cloudflare issues a short-lived JWT (`CF_Authorization` cookie)
5. App stores this JWT and includes it on all subsequent WebSocket connections
6. When JWT expires, app re-triggers the auth flow

### Cloudflare Access Service Tokens (for machine-to-machine)
For programmatic app connections without a browser login:

1. **Zero Trust → Access → Service Auth → Service Tokens → Create Token**
2. Gives you a `CF-Access-Client-Id` + `CF-Access-Client-Secret`
3. App sends both headers on every request:
   ```
   CF-Access-Client-Id: <id>.access
   CF-Access-Client-Secret: <secret>
   ```
4. No browser login required — token never expires (until rotated)
5. **Best approach for a native phone app** connecting to a specific agent

Service tokens are ideal when your app IS the client — issue one token per app, revoke if compromised.

---

## Per-Agent Policy Examples

```
koda.yourdomain.com      → Policy: Emails = charles@enspyredigital.com
alex.yourdomain.com      → Policy: Emails ending in @yourdomain.com
client1.yourdomain.com   → Policy: Emails = client@theirdomain.com
                           (client only sees their own agent)
```

This gives you per-agent access control without any code changes to OpenClaw.

---

## Pricing Tiers

| Tier | Price | Users | What's included |
|---|---|---|---|
| **Free** | $0 | 50 MAU | Cloudflare Access, Tunnel, basic policies |
| **Teams** | $7/user/month | Unlimited | Access + Gateway + WARP device agent |
| **Enterprise** | Custom | Unlimited | Full SASE, custom contracts, SLAs |

For Access only (no Gateway/WARP): **$3/user/month** Access-only plan.

Reference: https://www.cloudflare.com/plans/zero-trust-services/

**For most OpenClaw deployments:** Free tier (50 users) covers personal + small team use. Teams tier needed when distributing to clients.
