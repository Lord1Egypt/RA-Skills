---
name: huawei-cloud-voucher-claim
description: |
  1. Claim (领取 / 划拨) an amount of a Huawei Cloud BSS (费用中心) voucher /
     coupon for an enterprise sub-account through the official BSS API
     POST /v2/enterprises/multi-accounts/transfer-coupon (operation
     ClaimEnterpriseMultiAccountCoupon) — the KooCLI path is attempted first
     when the local KooCLI build exposes a BSS service, with an automatic
     fallback to the official huaweicloudsdkbss v2 SDK otherwise.
  2. After a successful claim the skill runs the read-only coupon-list API
     (ListSubCustomerCoupons — GET /v2/promotions/benefits/coupons) and prints
     the resulting coupon inventory: 券ID / 券码 / 面额 / 余额 / 有效期 / 状态
     (table, --json, or --no-list to skip).
  3. Zero-config operation: the invocation path is chosen automatically (CLI
     first, SDK fallback); credentials are loaded only from the hcloud profile
     or the standard Huawei Cloud environment variables.
  4. Idempotent: the API's trans_id (交易序列号) is derived deterministically
     from (customer, coupon, amount) so a retry reuses it and the server rejects
     the duplicate submission (CBC.99007009); a local ledger additionally skips
     a retry inside the idempotency window. --force overrides,
     --no-idempotency disables.
  5. Safe by default for a money-moving, irreversible operation: a live claim
     requires the explicit --confirm flag (otherwise the run only previews the
     request and exits 2); --dry-run previews the exact request.
  6. Graded errors: ConfigError (missing/invalid parameters or credentials) /
     AuthError (401/403 / insufficient IAM permission) / ApiError (unexpected
     API, network, or duplicate trans_id), each with an actionable hint.
  7. Write-intent guard: only the claim operation ever executes; reclaim /
     transfer-away / freeze / cancel / individually-issued-coupon mutation
     operations are rejected — this skill claims coupons only.
  8. Offline unit tests (mocked hcloud subprocess) cover validation, command
     construction, idempotency, error grading, SDK fallback and all CLI modes.
  9. Triggers include: "领取代金券", "代金券领取", "领取优惠券", "企业子账号领券",
     "划拨代金券", "claim voucher", "claim coupon", "enterprise coupon claim",
     "华为云代金券领取", "BSS coupon claim".
tags: [huawei-cloud, bss, billing, write, koo-cli]
---

# Huawei Cloud BSS Voucher Claim (代金券领取 / 企业多账号划拨)

## Overview

Claim (领取) an amount of a Huawei Cloud BSS voucher / coupon for an enterprise
sub-account through the official BSS enterprise multi-account coupon-transfer
operation (`ClaimEnterpriseMultiAccountCoupon`, service `BSS`) on the official
API, `POST /v2/enterprises/multi-accounts/transfer-coupon`, verified in the
`huaweicloudsdkbss` v2 client
`_claim_enterprise_multi_account_coupon_http_info` metadata. An enterprise
master account transfers (拨款) an amount of one of its coupons to one of its own
enterprise sub-accounts — the sub-account thereby claims the coupon. The skill
tries the KooCLI path first when the local KooCLI build exposes a BSS service;
because the current KooCLI build reports `Unsupported service: BSS`, the skill
runs the official `huaweicloudsdkbss` v2 SDK
(`BssClient.claim_enterprise_multi_account_coupon`).

After a successful claim the skill runs the read-only coupon-list operation
(`ListSubCustomerCoupons` / `GET /v2/promotions/benefits/coupons`) and prints the
resulting coupon inventory — 券ID / 券码 / 面额 / 余额 / 有效期 / 状态.

Architecture:

```text
agent → python3 scripts/claim_voucher.py --customer-id <c> --coupon-id <cp> --amount <v> --confirm
      → claim path: KooCLI claim operation (service BSS) when available,
                    else huaweicloudsdkbss v2 SDK
      → Huawei Cloud BSS OpenAPI (global endpoint) → sub_coupon_id
      → idempotency ledger (per customer/coupon/amount)
      → read-only ListSubCustomerCoupons (post-claim inventory)
      → human table (券ID/券码/面额/余额/有效期/状态) / --json
```

