# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/billing/bss/huawei-cloud-voucher-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic. 69 tests, all passing.
- The SDK fallback is tested via a `list_coupons_via_sdk` mock plus a live
  regression test that constructs the real `ListSubCustomerCouponsRequest` when
  `huaweicloudsdkbss` is installed (skipped otherwise); it also asserts the
  builder is wired with `GlobalCredentials` + `with_endpoints`.
- Cases cover: write-intent guard (read passes; create / reclaim / update /
  transfer / freeze blocked; `reclaim*` matched only as specific operation
  names so the read-only status label `reclaimed` is not blocked), `--status`
  parsing, command construction (including "no name parameter is ever sent to
  the server"), JSON extraction, failure classification (missing AK/SK / 403 /
  generic / `[USE_ERROR]` with rc=0), server-side status forwarding,
  client-side name / status filtering, paging (count, full-page, empty), SDK
  fallback (success / unavailable), rendering, and all main() output modes.

## Live verification (performed 2026-10-19)

hcloud (KooCLI) is not installable in the build environment
(`cn-north-4-res.hcccloud.com` unreachable), so the **SDK path was verified
live** against the real BSS global endpoint with the session credentials
(read-only):

```bash
python3 scripts/list_voucher.py --region cn-north-1 --names-only
# → Region cn-north-1 的 BSS 代金券名称列表（共 0 张）：  (exit 0)

python3 scripts/list_voucher.py --region cn-north-1 --json
# → []  (exit 0)

python3 scripts/list_voucher.py --region cn-north-1 --status available --names-only
# → exit 0

python3 scripts/list_voucher.py --operation ReclaimPartnerCoupons
# → [错误] 检测到写操作意图 ... 已被守卫拦截  (exit 1)
```

This confirms: the account has `bss:coupon:list`, the SDK authenticates via
`GlobalCredentials` against `https://bss.myhuaweicloud.com`, and all three
output modes plus the write-intent guard behave as designed. The account holds
0 coupons in `cn-north-1`, so the empty-list path is exercised live.

### CLI parameter caveat

The KooCLI parameter names are derived from the coupon-list OpenAPI query
parameters (`coupon_id` / `status` / `offset` / `limit`, snake_case). Because
hcloud could not be installed here, confirm the exact parameter list with
`hcloud BSS ListSubCustomerCoupons --help` in an environment where KooCLI is
available before production use. The script isolates this in `build_command()`,
so any final naming adjustment is a one-line change; the SDK fallback and all
offline tests are unaffected.

## REST path provenance

`GET /v2/promotions/benefits/coupons` comes from the official
`huaweicloudsdkbss` v2 client `_list_sub_customer_coupons_http_info`
`resource_path` metadata (the same path the SDK fallback invokes through
`BssClient.list_sub_customer_coupons`). No endpoint was inferred from naming
patterns.

## Operation name note

The read-only coupon-list operation is `ListSubCustomerCoupons`. The issue
shorthand "ListCoupons" is accepted as an alias and normalised to
`ListSubCustomerCoupons` (there is no separate `ListCoupons` in the official
BSS v2 SDK; the voucher list corresponds to this operation).
