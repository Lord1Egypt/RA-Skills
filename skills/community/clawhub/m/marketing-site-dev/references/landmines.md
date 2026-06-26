# Landmines — Read Before Executing

Every item here represents at least one hour of debugging that has already happened. Read once. Refer back when a step does something unexpected.

Numbering is stable — other files reference items by number.

---

## 1. `HTTPS_PROXY` pollution

**Symptom:** TOS or Volcengine OpenAPI calls fail with `Error: Protocol "http:" not supported. Expected "https:"`.

**Cause:** `@volcengine/tos-sdk` uses axios under the hood, and axios auto-picks up `HTTPS_PROXY` from env. If the user runs a local HTTP proxy (Clash, Surge, etc.), every TOS call gets routed through it and the protocol mismatch surfaces.

**Fix:** at the top of every Node script that touches TOS or `open.volcengineapi.com`, delete the proxy env vars:

```js
for (const k of ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']) {
  delete process.env[k];
}
```

All scripts in [`../assets/scripts/`](../assets/scripts/) already do this. If you write a new script that talks to Volcengine, include the same preamble.

---

## 2. `@volcengine/tos-sdk` API inconsistencies

Three different gotchas — all in the same SDK package:

### 2a. `headBucket` takes a string, not an options object

```js
// ✓ correct
await client.headBucket(bucket);
// ✗ wrong — triggers "invalid bucket name, the character set is illegal"
await client.headBucket({ bucket });
```

### 2b. `listObjectsType2` signature mismatch when `continuationToken` is undefined

The signer includes ALL keys in the canonical string, but axios drops `undefined` from the URL. Result: server computes signature without the param, client computes with it → mismatch.

```js
// ✗ wrong
await client.listObjectsType2({ bucket, maxKeys: 1000, continuationToken: undefined });

// ✓ correct — only include the key when it has a value
const input = { bucket, maxKeys: 1000, listOnlyOnce: true };
if (continuationToken) input.continuationToken = continuationToken;
await client.listObjectsType2(input);
```

### 2c. `putObject` defaults to private even on a public-read bucket

`putBucketAcl` controls the BUCKET's ACL, not each object's. Forgetting `acl: 'public-read'` on individual `putObject` calls means the uploaded files 403 when served through CDN.

```js
await client.putObject({
  bucket, key, body, contentType, cacheControl, contentMD5,
  acl: 'public-read',   // ← required on every put
});
```

---

## 3. TOS has no separate "website endpoint" hostname

Unlike AWS S3, where you get `<bucket>.s3-website-<region>.amazonaws.com` as a distinct DNS name for static-site hosting, Volcengine TOS uses the same `<bucket>.tos-<region>.volces.com` for both raw API access and website serving. What changes the behavior is the **HTTP `Host` header**:

| `Host:` header                         | TOS response                                |
|----------------------------------------|---------------------------------------------|
| `<bucket>.tos-<region>.volces.com`     | Bucket listing JSON (API mode)              |
| A custom domain bound via `putBucketCustomDomain` | `index.html` with website routing rules    |

So two things must both be true:

1. **`setup-bucket.mjs` calls `putBucketCustomDomain`** for each apex + www domain. This is the binding that tells TOS "treat this Host header as website mode".
2. **`cdn-setup.mjs`'s `AddCdnDomain` payload sets `OriginHost` to the user's domain** (not empty, not the storage hostname). When the CDN edge fetches from origin, it forwards `OriginHost` as the upstream Host header. If `OriginHost` is empty, the storage hostname is used by default → TOS returns JSON → users see `{"Code":"NoSuchKey","Message":"..."}` instead of your homepage.

This is the single most common deploy failure. The payload templates in `assets/cdn-payloads/` have `OriginHost` set correctly — don't strip it.

---

## 4. CDN domain ownership verification uses a different convention than DCDN

Two superficially-similar Volcengine products with **different** verification mechanics:

