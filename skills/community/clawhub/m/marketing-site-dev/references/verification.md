# Verification Checklist

Run this after a fresh `setup:cdn` + `cdn:refresh` to confirm the deploy actually works end-to-end. Each check is independent; failures point at distinct subsystems.

Use `/usr/bin/curl` rather than bare `curl` — see [landmines.md #8](landmines.md).

## 1. HTTP status + body size for every key route

```bash
APEX=example.com   # ← replace
for u in \
  https://${APEX}/                  \
  https://${APEX}/en/               \
  https://${APEX}/favicon.svg       \
  https://www.${APEX}/              \
  https://www.${APEX}/en/           ; do
  /usr/bin/curl -s -o /dev/null -w "%{http_code}  %{size_download}b  ${u}\n" --max-time 10 "${u}"
done
```

**Expected:** five `200` responses with non-trivial body sizes (typically 4-30 KB for HTML pages, 500-3000 bytes for the favicon).

**If you see `200` with a body that's plain JSON (`{"Code":"NoSuchKey"...}` or a bucket listing):** `OriginHost` is empty in the CDN config. Go fix the AddCdnDomain payload — see [landmines.md #3](landmines.md).

**If you see `403`:** the object exists but the per-object ACL is private. Re-run `pnpm run deploy:upload` — it sets `acl: 'public-read'` on every put. See [landmines.md #2c](landmines.md).

**If you see `404`:** Astro didn't emit the path (check `build.format: 'directory'` and `trailingSlash: 'always'` in `astro.config.mjs`), OR the file wasn't uploaded (check `dist/` matches what you expect after `pnpm build`).

## 2. HTTP → HTTPS redirect

```bash
/usr/bin/curl -sI http://${APEX}/ | head -3
```

**Expected:** `HTTP/1.1 301 Moved Permanently` with a `Location: https://${APEX}/` header.

**If you see `200`:** `ForcedRedirect` wasn't enabled. Re-run the `UpdateCdnConfig` step (step 11 in `cdn-setup.mjs`).

## 3. Certificate validity + SAN coverage

```bash
echo | openssl s_client -connect ${APEX}:443 -servername ${APEX} 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

**Expected:**
- `subject=CN = <APEX>` (or one of the SAN entries)
- `issuer=` something Let's Encrypt-ish or DigiCert depending on which cert you deployed
- `notBefore` < today < `notAfter`
- `X509v3 Subject Alternative Name:` containing BOTH `DNS:${APEX}` and `DNS:www.${APEX}`

**If SAN only covers apex (not www):** the cert you picked in step 9 of `cdn-setup.mjs` didn't cover www. Either find / issue / import one that does, then re-run `BatchDeployCert` with `--Domain "${APEX},www.${APEX}"`.

**If the cert is for `*.tos-cn-beijing.volces.com`:** CDN isn't actually serving — DNS still points at TOS directly. Wait 1-3 min more for DNS propagation, or re-check the CNAME records in `ve dns ListRecords`.

## 4. HSTS + HTTP/2 confirmation

```bash
/usr/bin/curl -sI --http2 https://${APEX}/ | grep -iE 'HTTP/|strict-transport-security|alt-svc'
```

**Expected:**
- `HTTP/2 200`
- `strict-transport-security: max-age=31536000` (one year)

**If you see `HTTP/1.1`:** HTTP/2 wasn't enabled. Check `UpdateCdnConfig` payload — `HTTPS.HTTP2: true`.

**If no HSTS header:** `HTTPS.Hsts.Switch: true` wasn't set or `Ttl` was 0.

## 5. CDN edge is actually caching

```bash
/usr/bin/curl -sI https://${APEX}/_astro/index.<hash>.js | grep -iE 'x-cache|cache-control|age'
```

**Expected:**
- `cache-control: public, max-age=31536000, immutable` (from your `_astro/` rule in `deploy.config.mjs`)
- `x-cache: HIT` (on the second request — first one populates the edge)
- `age:` > 0 on subsequent requests

**If `cache-control` says `max-age=0, must-revalidate`:** the cache rule didn't match — check the prefix in `deploy.config.mjs` and that `deploy.mjs` is reading it correctly.

## 6. Cache invalidation actually works

```bash
# Make a trivial content change to src/content/site.ts
pnpm run deploy && pnpm run cdn:refresh
# Wait ~30 seconds for the refresh task to propagate
/usr/bin/curl -s https://${APEX}/ | grep -i "<the new content>"
```

**Expected:** the new copy appears within ~30s.

**If old content lingers >2 minutes:** `cdn-refresh.mjs` got `InvalidParameter.Type` — confirm `Type: 'dir'` (NOT `directory`) in the request body. See [landmines.md #6](landmines.md).

## 7. Both languages render correctly

Open in a browser:

- `https://${APEX}/` → Chinese homepage, `<html lang="zh-CN">`
- `https://${APEX}/en/` → English homepage, `<html lang="en">`
- Language switcher in header swaps cleanly without 404s

Check the `<head>`:

- `<link rel="alternate" hreflang="zh-CN" href="..."/>`, same for `en` and `x-default`
- `<link rel="canonical" href="..."/>` matches the page being viewed
- OG + Twitter meta present

## All checks pass = done

If 1-7 all pass, the site is live and the deploy pipeline is working. Subsequent updates are:

```bash
pnpm run deploy && pnpm run cdn:refresh
```

…and re-running checks 1, 2, 6 is enough as a smoke test (no need to re-validate the cert + HSTS on every push).