Key properties:

- **Write by design, safe by default** — a claim transfers money / benefit to
  the target sub-account and is normally irreversible. A live claim requires the
  explicit `--confirm` flag; without it the run stops with a clear message and
  only prints the request preview. `--dry-run` previews the exact request
  (including the derived `trans_id`) without claiming anything.
- **Idempotent / no double-claim** — the API's `trans_id` (交易序列号) is derived
  deterministically from `(customer_id, coupon_id, amount)` when not supplied, so
  a retry reuses the same serial number and the server rejects a duplicate
  submission (`CBC.99007009`). A local ledger records the (customer, coupon,
  amount) natural key so a retry inside the window does not even call the API.
- **Post-claim inventory** — after a successful claim the script queries the
  read-only coupon list; `coupon_id` is filtered server-side and `customer_id`
  client-side (the list API has no `customer_id` parameter).
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI build does not expose a BSS service (current KooCLI) or the KooCLI
  binary is absent, the script falls back to `huaweicloudsdkbss` v2. BSS is a
  *global* service, so the SDK path uses `GlobalCredentials` + `with_endpoints`
  (`https://bss.myhuaweicloud.com`). Credentials are resolved by `config.py`
  (KooCLI profile for the CLI path; standard environment variables for the SDK
  path) — never handled by the skill.
- **Offline-testable** — validation, command construction, idempotency, error
  grading, SDK fallback and all output modes are covered by unit tests that mock
  the KooCLI subprocess.

Out of scope: coupon queries beyond the post-claim inventory (use the read-only
sibling skill), coupon reclaim / return / freeze / cancel, and partner issuance
to resold sub-customers (a different BSS operation).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkbss` to enable the
   SDK fallback path.
2. **Credential profile** — configure credentials out-of-band (hcloud configure
   in your terminal, or the standard credential environment variables). Never
   paste AK/SK into chat; `config.py` reads the hcloud profile / environment and
   never echoes or stores secrets.
3. **IAM write permission** — the claim action plus the read-only coupon-list
   action (least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md)). The calling
   identity must be the **enterprise master account** of the target sub-account.
4. **A transferable coupon (`coupon_id`)** — only Huawei-issued coupons
   (测试类/商务类/活动类) support transfer; obtain it from the enterprise master
   account's transferable-coupon list.
5. **Python 3.8+** (standard library only — argparse / json / subprocess /
   decimal / hashlib).
6. **Outbound HTTPS** access to `bss.myhuaweicloud.com`.
7. **Region** — BSS is a global service; use `cn-north-1` (the default here).

## Workflow

1. **Confirm the danger** — claiming vouchers is a money-moving, irreversible
   change. Obtain explicit user confirmation (the caller sets `--confirm`); the
   skill refuses to claim without it.
2. **Resolve the coupon** — determine the enterprise sub-account `customer_id`
   and the transferable `coupon_id` on the enterprise master account.
3. **Preview** — run with `--dry-run` (or without `--confirm`) to inspect the
   exact request and the derived `trans_id`; nothing is claimed.
4. **Claim** — re-run with `--confirm` to transfer the amount; the resulting
   `sub_coupon_id` is reported and the natural key is recorded in the
   idempotency ledger.
5. **Read the inventory** — the skill then queries the read-only coupon list and
   prints 券ID / 券码 / 面额 / 余额 / 有效期 / 状态 for the claimed coupon and
   sub-account.
6. **Retry safely** — re-running the same command is skipped inside the
   idempotency window; the derived `trans_id` also protects against a duplicate
   server-side submission.

## Core Commands

```bash
# Preview the claim request (no claim; also the default without --confirm):
python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \
  --amount 100.00 --dry-run

# Claim for a sub-account (requires explicit confirmation), then print the
# post-claim coupon inventory:
python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \
  --amount 100.00 --confirm

# Claim with an explicit transaction serial number (防重复提交):
python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \
  --amount 50.00 --trans-id 20261028001 --confirm

# Claim only, without the post-claim inventory query:
python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \
  --amount 100.00 --confirm --no-list

# Machine-readable result:
python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \
  --amount 100.00 --confirm --json
