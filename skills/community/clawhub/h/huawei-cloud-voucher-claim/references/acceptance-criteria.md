# Acceptance Criteria — huawei-cloud-voucher-claim

| # | Criterion | How satisfied |
| --- | ----------- | --------------- |
| 1 | Claim a coupon for an enterprise sub-account and the API returns success | `scripts/claim_voucher.py --customer-id … --coupon-id … --amount … --confirm` → operation `ClaimEnterpriseMultiAccountCoupon` (service BSS, `POST /v2/enterprises/multi-accounts/transfer-coupon`; KooCLI first when available, else `huaweicloudsdkbss` v2); response `sub_coupon_id` is reported |
| 2 | Post-claim inventory (券ID/券码/面额/余额/有效期/状态) | After a successful claim the script runs the read-only `ListSubCustomerCoupons` (`GET /v2/promotions/benefits/coupons`), filters by `customer_id` client-side and renders the inventory (table / `--json`); `--no-list` skips it |
| 3 | Idempotency — repeated calls do not double-claim | Deterministic `trans_id` (customer_id\|coupon_id\|amount) + a local natural-key ledger; targets inside `--idempotency-window` are skipped; `--force` overrides; `--no-idempotency` disables |
| 4 | Missing / invalid parameters produce a clear error | `ValidationError` (a `ConfigError` subclass) with an explicit hint; exit 1 |
| 5 | Graded errors | `ConfigError` (params / credentials) / `AuthError` (401/403 IAM) / `ApiError` (API / network / duplicate `trans_id`), each with an actionable message |
| 6 | CLI first, SDK fallback | KooCLI primary; `huaweicloudsdkbss` v2 `claim_enterprise_multi_account_coupon` / `list_sub_customer_coupons` used transparently when `hcloud` is absent |
| 7 | Unified credential loading | `scripts/config.py` resolves the hcloud profile (CLI) / standard environment variables (SDK); secrets are never echoed |
| 8 | Write-operation safety | A live claim requires explicit `--confirm`; without it the run prints a preview and exits 2; `--dry-run` previews without side effects; only the claim operation can execute |
| 9 | Offline tests | `python3 -m unittest discover -s tests -v` — validation, command construction, guard, error grading, idempotency, SDK fallback, output modes |
| 10 | Passes the Huawei Cloud Skill Specification | `validate-skill.sh -s <skill>`: required sections, frontmatter, reference docs, CLI command format, size/extension limits |

## Out of scope

Coupon reclaim / return / freeze / cancel, partner issuance to resold
sub-customers (a different BSS operation), and coupon queries beyond the
post-claim inventory.

## Residual / QA notes

- A real live claim requires enterprise-master credentials, a transferable
  (Huawei-issued) coupon and an explicit user confirmation; it is not performed
  during skill development.
- The exact IAM action name for the claim API should be confirmed in the IAM
  console (see `references/iam-policies.md`).