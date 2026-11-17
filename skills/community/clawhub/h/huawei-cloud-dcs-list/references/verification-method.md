# Verification Method

## 1. API provenance (no guessing)

The one REST endpoint this skill calls was taken from official sources only:

| Source | Evidence |
| -------- | --------- |
| hcloud service catalog (authoritative) | `hcloud DCS ListInstances --help` (live run, 2026-10-21): `method=GET`; params `--cli-region` (required), `--project_id` (required, path), `--capacity`, `--include_delete`, `--include_failure`, `--instance_id`, `--ip`, `--limit` (integer, 1~1000, default 10 per page), `--name`, `--name_equal`, `--offset` (integer ≥ 0), `--status`, `--tags` — all real server-side query parameters |
| SDK `_http_info` (authoritative) | `huaweicloudsdkdcs` v2 `dcs_client.py` → `_list_instances_http_info` → `"method": "GET"`, `"resource_path": "/v2/{project_id}/instances"`; `ListInstancesRequest` kwargs: `instance_id / include_failure / include_delete / name / offset / limit / status / name_equal / tags / ip` (verified: unknown kwargs raise `TypeError`) |
| SDK response model | `ListInstancesResponse` → `instances: list[InstanceListInfo]`, `instance_num: int` (drives the paging stop condition); `DcsRegion.value_of("cn-north-4")` → endpoint `https://dcs.cn-north-4.myhuaweicloud.com` |

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--limit`, `--offset` and the
  real server-side filters `--name` / `--instance_id` / `--ip` / `--status` /
  `--tags`; it never emits a parameter the API does not have.
- Paging uses `--limit` (clamped to 1~1000, default 100 instead of KooCLI's
  10-per-page default) + `--offset`, and stops when `instance_num` is
  reached (or a short/empty page arrives).
- The SDK fallback constructs `ListInstancesRequest(limit=…, offset=…,
  name=…, instance_id=…, ip=…, status=…, tags=…)` exactly; a unit test
  asserts that an unknown kwarg raises `TypeError`.
- Credentials for the SDK fallback are read from a fixed whitelist of env
  names via `os.environ.get(name)` — `os.environ` is never enumerated
  (skillspector E2 hard-fails on bulk env access).

## 2. Structure / specification validation

```bash
bash <skills-dir>/huawei-cloud-skill-creator/scripts/validate-skill.sh -s <skill-path>
```

Checks: SKILL.md + frontmatter (name matches directory, description with
triggers, no `version`), required sections, Reference Documents section, no
hardcoded AK/SK (SEC-001/SEC-002), no cross-Skill references, one-PR-one-skill,
file count / SKILL.md line / extension allowlist.

## 3. Skillspector security gate

```bash
skillspector scan <skill-path> --no-llm --format json
```

Required: **0 high-severity issues** (the repo gate from issues #22 / #23).
The two historical E2 findings (`os.environ.items()` env harvesting) are
avoided by design: scripts and tests only read whitelisted env names via
`os.environ.get(name)`, and the test credential cleanup blanks exactly those
names instead of copying the environment.

## 4. Offline unit tests (mocked hcloud, no credentials, no network)

```bash
python3 -m unittest discover -s tests -v
```

Every branch of `list_dcs.py` is exercised with a mocked `subprocess.run`:
write-intent guard, command construction, JSON extraction, failure
classification (`[USE_ERROR]` treated as a hard failure even at rc=0),
offset paging (`instance_num`-driven / full-page fallback / empty), SDK
fallback (env credentials, alternative prefixes, missing credentials,
missing project id, pagination, filters, real request signature), table /
JSON / names rendering, Markdown rendering and `--md-output` writing, and all
`main()` output and error paths. The SDK-specific tests run when
`huaweicloudsdkdcs` is installed and skip otherwise.

## 5. Markdown output verification

The Markdown contract is checked offline (no credentials, no network) by
`TestMarkdownOutput` / `TestResolveMode` / `TestMarkdownFileHelper`:

| Check | How |
| ----- | --- |
| Header is the export-markdown ten columns in order, separator immediately after | exact line equality against the literal `名称/ID/引擎/版本/容量/规格/状态/连接地址/端口/可用区` header and ten `---` cells |
| Column order / value mapping | `normalized_row` asserted cell by cell (name → id → engine → version → capacity → spec → status → ip → port → az) |
| Missing fields render `-` | instance with only `instance_id` → nine `-` plus the id |
| Escaping | name containing a pipe character → backslash-escaped pipe; `RUN\nNING` → `RUN NING`; `x\r\ny` → `x  y` |
| `--format md` == `--md` | both runs compared as whole stdout strings |
| Filters / paging still apply | `--md --status RUNNING --page-size 10` → `--status=RUNNING --limit=10` in the hcloud argv |
| Empty list | hint text only, no table header in stdout, target file absent |
| `--md-output` content equality | file text asserted equal to captured stdout, `[已写入]` on stderr |
| Atomic write failure | `os.replace` forced to `OSError` → exit 1, no target file, no leftover `*.tmp` |
| `--md-output` outside md mode | exit 1 with an explicit hint |
| Write-intent guard in md mode | `--md --name delete-me` → exit 1; `--md-output .../dcs-backup-restore.md` allowed |
| Legacy outputs unchanged | default / `--table` / `--json` stdout compared byte-for-byte |

Manual end-to-end check with a stub `hcloud` on `PATH`:

```bash
DCS_LIST_HCLOUD_BIN=/path/to/stub-hcloud python3 scripts/list_dcs.py --md
DCS_LIST_HCLOUD_BIN=/path/to/stub-hcloud python3 scripts/list_dcs.py \
  --md --md-output ./dcs_instances.md
cat ./dcs_instances.md   # identical to the table printed above
```

Expected: a ten-column Markdown table (rows for each instance, `-` for fields
the stub omits); the file content is identical to the printed table; an empty
stub response prints `当前区域（cn-north-4）无 DCS 实例。` and creates no file.

## 6. Functional smoke (optional, read-only)

With a working hcloud profile:

```bash
hcloud configure list
python3 scripts/list_dcs.py --region cn-north-4
python3 scripts/list_dcs.py --table
python3 scripts/list_dcs.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_dcs.py --name cache --names-only
```

Expected: an instance-name list (or table / JSON); an explicit
`当前区域（cn-north-4）无 DCS 实例` message on an empty region; an explicit
IAM hint on 403.
