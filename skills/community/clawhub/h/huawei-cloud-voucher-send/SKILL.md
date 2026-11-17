---
name: huawei-cloud-voucher-send
description: |
  1. Issue (发放) new Huawei Cloud BSS (费用中心) vouchers / coupons to
     sub-customers / partners through KooCLI (hcloud BSS CreatePartnerCoupons —
     mutating POST /v2/promotions/benefits/partner-coupons), with an automatic
     fallback to the official huaweicloudsdkbss v2 SDK when hcloud is not
     installed.
  2. Zero-config operation: the invocation path is chosen automatically (CLI
     first, SDK fallback); credentials are loaded only from the hcloud profile
     or the standard Huawei Cloud environment variables.
  3. Batch-aware: one call issues coupons to many sub-customer accounts
     (repeatable --customer-id / comma --customer-ids / --customers-file).
  4. Idempotent: a per-customer natural key is remembered in a local ledger, so
     retrying a partially failed batch never double-issues an already-issued
     customer; --force overrides, --no-idempotency disables.
  5. Safe by default for a money-moving, irreversible operation: a live send
     requires the explicit --confirm flag; --dry-run previews the exact request
     without issuing anything.
  6. Graded errors: ConfigError (missing/invalid parameters or credentials) /
     AuthError (401/403 / insufficient IAM permission) / ApiError (unexpected
     API or network failure), each with an actionable hint.
  7. Offline unit tests (mocked hcloud subprocess) cover validation, batch
     construction, idempotency, error grading, SDK fallback and all CLI modes.
  8. Triggers include: "发放代金券", "给子客户发券", "发放优惠券给子客户",
     "合作伙伴发券", "send voucher", "issue coupon", "create partner coupons",
     "华为云代金券发放", "BSS coupon issue".
  9. Write-intent guard: only the issue-coupon operation ever executes; reclaim
     / transfer / freeze / individually-issued-coupon mutation operations are
     rejected — this skill issues new coupons only.
tags: [huawei-cloud, bss, billing, write, koo-cli]
---

# Huawei Cloud BSS Voucher Send (发放代金券给子客户/合作伙伴)

## Overview

Issue **new** Huawei Cloud BSS vouchers / coupons to one or more sub-customer /
partner accounts through the KooCLI issue-coupon operation
(`CreatePartnerCoupons`, hcloud service `BSS`) on the official
issue-coupon API, `POST /v2/promotions/benefits/partner-coupons`, verified in
the `huaweicloudsdkbss` v2 client `_create_partner_coupons_http_info`
metadata). When `hcloud` is not installed the skill falls back to the official
`huaweicloudsdkbss` v2 SDK (`BssClient.create_partner_coupons`).

Architecture:

```text
agent → python3 scripts/send_voucher.py --quota-id <q> --customer-id <c> --face-value <v> --confirm
      → hcloud BSS CreatePartnerCoupons --cli-region=<region> ... (mutating POST)
      → Huawei Cloud BSS OpenAPI (global endpoint) → coupon_infos / error_details
      → idempotency ledger (per customer) + human summary / --json

(hcloud binary missing) → fallback: huaweicloudsdkbss v2 BssClient.create_partner_coupons
```

Key properties:

- **Write by design, safe by default** — issuing a coupon moves money / benefit
  to the target account and is normally irreversible. A live send requires the
  explicit `--confirm` flag; without it the run stops and prints a warning.
  `--dry-run` previews the exact request (including the ledger skips) without
  issuing anything.
- **Issuance source & the coupon code** — a *new* coupon has no 券码 before it is
  issued: the BSS issue API selects the coupon source by **coupon quota**
  (`quota_id`, an 额度ID obtained from `ListQuotaCoupons`), and **returns** the
  generated `coupon_id` / 券码 for each target. `coupon_code` is therefore a
  response-only field; this skill correctly parameterises the request with
  `quota_id` + `face_value` instead of a pre-existing code. (The Spec
  placeholder operation `SendSubCustomerCoupons` does not exist in the official
  API and is accepted only as a naming alias of `CreatePartnerCoupons`.)
- **Batch** — many sub-customers are issued in a single API call; the response
  reports per-customer successes (`coupon_infos`) and per-customer failures
  (`error_details`).
- **Idempotent / no double-issue** — a per-customer natural key (quota + customer
  + face value + expiry + memo + limits) is stored in a local ledger. On retry,
  customers already issued inside the idempotency window are skipped, so
  re-running a partially failed batch only retries the failures.
- **CLI first, SDK fallback** — KooCLI is the primary path; when the KooCLI
  binary is absent the script falls back to `huaweicloudsdkbss` v2. BSS is a
  *global* service, so the SDK path uses `GlobalCredentials` + `with_endpoints`
  (`https://bss.myhuaweicloud.com`). Credentials are resolved by `config.py`
  (hcloud profile for the CLI path; standard environment variables for the SDK
  path) — never handled by the skill.
- **Offline-testable** — validation, batch construction, idempotency, error
  grading, SDK fallback and all output modes are covered by unit tests that mock
  the hcloud subprocess.

Out of scope: coupon queries (use the read-only sibling skill), coupon
reclaim / return / freeze / cancel, and the account-to-account *transfer*
semantic (a different BSS operation).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkbss` to enable the
   SDK fallback path.
2. **Credential profile** — configure credentials out-of-band (hcloud configure
   in your terminal, or the standard credential environment variables). Never
   paste AK/SK into chat; `config.py` reads the hcloud profile / environment and
   never echoes or stores secrets.
3. **IAM write permission** — the issue-coupon action (least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md)). The calling
   identity must be a distributor / partner of the target sub-customers.
4. **A coupon quota (`quota_id`)** — the source of the coupon to issue; query it
   with `hcloud BSS ListQuotaCoupons --cli-region=cn-north-1`.
5. **Python 3.8+** (standard library only for the command path — argparse /
   json / subprocess / decimal).
6. **Outbound HTTPS** access to `bss.myhuaweicloud.com`.
7. **Region** — BSS is a global service; use `cn-north-1` (the default here).

## Workflow

1. **Confirm the danger** — issuing vouchers is a money-moving, irreversible
   change. Obtain explicit user confirmation (the caller sets `--confirm`); the
   skill refuses to send without it.
2. **Resolve the source quota** — query the coupon quota
   (`hcloud BSS ListQuotaCoupons --cli-region=cn-north-1`) to get the `quota_id` to issue from.
3. **Prepare the batch** — one or more target sub-customer account IDs
   (`--customer-id`, `--customer-ids`, or `--customers-file`) and the coupon
   `--face-value` (+ optional validity window / limits / memo).
4. **Preview** — run with `--dry-run` to inspect the exact request and the
   idempotency skips; nothing is issued.
5. **Issue** — re-run with `--confirm` to issue; the per-customer `coupon_id` /
   errors are reported and the successes are recorded in the idempotency ledger.
6. **Retry safely** — re-running the same command retries only the customers
   that are not yet recorded inside the idempotency window.

## Core Commands

```bash
# Preview the issue request (no send):
python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \
  --customer-id CUST001 --customer-id CUST002 --dry-run

# Issue to a batch of sub-customers (requires explicit confirmation):
python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \
  --customer-ids CUST001,CUST002 --memo "2026-Q1 营销" --confirm

# Issue with a validity window and a cloud-service restriction:
python3 scripts/send_voucher.py --quota-id Q001 --face-value 50.00 \
  --customer-id CUST001 \
  --valid-time 2026-01-01T00:00:00Z --expire-time 2026-12-31T23:59:59Z \
  --cloud-service-type ECS --confirm

# Read targets from a file (one account ID per line):
python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \
  --customers-file customers.txt --confirm

# Force a re-issue inside the idempotency window, or disable idempotency:
python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \
  --customer-id CUST001 --force --confirm

# Machine-readable result:
python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \
  --customer-id CUST001 --confirm --json
