---
name: oauth-debugger
description: Debug OAuth 2.0 and OIDC flows. Trace authorization code, PKCE, client credentials, and implicit flows. Diagnose redirect URI mismatches, scope issues, token exchange failures, and JWKS configuration problems.
---

# OAuth Debugger

Debug OAuth 2.0 and OpenID Connect flows without guessing. Trace each step of the authorization flow, identify where it breaks (redirect URI mismatch, scope issue, token exchange failure, JWKS misconfiguration), and provide the exact fix.

Use when: "oauth not working", "redirect URI mismatch", "invalid_grant", "login flow broken", "OIDC configuration", "token exchange failing", "PKCE error", "authorization code error", or when SSO/social login breaks.

## Commands

### 1. `trace` — Trace OAuth Flow Step by Step

#### Step 1: Discover OAuth Configuration

```bash
# OpenID Connect discovery
curl -s "https://$AUTH_DOMAIN/.well-known/openid-configuration" | python3 -c "
import json, sys
config = json.load(sys.stdin)
print('Authorization endpoint:', config.get('authorization_endpoint', '❌ MISSING'))
print('Token endpoint:', config.get('token_endpoint', '❌ MISSING'))
print('JWKS URI:', config.get('jwks_uri', '❌ MISSING'))
print('Supported flows:', config.get('grant_types_supported', ['not listed']))
print('Supported scopes:', config.get('scopes_supported', ['not listed']))
print('Token signing:', config.get('id_token_signing_alg_values_supported', ['not listed']))
"

# Check JWKS endpoint
curl -s "https://$AUTH_DOMAIN/.well-known/jwks.json" | python3 -c "
import json, sys
jwks = json.load(sys.stdin)
for key in jwks.get('keys', []):
    print(f'Key ID: {key.get(\"kid\")} | Algorithm: {key.get(\"alg\")} | Use: {key.get(\"use\")}')
"
```

#### Step 2: Validate Authorization Request

For Authorization Code + PKCE flow:
```bash
# Check the authorization URL construction
# Required parameters:
# - response_type=code
# - client_id=<your app>
# - redirect_uri=<must match exactly>
# - scope=<requested scopes>
# - state=<CSRF protection>
# - code_challenge=<PKCE S256 hash>
# - code_challenge_method=S256

python3 -c "
import hashlib, base64, secrets
verifier = secrets.token_urlsafe(32)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
print(f'code_verifier: {verifier}')
print(f'code_challenge: {challenge}')
print(f'code_challenge_method: S256')
"
```

#### Step 3: Diagnose Token Exchange

```bash
# Test token exchange
curl -s -X POST "https://$AUTH_DOMAIN/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=$AUTH_CODE" \
  -d "redirect_uri=$REDIRECT_URI" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "code_verifier=$CODE_VERIFIER" | python3 -c "
import json, sys
resp = json.load(sys.stdin)
if 'access_token' in resp:
    print('✅ Token exchange successful')
    print(f'Access token type: {resp.get(\"token_type\")}')
    print(f'Expires in: {resp.get(\"expires_in\")}s')
    print(f'Scopes: {resp.get(\"scope\")}')
    if 'id_token' in resp:
        print(f'ID token: present')
    if 'refresh_token' in resp:
        print(f'Refresh token: present')
else:
    print(f'❌ Error: {resp.get(\"error\")}')
    print(f'Description: {resp.get(\"error_description\")}')
"
```

### 2. `diagnose` — Common OAuth Errors

**`invalid_grant`:**
- Authorization code expired (usually 10 min TTL) → re-authorize
- Code already used (one-time use) → don't retry, re-authorize
- Redirect URI in token request doesn't match authorize request → exact match required
- PKCE verifier doesn't match challenge → check encoding

**`redirect_uri_mismatch`:**
- Trailing slash matters: `http://localhost:3000` ≠ `http://localhost:3000/`
- Scheme matters: `http` ≠ `https`
- Port matters: `localhost:3000` ≠ `localhost:3001`
- Path matters: `/callback` ≠ `/auth/callback`
- Check provider's registered redirect URIs list

**`invalid_client`:**
- Wrong client_id or client_secret
- Client credentials not sent correctly (Basic auth vs POST body)
- Client deleted or disabled in provider

**`invalid_scope`:**
- Requested scope not enabled for this client
- Scope format wrong (space-separated, not comma)
- Provider renamed scope (e.g., `email` → `openid email`)

**`access_denied`:**
- User denied consent
- Admin consent required but user is not admin
- Conditional access policy blocked the request

```markdown
# OAuth Debug Report

## Flow: Authorization Code + PKCE
## Provider: Auth0 (tenant.auth0.com)

## Trace
1. ✅ Discovery: .well-known/openid-configuration found
2. ✅ Authorization request: valid parameters
3. ✅ User authenticated and consented
4. ❌ Token exchange: `invalid_grant`

## Diagnosis
- Redirect URI in token request: `http://localhost:3000/callback`
- Redirect URI in authorize request: `http://localhost:3000/callback/`
- 🔴 **Trailing slash mismatch** — must be identical in both requests

## Fix
Change redirect_uri in token request to `http://localhost:3000/callback/` (with trailing slash)
OR update authorize request to omit trailing slash.
Also update provider's registered redirect URIs to match.
```

### 3. `test-flow` — Simulate OAuth Flows

**Client Credentials (machine-to-machine):**
```bash
curl -s -X POST "https://$AUTH_DOMAIN/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "audience=$API_AUDIENCE"
```

**Refresh Token:**
```bash
curl -s -X POST "https://$AUTH_DOMAIN/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "client_id=$CLIENT_ID"
```

### 4. `security-check` — Audit OAuth Implementation

Flag security issues:
- Implicit flow in use (deprecated, tokens in URL fragment)
- No PKCE on public clients (authorization code interception)
- State parameter missing (CSRF vulnerability)
- Token in URL query string (logged everywhere)
- Wildcard redirect URIs (open redirect)
- Long-lived access tokens without refresh (> 1 hour)
- Client secret in frontend code (exposed to users)
