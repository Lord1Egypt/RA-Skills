# Acceptance Criteria

| # | Criterion | How to verify |
| -- | --------- | ------------- |
| 1 | Can list HSS protected hosts in the target region | `python3 scripts/list_hss.py --region cn-north-4` prints the host table |
| 2 | Output includes host name / IP / protection status / Agent status / edition | Table columns contain `host_name`, `private_ip`/`public_ip`, `protect_status`, `agent_status`, `version` |
| 3 | `--json` returns the raw full-field response | `--json` prints a JSON array of host records |
| 4 | Support `--region` override | `--region cn-south-1` queries that region |
| 5 | Read-only (no create/delete/update) | Write intents (`create`, `ChangeEvent`, `install_agent`, ...) are rejected with an error |
| 6 | Handles IAM 403 explicitly | Missing `hss:host:listHostStatus` gives an explicit 「无权限访问主机安全服务（HSS）」 hint |
| 7 | Empty region handled | Prints 「当前区域（X）无已接入 HSS 的服务器」 |
| 8 | 27 offline unit tests pass | `python3 -m unittest tests.test_list_hss` → OK |

## Status value reference

| Field | Values |
| ----- | ------ |
| `agent_status` | `online`, `offline`, `installing`, `install_failed`, `not_installed`, `not_online` (query only) |
| `host_status` | `ACTIVE`, `SHUTOFF`, `BUILDING`, `ERROR` |
| `protect_status` | `opened`, `closed`, `protection_exception` |
| `version` | `hss.version.null`, `hss.version.basic`, `hss.version.advanced`, `hss.version.enterprise`, `hss.version.premium`, `hss.version.wtp`, `hss.version.container.enterprise` |
| `os_type` | `Linux`, `Windows` |