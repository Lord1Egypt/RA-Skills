# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| hcloud service catalog (authoritative) | `hcloud CDN ListDomains --cli-region=cn-north-1 --help`: `method=GET`; params `--cli-region` (required), `--domain_name`, `--business_type`, `--domain_status`, `--service_area`, `--enterprise_project_id`, `--exact_match`, `--show_tags`, `--page_size` (1~10000), `--page_number` (1~65535) — all real server-side query parameters |
| SDK `_http_info` (authoritative) | `huaweicloudsdkcdn` v1 `cdn_client.py` → `_list_domains_http_info` → `"method": "GET"`, `"resource_path": "/v1.0/cdn/domains"`; `ListDomainsRequest` kwargs: `domain_name / business_type / domain_status / service_area / page_size / page_number / show_tags / exact_match / enterprise_project_id` |
| SDK response model | `ListDomainsResponse` → `total`, `domains`; paging uses `page_size` + `page_number` over the reported `total`; CDN is global (`GlobalCredentials` + `CdnRegion`) |
| Region catalog | `hcloud CDN ListDomains --help` → `Supported regions: cn-north-1, ap-southeast-1` (the skill's default region is `cn-north-1`) |
| IAM action | Live CDN API 403 diagnostic: `is not authorized to perform: cdn:configuration:queryDomainList` |

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--page_size`, `--page_number`
  and the real server-side filters `--domain_name` / `--business_type` /
  `--domain_status` / `--service_area` / `--enterprise_project_id` /
  `--exact_match` / `--show_tags`; it never emits a parameter the API does not
  have.
- Paging uses `--page_size` + `--page_number` (advance until the collected count
  reaches the response `total`).
- Credentials for the SDK fallback are read from a fixed whitelist of env names
  via `os.environ.get(name)` — `os.environ` is never enumerated.
- The export file is generated on the local filesystem only; nothing is written
  back to the cloud.

## 2. Structure / specification validation

```bash
bash scripts/validate-skill.sh -s <skill-path>
```

Checks: SKILL.md + frontmatter (name matches directory, description with
triggers, no `version`), required sections, Reference Documents section, no
hardcoded AK/SK (SEC-001/SEC-002), no cross-Skill references, one-PR-one-skill,
file count / SKILL.md line / extension allowlist.

## 3. Offline unit tests (mocked hcloud, no credentials, no network)

Run from the skill directory (bundled runner, executor-friendly — the same
entrypoint used by templates/test-vars.json):

```bash
python3 scripts/run_unit_tests.py
```

Every branch of the script is exercised with a mocked `subprocess.run`:
write-intent guard (read passes / create / delete / update / enable / disable /
refresh / normalized variants / operation whitelist / filter+output value
exclusion / following-flag-still-scanned), command construction, the
skill-quality-cli wrapper (wrapped / bare override / report toggle), JSON
extraction and `domains` extraction, failure classification (missing AK/SK,
403, generic, `[USE_ERROR]` treated as a hard failure even at rc=0),
`page_number` paging (total / full page / empty), SDK fallback (missing env
credentials), normalization and table rendering, Markdown rendering (headers /
missing-field `-` fallback / header-only empty table / summary line / pipe
escaping), CSV/JSON rendering, atomic export (file written / header-only empty
file written / missing dir created / bad path leaves no file / default
filename), and all `main()` output and error paths.

## 4. Functional smoke (read-only)

```bash
hcloud configure list
python3 scripts/export_cdn_domains.py --region cn-north-1 --format table
python3 scripts/export_cdn_domains.py --region cn-north-1 --output /tmp/cdn_domains_cn-north-1.csv
python3 scripts/export_cdn_domains.py --region cn-north-1 --format json --output /tmp/cdn_domains_cn-north-1.json
python3 scripts/export_cdn_domains.py --region cn-north-1 --format markdown --output /tmp/cdn_domains_cn-north-1.md --summary
```

Expected: an aligned table / a generated `.csv` / `.json` / `.md` file
containing the `域名` column; an explicit
`当前区域（cn-north-1）无 CDN 加速域名` message plus a header-only (empty) file
on an empty region, exit code 0; an explicit IAM hint on 403
(`cdn:configuration:queryDomainList`).

## 5. Environment note

The development environment had the `hcloud` binary and an active credential
profile, so the KooCLI path was exercised live (read-only): the call reached the
CDN API and returned an explicit IAM authorization error for the current test
principal (`CDN.0004` / `cdn:configuration:queryDomainList`) — i.e. the command
shape and region (`cn-north-1`) are valid, and the failure is an
authorization gap on the test account, not a skill defect. The full offline
suite (mocked hcloud) passes without credentials.