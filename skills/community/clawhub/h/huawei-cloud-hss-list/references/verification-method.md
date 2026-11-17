# Verification Method

## Prerequisites

- AK/SK configured in the KooCLI profile (`hcloud configure set`), or
  `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY` (and `HUAWEI_PROJECT_ID` for the
  SDK fallback) environment variables set out-of-band.
- Test account has at least one HSS-protected server in the target region.
- IAM permission `hss:host:listHostStatus` granted (see `iam-policies.md`).
- Python 3.8+ and, for the SDK fallback path, `huaweicloudsdkhss`
  (`pip install huaweicloudsdkcore huaweicloudsdkhss`).

## Functional verification

```bash
# 1. Full-field table (default)
python3 scripts/list_hss.py --region cn-north-4

# 2. JSON output
python3 scripts/list_hss.py --region cn-north-4 --json

# 3. Names-only list
python3 scripts/list_hss.py --region cn-north-4 --names-only

# 4. Filters (all real server-side query parameters)
python3 scripts/list_hss.py --region cn-north-4 --agent-status online
python3 scripts/list_hss.py --region cn-north-4 --host-status ACTIVE
python3 scripts/list_hss.py --region cn-north-4 --protect-status opened --os-type Linux

# 5. Write-intent guard (must FAIL with an error, no command executes)
python3 scripts/list_hss.py --region cn-north-4 --host-name "create-host"
```

## Offline unit tests

```bash
cd skills/security/hss/huawei-cloud-hss-list
python3 -m unittest tests.test_list_hss -v   # expect: Ran 27 tests ... OK
```

## Environment-override knobs for testing without a live region

| Env var | Effect |
| ------- | ------ |
| `HSS_LIST_HCLOUD_BIN` | hcloud executable path (default `hcloud`) |
| `HSS_LIST_HCLOUD_ARGS` | extra args injected before the HSS operation |

## Known limitation on this test account

The sandbox account `gaoyunjiao` reports IAM `403 common.01010013` for
`hss:host:listHostStatus` in every region — the API is reachable (the error is
an authorization decision, not a connectivity/parameter failure). Functional
verification on a live account therefore requires granting the HSS read-only
action; the offline unit suite (27 cases, all passing) covers the script logic.