| Product | TXT record host | Verification API |
|---|---|---|
| DCDN (全站加速) | `_dnsauth.<domain>` | `ve dcdn VerifyDomainOwnership` |
| **CDN (内容分发网络)** — what marketing sites use | **`volccdnauth.<domain>`** | **`cdn:CheckCdnDomain`** (NOT in `ve` CLI 1.0.x — sign via `volc-api.mjs`) |

The two systems are independent. Verifying a domain for DCDN does NOT satisfy CDN. Mixing them up means the verification poll never succeeds and you spin for 15 minutes wondering why.

Also: **free DV certificate APPLICATION is blocked with permanent AK/SK** (`OperationDenied.RequestFreeInstance` from `certificateservice:RequestFreeInstance`). Volcengine restricts this to the console UI. Listing / importing / deploying / canceling certs all work via API — only initial free issuance is gated.

So when no usable cert exists, the workflow is:

- **Option A**: apply free DV in console → 控制台 → 证书中心 → SSL证书 → 申请证书. The cert lands in the same account, and `BatchDeployCert` picks it up.
- **Option B**: issue from Let's Encrypt with `lego` or similar, then `ve certificateservice ImportCertificate`.

---

## 5. Modified TXT records take ~10 min to reflect at Volcengine's verifier

Per the docs. Modifying a TXT record restarts the cache aging at Volcengine's edge — so churning through multiple TXT variants compounds the wait, not shortens it.

**Get the host/value right the first time.** Specifically:

- For CDN verification: host = `volccdnauth`, type = `TXT`, value = whatever `DescribeRetrieveInfo` returns.
- For DCDN verification (different skill, but easy to confuse): host = `_dnsauth`.

`cdn-setup.mjs` cleans stale `volccdnauth` records first then creates the new one — but only after fetching the current value, never speculating.

---

## 6. `pnpm deploy` collides with a pnpm built-in

`pnpm deploy` is **pnpm's workspace command** for shipping a single package as a standalone deployable. Running it in a non-workspace repo errors with:

```text
ERR_PNPM_CANNOT_DEPLOY
```

Any custom `deploy` script in `package.json` must be invoked as **`pnpm run deploy`** (or just `pnpm deploy` won't reach the script — pnpm dispatches to the built-in first).

Document this in the project's README:

```md
> ⚠️ Always use `pnpm run deploy` and `pnpm run cdn:refresh`. Bare `pnpm deploy` hits a pnpm built-in.
```

The same applies to any `script` name that collides with a pnpm built-in (`install`, `add`, `update`, `link`, `unlink`, `outdated`, `prune`, `rebuild`, `publish`, `store`, …). For project scripts, `run` prefix is the safe default.

---

## 7. Free DV certs are often already issued at domain registration

Before walking the user through a cert application, **list existing instances** to see if there's a free auto-gift cert already in the account:

```bash
ve certificateservice CertificateGetInstanceList --body '{"Limit": 50}'
```

Watch out for these response-shape pitfalls:

- The wrapper field is **`Result.Instances`** — not `InstanceList`, not `Data`. Easy to misread from intuition.
- Free auto-gift certs have `OrderBrand: digicert_free_activity` and `InstanceLevel: dv`.
- Filter by `Status === 'Issued'` AND look at the `San` array — a usable cert needs BOTH the apex and `www.<apex>` in SAN, not just one.

If a usable cert is found, skip straight to `BatchDeployCert` with that `InstanceId`. If not, fall back to console application (landmines.md #4).

---

## 8. `/usr/bin/curl` is more reliable than bare `curl` after long-running commands

Anecdote turned best practice: in some shells, after a long-running command (especially something that touched PATH), bare `curl` resolution occasionally goes weird (aliased to a Homebrew shim, resolves to a stale binary, etc.). Using the absolute path `/usr/bin/curl` avoids the lookup entirely.

Use `/usr/bin/curl` in the verification checklist and in any user-facing instructions. For programmatic checks, use Node's built-in `fetch` instead — same reliability, fewer environment variables to worry about.