```

Equivalent SDK call (the script's fallback path wraps exactly this REST request):

```python
# POST /v2/enterprises/multi-accounts/transfer-coupon  (service BSS)
from huaweicloudsdkbss.v2 import (
    BssClient,
    ClaimEnterpriseMultiAccountCouponRequest,
    TransferEnterpriseMultiAccountCouponReq,
)
body = TransferEnterpriseMultiAccountCouponReq(
    customer_id="CUST001", coupon_id="CP001", amount="100.00",
    trans_id="20261028001")
resp = client.claim_enterprise_multi_account_coupon(
    ClaimEnterpriseMultiAccountCouponRequest(body=body))
# resp.sub_coupon_id  ->  the resulting sub-coupon id
```

Post-claim inventory (read-only, wrapped by the script): the coupon-list
operation (`ListSubCustomerCoupons`, `GET /v2/promotions/benefits/coupons`),
filtered by `coupon_id` server-side and `customer_id` client-side.

> On a KooCLI build that exposes a BSS service, the script attempts the
> corresponding claim operation first (service BSS, operation
> `ClaimEnterpriseMultiAccountCoupon`, parameters `--customer_id` /
> `--coupon_id` / `--amount` / `--trans_id`). The current KooCLI build reports
> `Unsupported service: BSS`, so the SDK call above is used; confirm the exact
> KooCLI parameter list with the build's own `--help` when a BSS-capable KooCLI
> is present.

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--customer-id` | Yes | Enterprise sub-account customer ID (领取目标 / 付款接收方) | `CUST001` |
| `--coupon-id` | Yes | Coupon ID to claim from (领取来源 / 拨款来源) | `CP001` |
| `--amount` | Yes | Transfer amount in CNY (元), > 0 and precise to 2 decimals | `100.00` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-1`; BSS is global) | `cn-north-1` |
| `--trans-id` | No | Transaction serial number 交易序列号 (防重复提交); derived deterministically from customer/coupon/amount when omitted | `20261028001` |
| `--operation` | No | KooCLI BSS operation name; only the claim operation is allowed (`ClaimEnterpriseMultiAccountCoupon`; aliases normalised) | `ClaimEnterpriseMultiAccountCoupon` |
| `--dry-run` | No | Preview the request; never executes | — |
| `--confirm` | Yes (to claim) | Explicit confirmation required for the live write | — |
| `--no-list` | No | Skip the post-claim coupon-inventory query | — |
| `--list-limit` | No | Page size for the post-claim inventory (BSS maximum 100; default 100) | `100` |
| `--no-idempotency` | No | Disable the local natural-key idempotency ledger | — |
| `--force` | No | Ignore the ledger and re-claim | — |
| `--idempotency-window` | No | Idempotency window in seconds (default `86400`) | `86400` |
| `--ledger` | No | Idempotency ledger file (default `~/.cache/huawei-cloud-voucher-claim/ledger.json`) | `/tmp/ledger.json` |
| `--json` | No | Output the structured result as JSON | — |

> **On amount / 券码**: the claim API transfers an **amount** (`amount`, 总划拨
> 金额, 单位：元) of an existing coupon (`coupon_id`); it does not take a coupon
> code. The resulting 券码 is read back through the post-claim coupon inventory
> (`ListSubCustomerCoupons` → `coupon_code`).

## Write-Intent Guard

- Only the claim operation (`ClaimEnterpriseMultiAccountCoupon`, plus accepted
  aliases `ClaimCoupon` / `ClaimVoucher` / `ReceiveCoupon` /
  `TransferEnterpriseMultiAccountCoupon`) may be executed; any other
  `--operation` raises a `ValidationError` **before** a single command runs.
- `build_command()` constructs only the claim request — there is no code path
  that can emit a reclaim / freeze / cancel call.

## Danger Confirmation

Because claiming vouchers is a **变更类写操作 that moves money / benefit to the
target sub-account and is normally irreversible**:

- a live claim requires the explicit `--confirm` flag; without it the run stops
  with `领取代金券是变更类写操作... 请确认后加 --confirm 执行` (exit code 2);
- `--dry-run` is available for a safe, side-effect-free preview;
- idempotency (derived `trans_id` + local ledger) prevents accidental
  double-claiming across retries.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `BSS`.
- **Operation name** — PascalCase: `ClaimEnterpriseMultiAccountCoupon`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-1`
  (required for every concrete BSS call; BSS is global, `cn-north-1`).
