# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| SDK `_http_info` (authoritative) | `huaweicloudsdkdws` v2 `dws_client.py` → `_list_clusters_http_info` → `"method": "GET"`, `"resource_path": "/v1.0/{project_id}/clusters"` |
| hcloud service catalog (authoritative) | `DWS.ListClusters`: `method=GET`, `path=/v1.0/{{project_id}}/clusters`, `read_only=true`, `optional_params=[enterprise_project_id]`, `supports_limit=false` |

Consequences encoded in the script:

- `build_command()` emits only `--cli-region` and (optionally)
  `--enterprise_project_id`; it never emits `--name` / `--status` / `--id` /
  `--limit` / `--offset` because the API has no such parameters.
- Name / status / id filtering and limit / offset pagination are implemented as
  **client-side** helpers (`filter_clusters`, `paginate`).
- The SDK fallback constructs `ListClustersRequest(enterprise_project_id=...)`
  exactly; a unit test asserts that unknown kwargs such as `limit=` / `status=`
  raise `TypeError`.

## 2. Structure / specification validation

```bash
bash <skills-dir>/huawei-cloud-skill-creator/scripts/validate-skill.sh -s <skill-path>
```

Checks: SKILL.md + frontmatter (name matches directory, description with
triggers, no `version`), required sections, Reference Documents section, no
hardcoded AK/SK (SEC-001/SEC-002), no cross-Skill references, one-PR-one-skill,
file count / SKILL.md line / extension allowlist.

## 3. Offline unit tests (mocked hcloud, no credentials, no network)

```bash
python3 -m unittest discover -s tests -v
```

Every branch of `list_dws.py` is exercised with a mocked `subprocess.run`:
write-intent guard, command construction, JSON extraction, failure
classification (`[USE_ERROR]` treated as a hard failure even at rc=0),
client-side filters, client-side pagination, SDK fallback (env credentials,
missing credentials, alternative prefixes, real request signature), table /
JSON / names rendering, and all `main()` output and error paths. The SDK-specific
tests run when `huaweicloudsdkdws` is installed and skip otherwise.

## 4. Functional smoke (optional, read-only)

With a working hcloud profile:

```bash
hcloud configure list
python3 scripts/list_dws.py --region cn-north-4
python3 scripts/list_dws.py --names-only
python3 scripts/list_dws.py --json --limit 1
```

Expected: a table (or JSON / name list) of clusters; an explicit
`当前区域（cn-north-4）无 DWS 集群` message on an empty region; an explicit
IAM hint on 403.