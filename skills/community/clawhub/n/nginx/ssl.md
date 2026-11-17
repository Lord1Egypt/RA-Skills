# SSL/TLS: Traps and Diagnosis

## Certificates & Chain

- `ssl_certificate` = fullchain: leaf first, then intermediates, never the root. Wrong order or leaf-only passes on machines with cached intermediates and fails on fresh clients/older Androids — the "works on my browser" cert bug.
- Verify what's actually served, not what's on disk: `openssl s_client -connect host:443 -servername host` — check the chain depth and `Verify return code: 0`.
- Key/cert mismatch = nginx refuses to start with `SSL_CTX_use_PrivateKey_file... key values mismatch`. Compare `openssl x509 -noout -modulus` vs `openssl rsa -noout -modulus`.
- Expired cert: nginx starts fine, browsers reject. Cert lifecycle monitoring is not nginx's job — see the `ssl` skill for issuance/renewal.
- Cert for `example.com` does not cover `www.example.com` — SAN must list both, or wildcard (`*.example.com` covers www but NOT the apex; you need both entries).

## Modern Baseline

```nginx
listen 443 ssl;
http2 on;                                  # nginx >=1.25.1; older: listen 443 ssl http2;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;             # modern advice; "on" was TLS1.2-era
ssl_session_cache shared:SSL:10m;          # ~4000 sessions per MB, shared across workers
ssl_session_timeout 1d;
```

- Start from the Mozilla SSL config generator (intermediate profile); hand-rolled `ssl_ciphers` lists rot.
- `ssl_ciphers` governs TLS ≤1.2 only. TLS1.3 suites are set via `ssl_conf_command Ciphersuites` — if a scanner flags a TLS1.3 suite, editing `ssl_ciphers` will change nothing.
- `ssl on;` is removed in modern nginx — `listen 443 ssl` is the only form.
- `ssl_session_tickets off` if you can't rotate ticket keys — static ticket keys undermine forward secrecy across restarts.

## The Redirect Loop (behind CDN/LB)

CDN terminates TLS, talks HTTP to nginx → nginx sees `$scheme = http` → redirects to https → CDN fetches again over http → loop.

```nginx
# redirect only when the ORIGINAL request was http:
if ($http_x_forwarded_proto = "http") { return 301 https://$host$request_uri; }
```

Only trust that header when a known LB sets it (strip/overwrite it at the edge). Standalone nginx keeps the simple form: a port-80 server with `return 301 https://$host$request_uri;`.

## HSTS (a one-way door)

- Rollout ramp: `max-age=300` first, verify every subdomain serves valid TLS, then raise to `max-age=31536000` (1 year, the preload-list minimum).
- `includeSubDomains` breaks any HTTP-only internal subdomain for every visitor's browser until max-age expires — audit subdomains BEFORE, not after.
- HSTS + broken cert = browsers offer no bypass button. That's the feature; it's also why you ramp.
- Apply via `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;` — the `always` flag makes it apply to error responses too, and remember `add_header` inheritance (any add_header in a location wipes inherited ones).

## OCSP Stapling

- Requires `ssl_stapling on; ssl_stapling_verify on; ssl_trusted_certificate <chain>;` AND a `resolver` — missing pieces disable stapling silently (only an error-log warning).
- The FIRST request after startup is never stapled: nginx fetches the OCSP response asynchronously. Test with a second `openssl s_client -status` call.
- CA OCSP responders can be slow — stapling moves that latency from every client to nginx's background fetch, which is the point.

## Client Certificates (mTLS)

- `ssl_client_certificate` is the CA that signs client certs, not any client's cert.
- `ssl_verify_client optional` + check `$ssl_client_verify = "SUCCESS"` in the app/location — lets you serve a friendly 403 instead of a TLS-level handshake failure. The variable is the string `SUCCESS`, not a boolean.
- No CRL/OCSP for client certs unless you configure `ssl_crl` — revoked client certs keep working otherwise.
- Pass identity upstream explicitly: `proxy_set_header X-Client-DN $ssl_client_s_dn;` — the backend can't see the TLS layer.

## HTTP/2 and HTTP/3

- `http2 on;` is a server-level directive since nginx >=1.25.1; `listen ... http2` is the deprecated spelling.
- HTTP/2 to the client + HTTP/1.1 to upstream is normal and fine — multiplexing gains are on the client leg where latency lives.
- HTTP/3/QUIC: `listen 443 quic;` (nginx >=1.25) + advertise with `add_header Alt-Svc 'h3=":443"; ma=86400';` — clients discover h3 via that header, not automatically.
- Header-heavy clients on HTTP/2 may need `large_client_header_buffers` raised — symptom is 400s only from some browsers.
