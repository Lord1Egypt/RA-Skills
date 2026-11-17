# Verification Method — huawei-cloud-rms-list

## Static / offline verification

- `validate-skill.sh` against the Huawei Cloud Skill Specification: structure,
  frontmatter, sections, size/extension limits, no hardcoded credentials, no
  cross-skill references — all PASS.
- Offline unit tests (mocked hcloud subprocess, no credentials, no network):

  ```bash
  python3 -m unittest discover -s tests -v
  ```

  Covered behaviour:
  - write-intent guard: read verbs pass; `CreateConfigurationAggregator`,
    `delete-aggregator`, `UpdateTrackerConfig`, `DeleteStoredQuery`, ... blocked;
    operation whitelist; value-flag exclusion; a following flag is still scanned.
  - operation resolution: default `ListAllResources`; `--provider`+`--type` →
    `ListResources`; `--list-providers` / `--list-regions`.
  - command construction: filters forwarded as real server-side parameters,
    `--domain_id`, `--X-Language`, `--limit` / `--marker` / `--offset`.
  - JSON extraction (with wrapper noise), and error-envelope classification,
    including the `RMS.00010006` permission envelope returned on **stdout with
    rc=0**.
  - paging: `page_info.next_marker` for resources; `offset` + `total_count` for
    ListProviders.
  - SDK fallback: triggered when `hcloud` is missing; missing env credentials
    raise `ConfigError`.
  - renderers: table / Markdown / CSV / JSON, incl. header-only empty output.
  - atomic export (temp file + rename, missing directory creation).

## Live read-only verification (executed during development)

Against the active hcloud profile in `cn-north-4`:

- `hcloud RMS ListProviders --cli-region=cn-north-4 --limit=3 --offset=1` — OK.
- `hcloud RMS ListRegions --cli-region=cn-north-4` — OK (21 regions).
- `hcloud RMS ListAllResources --cli-region=cn-north-4 --limit=1` — returned
  `RMS.00010006 You are not authorized with rms:resources:list`, which the script
  classified as an explicit permission error (the current IAM principal lacks the
  read permission; not a skill defect).

Full end-to-end read validation of the account-wide inventory requires an IAM
principal holding `rms:resources:list`; it is performed out-of-band by QA.

## API facts verified (not guessed)

- REST paths read from the `huaweicloudsdkrms` v1 `*_http_info` metadata:
  `/all-resources`, `/provider/{provider}/type/{type}/resources`, `/providers`,
  `/regions` (all under `/v1/resource-manager/domains/{domain_id}`).
- Request parameters verified against `ListAllResourcesRequest`,
  `ListResourcesRequest`, `ListProvidersRequest`, `ListRegionsRequest`.
- IAM action names verified via
  `hcloud IAM GetAuthorizationSchemaV5 --service_code=rms --cli-region=cn-north-4`.
