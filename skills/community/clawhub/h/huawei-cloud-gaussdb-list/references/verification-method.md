# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| hcloud service catalog (authoritative) | `hcloud GaussDB ListGaussMySqlInstances --help` (live run, 2026-11-09): `method=GET`; params `--cli-region` (required), `--project_id` (required, path), `--X-Language`, `--datastore_type`, `--id`, `--limit` (integer, 1~100, default 100), `--name`, `--offset` (integer ≥ 0), `--private_ip`, `--proxy_ip`, `--readonly_private_ip`, `--subnet_id`, `--tags`, `--type`, `--vpc_id` — all real parameters |
| SDK `_http_info` (authoritative) | `huaweicloudsdkgaussdb` v3 `gaussdb_client.py` → `_list_gauss_my_sql_instances_http_info` → `"method": "GET"`, `"resource_path": "/v3/{project_id}/instances"`; `ListGaussMySqlInstancesRequest` kwargs: `x_language / id / name / type / datastore_type / vpc_id / subnet_id / private_ip / readonly_private_ip / proxy_ip / offset / limit / tags` (verified: unknown kwargs raise `TypeError`) |
| SDK response model | `ListGaussMySqlInstancesResponse` → `instances: list[MysqlInstanceListInfo]`, `total_count: int` (drives the paging stop condition); `MysqlInstanceListInfo` carries `id / name / status / private_ips / public_ips / port / type / region / datastore / created / updated / flavor_ref / flavor_info / volume / ...`; `GaussDBRegion.value_of("cn-north-4")` → endpoint `https://gaussdb.cn-north-4.myhuaweicloud.com` |

**Note**: `hcloud GaussDB ListInstances` does **not** exist — the correct
operation is `ListGaussMySqlInstances`. This was verified against the live
service catalog (`hcloud GaussDB --help` lists `ListGaussMySqlInstances`).

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--limit`, `--offset` and the
  real parameters `--project_id` / `--name` / `--id` / `--datastore_type` /
  `--type` / `--vpc_id` / `--subnet_id`; it never emits a parameter the API
  does not have (in particular there is **no `--status`**).
- Paging uses `--limit` (clamped to 1~100) + `--offset`, and stops when
  `total_count` is reached (or a short/empty page arrives).
- The SDK fallback constructs `ListGaussMySqlInstancesRequest(limit=…,
  offset=…, name=…, id=…, datastore_type=…, type=…, vpc_id=…, subnet_id=…)`
  exactly.
- Credentials for the SDK fallback are read from a fixed whitelist of env
  names via `os.environ.get(name)` — `os.environ` is never enumerated.

## 2. Structure / specification validation

```bash
bash <skills-dir>/huawei-cloud-skill-creator/scripts/validate-skill.sh -s <skill-path>
```

Checks: SKILL.md + frontmatter (name matches directory, description with
triggers, no `version`), required sections, Reference Documents section, no
hardcoded AK/SK (SEC-001/SEC-002), no cross-Skill references, one-PR-one-skill,
file count / SKILL.md line / extension allowlist.

## 3. Functional smoke (read-only)

With a working hcloud profile:

```bash
hcloud configure list
python3 scripts/list_gaussdb.py --region cn-north-4
python3 scripts/list_gaussdb.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_gaussdb.py --name gauss --status ACTIVE
```

Expected: a table (or raw JSON array); an explicit
`当前区域（cn-north-4）无 GaussDB 实例` message on an empty region; an explicit
IAM hint on 403. The same read-only cases are recorded in
`templates/test-vars.json` for reuse by the verification run.