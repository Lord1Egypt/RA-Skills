# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| hcloud service catalog (authoritative) | `hcloud DCS ListInstances --help`: `method=GET`; params `--cli-region` (required), `--project_id` (required, path), `--capacity`, `--include_delete`, `--include_failure`, `--instance_id`, `--ip`, `--limit` (integer, 1~1000, default 10 per page), `--name`, `--name_equal`, `--offset` (integer ≥ 0), `--status`, `--tags` — all real server-side query parameters |
| SDK `_http_info` (authoritative) | `huaweicloudsdkdcs` v2 `dcs_client.py` → `_list_instances_http_info` → `"method": "GET"`, `"resource_path": "/v2/{project_id}/instances"`; `ListInstancesRequest` kwargs: `instance_id / include_failure / include_delete / name / offset / limit / status / name_equal / tags / ip` |
| SDK response model | `ListInstancesResponse` → `instances: list[InstanceListInfo]`, `instance_num: int` (drives the paging stop condition); `DcsRegion.value_of("cn-north-4")` → endpoint `https://dcs.cn-north-4.myhuaweicloud.com` |

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--limit`, `--offset` and the
  real server-side filters `--name` / `--instance_id` / `--ip` / `--status` /
  `--tags`; it never emits a parameter the API does not have.
- Paging uses `--limit` (clamped to 1~1000, default 100) + `--offset`, and stops
  when `instance_num` is reached (or a short/empty page arrives).
- Credentials for the SDK fallback are read from a fixed whitelist of env names
  via `os.environ.get(name)` — `os.environ` is never enumerated.

## 2. Structure / specification validation

```bash
bash scripts/validate-skill.sh -s <skill-path>
```

Checks: SKILL.md + frontmatter (name matches directory, description with
triggers, no `version`), required sections, Reference Documents section, no
hardcoded AK/SK (SEC-001/SEC-002), no cross-Skill references, one-PR-one-skill,
file count / SKILL.md line / extension allowlist.

## 3. Offline unit tests (mocked hcloud, no credentials, no network)

```bash
python3 -m unittest discover -s tests -v
```

Every branch of the script is exercised with a mocked `subprocess.run`:
write-intent guard (read passes / create / delete / resize / restart / flush /
backup / freeze / normalized variants / operation whitelist / filter+output
value exclusion), command construction, the skill-quality-cli wrapper (wrapped /
bare override / report toggle), JSON extraction, failure classification
(`[USE_ERROR]` treated as a hard failure even at rc=0), offset paging
(`instance_num`-driven / full-page fallback / empty), SDK fallback (missing env
credentials, missing project id), normalization and table rendering, Markdown
rendering (headers / missing-field `-` fallback / summary line / pipe escaping),
atomic export (file written / missing dir created / bad path leaves no file /
default filename), and all `main()` output and error paths.

## 4. Functional smoke (optional, read-only)

With a working hcloud profile:

```bash
hcloud configure list
python3 scripts/list_dcs_export_markdown.py --region cn-north-4 --format table
python3 scripts/list_dcs_export_markdown.py --region cn-north-4 --format json | python3 -m json.tool >/dev/null
python3 scripts/list_dcs_export_markdown.py --region cn-north-4 --output /tmp/dcs.md --summary
```

Expected: an aligned table / JSON array / a generated `.md` report; an explicit
`当前区域（cn-north-4）无 DCS 实例，未生成 Markdown 文件` message on an empty
region; an explicit IAM hint on 403.