- **Simple parameter** — `--key=value`, e.g. `--customer_id=CUST001`,
  `--coupon_id=CP001`, `--amount=100.00`, `--trans_id=20261028001`.
- **REST path (official SDK `_http_info`)** —
  `POST /v2/enterprises/multi-accounts/transfer-coupon` (`huaweicloudsdkbss` v2
  `_claim_enterprise_multi_account_coupon_http_info`); the request body is
  `TransferEnterpriseMultiAccountCouponReq` and the call is a global (domain) API.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Missing / invalid parameter (customer / coupon / amount) | Exit 1, `ValidationError` with an explicit hint (e.g. amount must be > 0 with ≤2 decimals) |
| Live claim without `--confirm` | Exit 2, danger-confirmation hint, nothing claimed |
| Missing / invalid AK-SK (CLI or SDK) | Exit 1, `ConfigError`; configure credentials out-of-band (never in chat) |
| 401 / 403 / insufficient IAM permission | Exit 1, `AuthError` hint referencing the IAM policy |
| Duplicate `trans_id` (`CBC.99007009`, 交易事务ID重复) | Exit 1, `ApiError` hint: the request was already submitted — check the coupon inventory before retrying |
| hcloud not installed | Transparent SDK fallback; if the SDK is also unavailable, exit 1 with the install hint |
| Network / unexpected API failure | Exit 1 with the hcloud stderr excerpt (`ApiError`) |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, `ApiError` hint pointing to the operation's own `--help` (service BSS, operation `ClaimEnterpriseMultiAccountCoupon`) |
| Non-claim operation requested | Exit 1, `ValidationError`, no command executed |

Exit codes: `0` success (or an idempotent skip); `1` validation / config / auth /
API error; `2` live claim attempted without `--confirm`.

## Idempotency Semantics

- **Natural key** = `sha256(customer_id | coupon_id | amount)[:32]`, stored in
  the ledger (`~/.cache/huawei-cloud-voucher-claim/ledger.json`, override with
  `--ledger` / `$VOUCHER_CLAIM_LEDGER`) with the claim timestamp and the returned
  `sub_coupon_id`.
- **Derived `trans_id`** = `sha256(customer_id | coupon_id | amount)[:32]` when
  `--trans-id` is omitted; a retry reuses the same serial number so the server
  rejects a duplicate submission (`CBC.99007009`).
- On a run, a natural key present inside `--idempotency-window` (default 24h) is
  skipped (no API call, exit 0, `reason=already_claimed_in_window`).
- `--force` ignores existing entries for one run (and still records the new
  result); `--no-idempotency` disables reading/writing the ledger entirely.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `--dry-run` combined with idempotency | Preview only; the ledger is untouched (even for an already-claimed key the preview still prints the request) |
| Already-claimed key in the window | Exit 0, `reason=already_claimed_in_window`, no API call |
| Amount with > 2 decimals | Rejected (`ValidationError`) rather than silently rounded |
| Post-claim list returns nothing for the customer | Claim still succeeds; the inventory prints `未查询到该客户/该券的券清单记录` |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkbss` (GlobalCredentials + global endpoint), same result shape |
| User asks to reclaim / freeze / cancel coupons | Out of scope — rejected by the operation guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: amount / input validation, deterministic `trans_id` derivation,
operation alias normalisation and guard, claim/list command construction (no
`face_value` / `quota_id` parameter is ever sent), failure classification
(missing AK/SK, 403, generic, `[USE_ERROR]` with rc 0, duplicate `trans_id`),
JSON extraction, claim response parsing, coupon extraction / client-side filter,
idempotency key + ledger load/save/prune, `claim_voucher` (dry-run /
confirm-required / success + ledger / retry-skip / force / list-after-claim /
SDK fallback), and all `main()` modes including exit codes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege write IAM policy for claiming coupons + read-only list |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified (CLI→SDK→API research) |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |