# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| hcloud service catalog (authoritative) | `hcloud VPC ListVpcs --help`: `method=GET`; params `--cli-region` (required), `--limit` (integer, 0~2000), `--marker`, `--id`, `--enterprise_project_id` — all real server-side query parameters |
| SDK `_http_info` (authoritative) | `huaweicloudsdkvpc` v2 `vpc_client.py` → `_list_vpcs_http_info` → `"method": "GET"`, `"resource_path": "/v1/{project_id}/vpcs"`; `ListVpcsRequest` kwargs: `limit / marker / id / enterprise_project_id` |
| SDK response model | `ListVpcsResponse` → `vpcs: list[Vpc]`, `page_info.next_marker` (drives paging); `VpcRegion.value_of("cn-north-4")` → endpoint `https://vpc.cn-north-4.myhuaweicloud.com` |

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--limit`, `--marker` and the
  real server-side filters `--id` / `--enterprise_project_id`; it never emits a
  parameter the API does not have.
- Paging uses `--limit` + `--marker` (the marker is the `next_marker` from the
  response `page_info`).
- Credentials for the SDK fallback are read from a fixed whitelist of env names
  via `os.environ.get(name)` — `os.environ` is never enumerated.
- The Markdown report is generated on the local filesystem only; nothing is
  written back to the cloud.

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
write-intent guard (read passes / create / delete / update / associate /
release / normalized variants / operation whitelist / filter+output value
exclusion / following-flag-still-scanned), command construction, the
skill-quality-cli wrapper (wrapped / bare override / report toggle), JSON
extraction and `vpcs` extraction, failure classification (missing AK/SK,
403, generic, `[USE_ERROR]` treated as a hard failure even at rc=0), marker
paging (`next_marker` / full-page fallback / empty), SDK fallback (missing env
credentials, missing project id), normalization and table rendering, Markdown
rendering (headers / missing-field `-` fallback / header-only empty table /
summary line / pipe escaping), atomic export (file written / empty table file
written / missing dir created / bad path leaves no file / default filename), and
all `main()` output and error paths.

## 4. Functional smoke (read-only)

```bash
hcloud configure list
python3 scripts/export_vpc_markdown.py --region cn-north-4 --format table
python3 scripts/export_vpc_markdown.py --region cn-north-4 --format json | python3 -m json.tool >/dev/null
python3 scripts/export_vpc_markdown.py --region cn-north-4 --output /tmp/vpc_list_cn-north-4.md --summary
```

Expected: an aligned table / JSON array / a generated `.md` report containing
the `VPC 名称` column; an explicit `当前区域（cn-north-4）无虚拟私有云（VPC）`
message plus a header-only (empty) table on an empty region, exit code 0; an
explicit IAM hint on 403.