# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/compute/bms/huawei-cloud-bms-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_servers_via_sdk` mock (no real SDK
  import, no network), plus a live regression test that constructs the real
  `ListBareMetalServersRequest` when `huaweicloudsdkbms` is installed (skipped
  otherwise).
- Cases cover: write-intent guard (read passes / create / delete / reboot /
  rebuild / resize / reinstall / normalize variants / operation whitelist /
  status-value exemption), command construction (page-number offset, name +
  status forwarded, no write flags), JSON extraction, failure classification
  (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0), client-side
  server-id filtering (exact / case-insensitive / no-match), paging (count,
  full-page, empty), SDK fallback (success / unavailable), rendering, and all
  main() output modes.

## Live verification

CLI operation / parameter provenance (2026-10-19, KooCLI 7.3.12):

```bash
hcloud BMS ListBareMetalServers --cli-region=cn-north-4 --help
```

Confirmed parameters: `--cli-region` (required), `--project_id` (required
path), `--detail`, `--enterprise_project_id`, `--flavor`, `--limit` (default 25,
max 1000), `--name`, `--offset` (**page number, starts at 1**), `--reservation_id`,
`--status` (`ACTIVE` / `BUILD` / `ERROR` / `HARD_REBOOT` / `REBOOT` / `REBUILD` /
`SHUTOFF`), `--tags`. There is **no server-id parameter** — hence `--server-id`
is applied client-side.

SDK fallback live probe (real `huaweicloudsdkbms` v1, region `cn-north-4`):

```bash
python3 -c "..."  # BmsClient.list_bare_metal_servers(ListBareMetalServersRequest(limit=1))
```

The response object exposes `servers` (list of `ServerDetails`) and `count`
(total), confirming the response shape the script parses
(`servers` / `count`). The probe returned an empty list with `count == 0`
(no BMS in the region).

When credentials are available, the full flow can be exercised with:

```bash
hcloud configure list
hcloud BMS ListBareMetalServers --cli-region=cn-north-4 --limit=1
python3 scripts/list_bms.py --region cn-north-4
python3 scripts/list_bms.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_bms.py --names-only
python3 scripts/list_bms.py --status ACTIVE
python3 scripts/list_bms.py --server-id <uuid>
```

## REST path provenance

`GET /v1/{project_id}/baremetalservers/detail` comes from the official
`huaweicloudsdkbms` v1 client `_list_bare_metal_servers_http_info`
`resource_path` metadata (the same path the SDK fallback invokes through
`BmsClient.list_bare_metal_servers`). No endpoint was inferred from naming
patterns. The concrete KooCLI service/operation names (`BMS` /
`ListBareMetalServers`) were confirmed with `hcloud BMS --help` and
`hcloud BMS ListBareMetalServers --help`.
