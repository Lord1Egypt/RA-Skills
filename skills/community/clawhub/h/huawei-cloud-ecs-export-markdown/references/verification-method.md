# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| hcloud service catalog (authoritative) | `skill-quality-cli run --skill-name huawei-cloud-skill-coding -- hcloud ECS ListServersDetails --help`: `Method: GET`; params `--cli-region` (required), `--project_id` (required, path), `--limit` (integer, 1~1000), `--offset` (integer ≥ 0), `--status` (ACTIVE / BUILD / ERROR / HARD_REBOOT / MIGRATING / REBOOT / REBUILD / RESIZE / REVERT_RESIZE / SHUTOFF / VERIFY_RESIZE), `--name` (fuzzy), `--flavor`, `--ip`, `--ip_eq`, `--server_id`, `--tags`, `--not-tags`, `--enterprise_project_id`, `--marker`, `--reservation_id` — all real server-side query parameters |
| SDK `_http_info` (authoritative) | `huaweicloudsdkecs` v2 `ecs_client.py` → `_list_servers_details_http_info` → `"method": "GET"`, `"resource_path": "/v1/{project_id}/cloudservers/detail"`; `ListServersDetailsRequest.openapi_types`: `enterprise_project_id / flavor / ip / ip_eq / limit / marker / name / not_tags / offset / reservation_id / server_id / status / tags` |
| SDK response model | `ListServersDetailsResponse` → `servers: list[ServerDetail]`, `count: int` (drives the paging stop condition); `EcsRegion.value_of("cn-north-4")` → endpoint `https://ecs.cn-north-4.myhuaweicloud.com` |

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--limit`, `--offset` and the
  real server-side filters `--status` / `--name`; it never emits a parameter the
  API does not have and never emits a mutating flag.
- Paging uses `--limit` (clamped to 1~1000, default 100) + `--offset`, and stops
  when `count` is reached (or a short/empty page arrives).
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
write-intent guard (read passes / create / delete / update / reboot / resize /
attach / detach / normalized variants / operation whitelist / filter+output
value exclusion / following-flag-still-scanned), command construction, the
skill-quality-cli wrapper (wrapped / bare override / report toggle / missing
CLI), JSON extraction, failure classification (`[USE_ERROR]` treated as a hard
failure even at rc=0), offset paging (`count`-driven / full-page fallback /
empty), SDK fallback (missing env credentials / unavailable), normalization and
table rendering, Markdown rendering (headers / separator / data rows /
missing-field `-` fallback / region+filter metadata / summary line / pipe and
newline escaping), atomic export (file written / missing dir created / bad path
leaves no file / rename failure leaves no temp file / default filename), and all
`main()` output and error paths.

## 4. Functional smoke (optional, read-only)

With a working hcloud profile:

```bash
hcloud configure list
python3 scripts/list_ecs_export_markdown.py --region cn-north-4 --format table
python3 scripts/list_ecs_export_markdown.py --region cn-north-4 --format json | python3 -m json.tool >/dev/null
python3 scripts/list_ecs_export_markdown.py --region cn-north-4 --output /tmp/ecs.md --summary
```

Expected: an aligned table / JSON array / a generated `.md` report; an explicit
`当前区域（cn-north-4）无 ECS 实例，未生成 Markdown 文件` message on an empty
region; an explicit IAM hint on 403. All calls are read-only (GET) and create no
cloud resources.