# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/database/rds/huawei-cloud-rds-export-markdown
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_instances_via_sdk` mock (no real SDK
  import, no network), plus a live regression test that constructs the real
  `ListInstancesRequest` when `huaweicloudsdkrds` is installed (skipped
  otherwise).
- Markdown rendering and file writing run against a temporary directory.

Coverage: write-intent guard (read passes / create / delete / resize / restart /
stop / restore / normalized separators / operation whitelist / read-only value
scrubbing), command construction (including "status is never sent to the
server" and `--cli-project-id` mapping), JSON extraction, failure classification
(missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0), client-side status
filtering (exact / case-insensitive / no-match), paging (total / full-page /
empty), SDK fallback (success / unavailable / env credentials), normalization,
Markdown rendering (title / header / rows / empty-result note / pipe & newline
escaping), atomic file writing (missing dirs / bad path), and all `main()`
output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                  # profile check
hcloud RDS ListInstances --cli-region=cn-north-4 --limit=1             # API sanity
python3 scripts/list_rds_export_markdown.py --region cn-north-4                     # full flow
cat rds_instances.md                                                   # inspect the table
python3 scripts/list_rds_export_markdown.py --region cn-north-4 --output /tmp/rds.md --stdout
python3 scripts/list_rds_export_markdown.py --status ACTIVE                         # client-side filter
```

## Endpoint provenance

`GET /v3/{project_id}/instances` comes from the official `huaweicloudsdkrds`
v3 client `_list_instances_http_info` `resource_path` metadata (the same path
the SDK fallback invokes through `RdsClient.list_instances`). No endpoint was
inferred from naming patterns.

- `ListInstancesRequest` real kwargs: `x_language / id / name / type /
  datastore_type / eps_id / vpc_id / subnet_id / offset / limit / tags /
  group_type` — there is **no `status`** attribute and **no `project_id`**
  attribute (project id is a path parameter resolved by the client).
- Therefore the CLI path forwards `--name` / `--datastore_type` / `--id`
  server-side and maps `--project_id` to the KooCLI global `--cli-project-id`;
  `--status` is applied client-side after the full paged list is fetched.
- `rc=0 + [USE_ERROR]` output is recognized as an explicit parameter error
  (`hcloud 参数错误 ... --help` hint) instead of a JSON-parse failure.