```

Equivalent direct KooCLI command (the script wraps exactly this call):

```bash
hcloud BSS CreatePartnerCoupons --cli-region=cn-north-1 --quota_id=Q001 \
  --customer_ids.1=CUST001 --customer_ids.2=CUST002 --face_value=100.00
```

> The issue operation is `CreatePartnerCoupons` (the underlying
> `POST /v2/promotions/benefits/partner-coupons`). When hcloud is available,
> confirm the exact parameter list with
> `hcloud BSS CreatePartnerCoupons --cli-region=cn-north-1 --help`.

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--quota-id` | Yes | Coupon quota ID to issue from (代金券额度ID; the coupon source) | `Q001` |
| `--customer-id` | Yes* | Target sub-customer account ID (repeatable for batch) | `CUST001` |
| `--customer-ids` | Yes* | Target sub-customer account IDs, comma-separated (batch) | `CUST001,CUST002` |
| `--customers-file` | Yes* | File with one target account ID per line (`#` comments allowed) | `customers.txt` |
| `--face-value` | Yes | Coupon face value in CNY (元), > 0 and precise to 2 decimals | `100.00` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-1`; BSS is global) | `cn-north-1` |
| `--valid-time` | No | Validity start, UTC `yyyy-MM-ddTHH:mm:ssZ` (default: quota's effective time) | `2026-01-01T00:00:00Z` |
| `--expire-time` | No | Expiry, UTC `yyyy-MM-ddTHH:mm:ssZ` (default: quota's expiry) | `2026-12-31T23:59:59Z` |
| `--cloud-service-type` | No | Allowed cloud service type (repeatable, max 10) | `ECS` |
| `--product-id` | No | Allowed product ID (repeatable) | `P1` |
| `--memo` | No | Free-text memo recorded with the issuance | `2026-Q1 营销` |
| `--indirect-partner-id` | No | Cloud reseller ID (required when a reseller issues to its sub-customer) | `IP001` |
| `--operation` | No | hcloud BSS operation name; only the issue operation is allowed (`CreatePartnerCoupons`; aliases normalised) | `CreatePartnerCoupons` |
| `--dry-run` | No | Preview the request; never executes | — |
| `--confirm` | Yes (to send) | Explicit confirmation required for the live write | — |
| `--json` | No | Output the structured result as JSON | — |
| `--no-idempotency` | No | Disable the per-customer idempotency ledger | — |
| `--force` | No | Ignore the ledger and re-issue | — |
| `--idempotency-window` | No | Idempotency window in seconds (default `86400`) | `86400` |
| `--ledger` | No | Idempotency ledger file (default `~/.cache/huawei-cloud-voucher-send/ledger.json`) | `/tmp/ledger.json` |

`*` At least one target source (`--customer-id` / `--customer-ids` /
`--customers-file`) is required; duplicates across sources are de-duplicated.

> **On 券码 (coupon code)**: the BSS issue API does not accept a coupon code —
> a new coupon only receives its `coupon_id` / 券码 **after** issuance, returned
> in `coupon_infos`. The coupon source is selected by the **quota** (`quota_id`)
> and the amount by `--face-value`. If the requirement needs a coupon-code based
> operation, that is the account-transfer / reclaim family, which this skill
> deliberately does not cover.

## Write-Intent Guard

- Only the issue operation (`CreatePartnerCoupons`, plus accepted aliases
  `CreateSubCustomerCoupons` / `SendSubCustomerCoupons` / `SendCoupons`) may be
  executed; any other `--operation` raises a `ValidationError` **before** a
  single command runs.
- `build_command()` constructs only the issue request — there is no code path
  that can emit a reclaim / transfer / freeze call.

## Danger Confirmation

Because issuing vouchers is a **变更类写操作 that moves money / benefit to the
target account and is normally irreversible**:

- a live send requires the explicit `--confirm` flag; without it the run stops
  with `发放代金券是变更类写操作... 请确认后加 --confirm 执行` (exit code 2);
- `--dry-run` is available for a safe, side-effect-free preview;
- idempotency prevents accidental double-issuance across retries.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `BSS`.
- **Operation name** — PascalCase: `CreatePartnerCoupons`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-1`
  (required for every concrete BSS call; BSS is global, `cn-north-1`).
