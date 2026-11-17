# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/database/rds/huawei-cloud-rds-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_instances_via_sdk` mock (no real SDK
  import, no network), plus a live regression test that constructs the real
  `ListInstancesRequest` when `huaweicloudsdkrds` is installed (skipped
  otherwise).
- Cases cover: write-intent guard, command construction (including "status is
  never sent to the server"), JSON extraction, failure classification (missing
  AK/SK / 403 / generic / `[USE_ERROR]` with rc=0), client-side status
  filtering (exact / case-insensitive / no-match), paging (total, full-page,
  empty), SDK fallback (success / unavailable), rendering, and all main()
  output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                  # profile check
hcloud RDS ListInstances --cli-region=cn-north-4 --limit=1             # API sanity
python3 scripts/list_rds.py --region cn-north-4                        # full flow
python3 scripts/list_rds.py --json | python3 -m json.tool >/dev/null   # JSON validity
python3 scripts/list_rds.py --names-only
python3 scripts/list_rds.py --status ACTIVE                            # client-side filter
python3 scripts/list_rds.py --datastore-type MySQL
```

Live verification against the real environment (2026-10-16):

- `hcloud RDS ListInstances --help` parameter list contains **no `--status`**
  parameter — passing `--status=ACTIVE` fails with
  `[USE_ERROR]Invalid parameter: status` **and exit code 0**.
- The `huaweicloudsdkrds` v3 `ListInstancesRequest` has no `status` attribute
  (`status=` raises TypeError); its real kwargs are `x_language / id / name /
  type / datastore_type / eps_id / vpc_id / subnet_id / offset / limit / tags /
  group_type`.
- Consequently `--status` is applied client-side (`filter_by_status`) after the
  full paged list is fetched; `--name` / `--datastore-type` / `--instance-id`
  remain real server-side query parameters.
- `rc=0 + [USE_ERROR]` output is recognized as an explicit parameter error
  (`hcloud 参数错误 ... --help` hint) instead of a JSON-parse failure.

## REST path provenance

`GET /v3/{project_id}/instances` comes from the official `huaweicloudsdkrds`
v3 client `_list_instances_http_info` `resource_path` metadata (the same path
the SDK fallback invokes through `RdsClient.list_instances`). No endpoint was
inferred from naming patterns.
