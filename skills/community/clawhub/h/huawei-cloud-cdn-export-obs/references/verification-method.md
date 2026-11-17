# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/cdn/huawei-cloud-cdn-export-obs
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeHcloud`) that dispatches on
  the argv (CDN vs OBS) — no credentials, no network, deterministic.
- Every code path is exercised: CDN write-intent guard, CDN command construction
  + filters, JSON extraction, `total` paging, CDN failure classification
  (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0), CDN SDK fallback;
  serialization (json / csv / md / empty table / pipe escaping / tags
  flattening), default file naming, atomic file write (directory creation, bad
  path); OBS helpers (`parse_obs_url`, cp/stat argv, operation whitelist, stat
  parsing, not-found detection), object existence probe (exists / not-found /
  auth / SDK fallback), upload (new object / overwrite refusal / overwrite
  allowed / read-back size mismatch / missing local file / SDK fallback / API
  error propagation); and the end-to-end entry point (json/csv/md,
  `--export-only`, no-bucket skip, overwrite refusal/allowed, empty region, guard
  blocking, default key, local path containing a write word).
- The SDK fallbacks (CDN + OBS) are tested with module-level mocks so no real SDK
  import or network access is required.

## Live verification (when credentials exist — QA stage)

```bash
hcloud configure list                                             # CDN profile check
hcloud CDN ListDomains --cli-region=cn-north-4 --page_size=1     # CDN API sanity
python3 scripts/cdn_export_obs.py --export-only --format md --output /tmp/cdn.md
python3 scripts/cdn_export_obs.py --bucket <bucket> --key verify/cdn_domains.json
python3 scripts/cdn_export_obs.py --bucket <bucket> --key verify/cdn_domains.json   # 2nd run: refuses overwrite
python3 scripts/cdn_export_obs.py --bucket <bucket> --key verify/cdn_domains.json --overwrite
hcloud OBS stat obs://<bucket>/verify/cdn_domains.json -e=obs.cn-north-4.myhuaweicloud.com
```

## API / parameter provenance

Verified against the installed official SDKs (no endpoint or parameter inferred
from naming patterns):

- `huaweicloudsdkcdn` v1 `CdnClient._list_domains_http_info` declares
  `method = GET`, `resource_path = /v1.0/cdn/domains`. `ListDomainsRequest` real
  query parameters: `domain_name`, `business_type`, `domain_status`,
  `service_area`, `page_size`, `page_number`, `show_tags`, `exact_match`,
  `enterprise_project_id`; paging is `page_size` + `page_number`; the response
  carries `total`.
- `huaweicloudsdkobs` v1 `ObsClient._put_object_http_info` declares
  `method = PUT`, `resource_path = /{object_key}` (body = file stream), and
  `ObsClient._head_object_http_info` declares `method = HEAD`,
  `resource_path = /{object_key}` (`HeadObjectResponse.content_length` /
  `.e_tag`).
- KooCLI `hcloud OBS` is obsutil-backed (lowercase `cp` / `stat`; endpoint via
  `-e=`), consistent with the sibling OBS listing skill.

## Environment note

The development environment had `huaweicloudsdkcdn` / `huaweicloudsdkcore`
installed but **not** `huaweicloudsdkobs`; the OBS SDK fallback was therefore
covered with a module-level mock, and `ensure_env.py` declares
`huaweicloudsdkobs` among the packages it installs. The KooCLI paths could not be
executed live in-session (no credentials were provided at development time); the
real read-only / write verification is performed by the QA agent out-of-band.