- **Simple parameter** — `--key=value`, e.g. `--quota_id=Q001`,
  `--face_value=100.00`, `--memo=promo`.
- **Array parameter** — `--key.<index>=value` (KooCLI form), e.g.
  `--customer_ids.1=CUST001 --customer_ids.2=CUST002`,
  `--cloud_service_types.1=ECS`.
- **REST path (official SDK `_http_info`)** —
  `POST /v2/promotions/benefits/partner-coupons` (`huaweicloudsdkbss` v2
  `_create_partner_coupons_http_info`); the request body is
  `CreatePartnerCouponsReq` and the call is a global (domain) API.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Missing / invalid parameter (quota / customers / face value / time) | Exit 1, `ValidationError` with an explicit hint (e.g. face value must be > 0 with ≤2 decimals) |
| Live send without `--confirm` | Exit 2, danger-confirmation hint, nothing issued |
| Missing / invalid AK-SK (CLI or SDK) | Exit 1, `ConfigError`; configure credentials out-of-band (never in chat) |
| 401 / 403 / insufficient IAM permission | Exit 1, `AuthError` hint referencing the IAM policy |
| Partial batch failure (HTTP 200 with `error_details`) | Exit 1, per-customer success/error summary; successes recorded in the ledger |
| hcloud not installed | Transparent SDK fallback; if the SDK is also unavailable, exit 1 with the install hint |
| Network / unexpected API failure | Exit 1 with the hcloud stderr excerpt (`ApiError`) |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, `ApiError` hint pointing to `hcloud BSS CreatePartnerCoupons --cli-region=cn-north-1 --help` |
| Non-issue operation requested | Exit 1, `ValidationError`, no command executed |

Exit codes: `0` success; `1` validation / config / auth / API error (or a partial
batch failure); `2` live send attempted without `--confirm`.

## Idempotency & Batch Semantics

- **Natural key** (per target) = `sha256(quota_id | customer_id | face_value |
  expire_time | memo | cloud_service_types | product_ids |
  indirect_partner_id)[:32]`.
- The ledger (`~/.cache/huawei-cloud-voucher-send/ledger.json`, override with
  `--ledger` / `$VOUCHER_SEND_LEDGER`) stores the key with the issue timestamp
  and the returned `coupon_id`.
- On a run, targets whose key is present inside `--idempotency-window` (default
  24h) are skipped; only the remaining targets are sent. A partially failed
  batch therefore retries only the failures on the next run.
- `--force` ignores existing entries for one run (but still records the new
  result); `--no-idempotency` disables reading/writing the ledger entirely.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Duplicate customer IDs across `--customer-id` / `--customer-ids` / file | De-duplicated, order preserved |
| Face value with > 2 decimals | Rejected (`ValidationError`) rather than silently rounded |
| All targets already issued in the window | Exit 0, `reason=all_skipped_by_idempotency`, no API call |
| `--dry-run` combined with idempotency | Preview shows the exact skipped vs pending targets; ledger untouched |
| Multiple `--cloud-service-type` | Forwarded as indexed array parameters; API caps at 10 |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkbss` `create_partner_coupons` (GlobalCredentials + global endpoint), same result shape |
| User asks to reclaim / transfer coupons | Out of scope — rejected by the operation guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: face-value / time / customer validation, CLI batch construction
(indexed array parameters; no `coupon_code` parameter is ever sent), operation
alias normalisation and guard, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc 0), JSON extraction, response parsing,
idempotency key stability + ledger load/save/prune, `send_coupons` dry-run /
confirm-required / success+ledger / retry-skip / force / partial-error / SDK
fallback, and all `main()` modes including exit codes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege write IAM policy for issuing coupons |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified (CLI→SDK→API research) |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |