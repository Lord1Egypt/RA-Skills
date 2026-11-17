# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/cdn/huawei-cloud-cdn-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_domains_via_sdk` mock (no real SDK
  import, no network), plus a live regression test that constructs the real
  `ListDomainsRequest` when `huaweicloudsdkcdn` is installed (skipped
  otherwise).
- Cases cover: write-intent guard, command construction (filters forwarded
  server-side; page_number paging), JSON extraction, failure classification
  (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0), total-based paging
  (page_number increment / full page / empty), SDK fallback (success /
  unavailable / pagination), rendering, and all main() output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                              # profile check
hcloud CDN ListDomains --cli-region=cn-north-4 --page_size=1       # API sanity
python3 scripts/list_cdn.py --region cn-north-4                    # full flow
python3 scripts/list_cdn.py --json | python3 -m json.tool >/dev/null  # JSON validity
python3 scripts/list_cdn.py --names-only
python3 scripts/list_cdn.py --domain-status online                 # server-side filter
python3 scripts/list_cdn.py --business-type web
```

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdkcdn` (3.1.219); no
endpoint or parameter was inferred from naming patterns:

- `huaweicloudsdkcdn` v1 `cdn_client._list_domains_http_info` declares
  `method = GET`, `resource_path = /v1.0/cdn/domains`.
- `ListDomainsRequest` real query parameters: `domain_name`, `business_type`,
  `domain_status`, `service_area`, `page_size`, `page_number`, `show_tags`,
  `exact_match`, `enterprise_project_id`.
- Paging is `page_size` + `page_number`; the response carries a `total`
  accelerated-domain count.
- `ListDomainsResponse` fields: `total`, `domains` (`Domains` items),
  `x_request_id`.
- `Domains` fields: `id`, `domain_name`, `business_type`, `domain_status`,
  `cname`, `user_domain_id`, `service_area`, `https_status`, `disabled`,
  `locked`, `locked_reason`, `banned_reason`, `origin_status`, `range_status`,
  `follow_status`, `auto_refresh_preheat`, `sources`, `domain_origin_host`,
  `enterprise_project_id`, `tags`, `create_time`, `modify_time`.
- IAM action `cdn:domain:list` recorded from the Issue #52 spec / official CDN
  API reference.

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path could not be executed live; its command/parameter shape is derived
from the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The
in-session functional smoke used a same-shape mock `hcloud` (see
`templates/test-vars.json`); the SDK fallback path was import-verified against
the installed `huaweicloudsdkcdn`.