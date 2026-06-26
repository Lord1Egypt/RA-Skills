# Phase 2 — Deploy to Volcengine

Detailed walkthrough for the deploy half. Read [landmines.md](landmines.md) FIRST — half of the time you spend in Phase 2 is avoiding landmines, not running commands.

## What `ve` CLI can and cannot do

| Can | Cannot |
|---|---|
| All CDN management (`ve cdn AddCdnDomain`, `UpdateCdnConfig`, `BatchDeployCert`, `SubmitRefreshTask`, …) | TOS data plane (upload / list / delete objects) — no service namespace exists |
| All DNS management (`ve dns ListZones`, `CreateRecord`, `UpdateRecord`, `DeleteRecord`) | TOS bucket-level metadata that `ve` doesn't ship (`CreateBucket`, `PutBucketWebsite`, `PutBucketCustomDomain`) |
| Certificate listing / import / cancellation (`ve certificateservice CertificateGetInstanceList`, `ImportCertificate`) | Free DV cert **APPLICATION** — Volcengine blocks free issuance with permanent AK/SK (`OperationDenied.RequestFreeInstance`). Free DV is console-only. |
| DCDN domain ownership (`ve dcdn VerifyDomainOwnership`) | **CDN domain ownership** (`DescribeRetrieveInfo` / `CheckCdnDomain` exist in API v2021-03-01 but are NOT in `ve` CLI 1.0.x) |

**Mitigation:** for any API missing from `ve`, sign requests yourself with Volcengine SigV4 using Node's built-in `crypto` — zero dependencies. That's exactly what [`../assets/scripts/lib/volc-api.mjs`](../assets/scripts/lib/volc-api.mjs) does. Use it as the escape hatch whenever the local `ve` binary is too old.

## The 5 scripts that ship in `assets/scripts/`

All five are designed to be **idempotent** — re-running picks up where it left off rather than re-creating things. Copy them into `scripts/` in the user's project as-is. The only thing that should change per project is `deploy.config.mjs`.

### 1. `lib/volc-api.mjs` — SigV4 signer

Zero deps. Exports a single `callVolc({ service, region, action, version, body })` function. Reads `VOLC_ACCESS_KEY` / `VOLC_SECRET_KEY` from env. **Deletes proxy env vars at the top of every call** (see landmines.md #1 — TOS SDK + local HTTP proxy = signature failure).

### 2. `setup-bucket.mjs` — one-shot bucket setup

Uses `@volcengine/tos-sdk`. Performs in order:

1. `client.headBucket(bucket)` — if it 404s, `client.createBucket({ bucket, acl: 'public-read', storageClass: 'STANDARD' })`. **Note: `headBucket` takes a STRING, not `{ bucket }`** — see landmines.md #2.
2. `client.putBucketWebsite({ bucket, indexDocument: { suffix: 'index.html' }, errorDocument: { key: '404.html' } })`
3. `client.putBucketCustomDomain({ bucket, customDomainRule: { domain } })` × 2 (apex + www)

### 3. `deploy.mjs` — TOS sync uploader

Uses `@volcengine/tos-sdk` + `mime`. Performs:

1. Walks `dist/` recursively
2. For each file, `client.putObject({ bucket, key, body, contentType, cacheControl, contentMD5, acl: 'public-read' })`. **`acl: 'public-read'` on every put** — see landmines.md #2; TOS defaults objects to private even on a public-read bucket.
3. `cacheControl` is picked from `deploy.config.mjs`'s `cacheRules` (first matching prefix wins) with `defaultCacheControl` as fallback.
4. Lists remote keys via `listObjectsType2` (see landmines.md #2 for the continuation-token gotcha — only pass the token in the input when it has a value, otherwise signature fails) and deletes orphans via `deleteMultiObjects` in chunks of 1000.

### 4. `cdn-setup.mjs` — orchestrate CDN end-to-end

The most fiddly script. Steps in order:

| # | What | Tool |
|---|---|---|
| 1 | `ve dns ListZones --SearchKeyWord <root-domain>` → resolve ZID | `ve` |
| 2 | `cdn:DescribeRetrieveInfo` → get TXT host (`volccdnauth`) + value | `volc-api.mjs` (NOT in `ve` 1.0.x) |
| 3 | Clean stale `volccdnauth` TXT, create the new one | `ve dns DeleteRecord` + `CreateRecord` |
| 4 | Poll `cdn:CheckCdnDomain` every 30s until `Result.Status === 'success'`, bail at 30 attempts | `volc-api.mjs` |
| 5 | `ve cdn AddCdnDomain --body @scripts/cdn-payloads/apex.json` × 2 (apex + www) | `ve` |
| 6 | `ve cdn StartCdnDomain` × 2 | `ve` |
| 7 | `ve cdn ListCdnDomains` → read each domain's `Cname` field | `ve` |
| 8 | Upsert apex `@` + `www` CNAME records pointing to CDN targets | `ve dns CreateRecord` / `UpdateRecord` |
| 9 | `ve certificateservice CertificateGetInstanceList --body '{"Limit":50}'` → find a cert whose `San` covers both apex + www | `ve` |
| 10 | `ve cdn BatchDeployCert --body '{"CertId":"<id>","Domain":"apex,www"}'` | `ve` |
| 11 | `ve cdn UpdateCdnConfig` per domain to enable HTTPS hardening | `ve` |
| 12 | Print final URLs + cert expiration date | — |

The HTTPS hardening payload for step 11 (per domain):

```json
{
  "Domain": "<the domain>",
  "HTTPS": {
    "Switch": true,
    "HTTP2": true,
    "ForcedRedirect": { "EnableForcedRedirect": true, "StatusCode": "301" },
    "Hsts": { "Switch": true, "Ttl": 31536000, "Subdomain": "exclude" },
    "TlsVersion": ["tlsv1.2", "tlsv1.3"]
  }
}
```

Step 9 — **always list before applying**. Free DV certs are often pre-issued at domain registration with `OrderBrand: digicert_free_activity` and `InstanceLevel: dv`. The response field is `Result.Instances` (NOT `InstanceList`, NOT `Data` — easy to read wrong from intuition).

If no usable cert exists, tell the user to either:

- Apply free DV in console at **控制台 → 证书中心 → SSL证书 → 申请证书** (the API for free issuance is blocked with permanent AK/SK — see landmines.md #4), OR
- Use `lego` or similar to issue from Let's Encrypt and `ve certificateservice ImportCertificate` it.

### 5. `cdn-refresh.mjs` — cache invalidation

Uses `volc-api.mjs` (NOT `ve` CLI — must work in CI without the binary). Calls `cdn:SubmitRefreshTask` with `{ Type: 'dir', Urls: '<url1>\n<url2>' }`.

**`Type` is `'dir'`** — not `'directory'`. The latter returns `InvalidParameter.Type`. Common typo.

## Execution order (first deploy)

```bash
pnpm install
pnpm build                          # verify build works locally first
pnpm run setup:bucket               # idempotent: bucket + website + custom domain bind
pnpm run deploy:upload              # sync dist/ to bucket
# at this point: https://<bucket>.tos-<region>.volces.com/index.html should 200
pnpm run setup:cdn                  # verification + CDN add + start + CNAME + cert + HTTPS hardening
# wait 1-3 min for DNS propagation
pnpm run cdn:refresh                # purge cache so first hits don't get bucket-listing JSON
```

After this initial run, daily iteration becomes one command:

```bash
pnpm run deploy && pnpm run cdn:refresh
```

## Environment

`.env` at project root (gitignored). The scripts are launched via `node --env-file-if-exists=.env` so the file is loaded automatically — no `dotenv` package needed.

```env
VOLC_ACCESS_KEY=AK...
VOLC_SECRET_KEY=...
```

The Volcengine AK/SK must have permission for: `TOSFullAccess`, `CDNFullAccess`, `DNSFullAccess`, `CertificateFullAccess`. For least-privilege, scope to the specific bucket / domain / zone you're working with.

## CDN payload templates (`assets/cdn-payloads/`)

[`apex.json`](../assets/cdn-payloads/apex.json) and [`www.json`](../assets/cdn-payloads/www.json) use `{{DOMAIN}}`, `{{BUCKET}}`, `{{REGION}}` placeholders. `cdn-setup.mjs` substitutes them at runtime (or copy the files into the user's project with the values pre-filled — both work).

**`OriginHost` MUST be set to the same domain being added** (apex domain in `apex.json`, `www.<domain>` in `www.json`) — not empty, not the storage hostname. Empty `OriginHost` causes TOS to receive its own `*.tos-<region>.volces.com` hostname as Host, which returns bucket-listing JSON instead of the website-bound `index.html`. This is the single biggest landmine in the whole workflow — see landmines.md #3 for the why.

## When something doesn't work

1. **TOS upload returns 403 / signature mismatch** → check landmines.md #1 (proxy pollution) and #2 (continuation-token / headBucket signature).
2. **CDN verification stuck on `failed`** → check landmines.md #4 (CDN ≠ DCDN — TXT host is `volccdnauth`, NOT `_dnsauth`).
3. **Visiting the domain returns bucket-listing JSON** → check landmines.md #3 (`OriginHost` empty).
4. **HTTPS not enforced after BatchDeployCert** → step 11's `UpdateCdnConfig` didn't run or applied to wrong domain. Re-run; idempotent.
5. **Refresh task rejected** → `Type` typo (`directory` vs `dir`).
6. **`pnpm deploy` errors with `ERR_PNPM_CANNOT_DEPLOY`** → see landmines.md #6. Use `pnpm run deploy`.
