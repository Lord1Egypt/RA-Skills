---
name: jwt-debugger
description: Decode, validate, and debug JSON Web Tokens. Inspect headers, payloads, signatures, expiration, claims, and key mismatches. Diagnose common JWT issues in authentication flows without external tools.
---

# JWT Debugger

Decode and debug JWTs without pasting them into random websites. Inspect headers, validate signatures, check expiration and claims, diagnose key mismatches, and trace authentication failures — all locally, keeping tokens secure.

Use when: "debug jwt", "decode this token", "why is auth failing", "jwt expired", "invalid signature", "token validation error", "check jwt claims", or when troubleshooting authentication.

## Commands

### 1. `decode` — Decode and Inspect JWT

```bash
# Decode without signature verification (inspection only)
echo "$TOKEN" | python3 -c "
import sys, json, base64

token = sys.stdin.read().strip()
parts = token.split('.')
if len(parts) != 3:
    print(f'❌ Invalid JWT: expected 3 parts, got {len(parts)}')
    sys.exit(1)

def decode_part(s):
    padding = 4 - len(s) % 4
    s += '=' * padding
    return json.loads(base64.urlsafe_b64decode(s))

header = decode_part(parts[0])
payload = decode_part(parts[1])

print('=== HEADER ===')
print(json.dumps(header, indent=2))
print()
print('=== PAYLOAD ===')
print(json.dumps(payload, indent=2))
print()

# Check expiration
import time
if 'exp' in payload:
    exp = payload['exp']
    now = int(time.time())
    remaining = exp - now
    if remaining < 0:
        print(f'🔴 EXPIRED: {abs(remaining)//3600}h {abs(remaining)%3600//60}m ago')
    elif remaining < 300:
        print(f'🟡 EXPIRING SOON: {remaining}s remaining')
    else:
        print(f'🟢 Valid: {remaining//3600}h {remaining%3600//60}m remaining')

if 'iat' in payload:
    from datetime import datetime, timezone
    issued = datetime.fromtimestamp(payload['iat'], tz=timezone.utc)
    print(f'Issued at: {issued.isoformat()}')

if 'nbf' in payload:
    nbf = payload['nbf']
    now = int(time.time())
    if now < nbf:
        print(f'🔴 NOT YET VALID: becomes valid in {nbf - now}s')

# Common claims
for claim, label in [('sub', 'Subject'), ('iss', 'Issuer'), ('aud', 'Audience'), ('scope', 'Scopes'), ('roles', 'Roles')]:
    if claim in payload:
        print(f'{label}: {payload[claim]}')

print(f'\\nAlgorithm: {header.get(\"alg\", \"MISSING\")}')
print(f'Key ID: {header.get(\"kid\", \"not set\")}')
print(f'Type: {header.get(\"typ\", \"not set\")}')
"
```

### 2. `validate` — Full Signature Verification

```bash
# Verify with known secret (HS256)
python3 -c "
import sys, hmac, hashlib, base64

token = '$TOKEN'
secret = '$SECRET'
parts = token.split('.')
signing_input = f'{parts[0]}.{parts[1]}'.encode()
signature = base64.urlsafe_b64decode(parts[2] + '==')
expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
if hmac.compare_digest(signature, expected):
    print('✅ Signature VALID')
else:
    print('❌ Signature INVALID — secret mismatch or token tampered')
"

# Verify with public key (RS256/ES256)
python3 -c "
import jwt  # pip install PyJWT[crypto]
try:
    decoded = jwt.decode('$TOKEN', '$PUBLIC_KEY', algorithms=['RS256'], audience='$EXPECTED_AUD')
    print('✅ Valid:', decoded)
except jwt.ExpiredSignatureError:
    print('❌ Token expired')
except jwt.InvalidSignatureError:
    print('❌ Invalid signature — wrong key or tampered token')
except jwt.InvalidAudienceError:
    print('❌ Audience mismatch')
except Exception as e:
    print(f'❌ {e}')
"
```

### 3. `diagnose` — Common JWT Problems

Check for these issues:

**Expiration issues:**
- Token expired → check clock sync between issuer and validator
- Token not yet valid (nbf) → clock skew between services
- Very short TTL (< 5 min) → may cause issues with slow requests

**Signature issues:**
- "none" algorithm → security vulnerability, reject immediately
- Algorithm mismatch → server expects RS256, token has HS256
- Wrong key → key rotation happened, old key used
- kid mismatch → key ID in header doesn't match available keys

**Claims issues:**
- Missing required claims (iss, sub, aud, exp)
- Audience mismatch → token issued for service A, used with service B
- Issuer mismatch → token from wrong identity provider
- Scope insufficient → token has read scope, endpoint requires write

**Security red flags:**
- `alg: "none"` → algorithm confusion attack
- `alg: "HS256"` with RSA public key → key confusion attack
- Token in URL query parameter → logged in server logs, browser history
- Token size > 8KB → may exceed header size limits
- Sensitive data in payload (passwords, SSN) → payload is base64, not encrypted

```markdown
# JWT Diagnostic Report

## Token Summary
- Algorithm: RS256
- Issuer: auth.example.com
- Subject: user-12345
- Issued: 2026-04-29 01:00:00 UTC
- Expires: 2026-04-29 02:00:00 UTC (🔴 EXPIRED 31m ago)

## Issues Found
1. 🔴 **Expired** — token expired 31 minutes ago
   Fix: refresh token or re-authenticate

2. 🟡 **No audience claim** — token doesn't specify intended audience
   Risk: token accepted by unintended services
   Fix: add `aud` claim to token issuer config

3. 🟢 Algorithm: RS256 (secure)
4. 🟢 Key ID present: matches current JWKS
```

### 4. `compare` — Diff Two Tokens

Compare tokens side-by-side to identify what changed:
- Different claims (permissions changed?)
- Different expiry (session settings changed?)
- Different issuer (wrong auth provider?)
- Different kid (key rotated?)

### 5. `generate` — Create Test JWT

Generate a signed JWT for testing:
```bash
python3 -c "
import jwt, time, json
payload = {
    'sub': 'test-user',
    'iss': 'test-issuer',
    'aud': 'test-audience',
    'iat': int(time.time()),
    'exp': int(time.time()) + 3600,
    'scope': 'read write'
}
token = jwt.encode(payload, 'test-secret', algorithm='HS256')
print(token)
"
```
