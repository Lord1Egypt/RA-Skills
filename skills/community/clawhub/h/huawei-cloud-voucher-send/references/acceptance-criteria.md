# Acceptance Criteria — huawei-cloud-voucher-send

| # | Criterion | How satisfied |
| --- | ----------- | --------------- |
| 1 | Issue a new coupon to a sub-customer / partner and the API returns success | `scripts/send_voucher.py --quota-id … --customer-id … --face-value … --confirm` → `hcloud BSS CreatePartnerCoupons` (`POST /v2/promotions/benefits/partner-coupons`); response `coupon_infos` reports the issued `coupon_id` |
| 2 | Batch issuance | `--customer-id` (repeatable) / `--customer-ids` (comma) / `--customers-file`; all targets sent in one API call |
| 3 | Idempotency — repeated calls do not double-issue | Per-customer natural key recorded in a local ledger; targets inside `--idempotency-window` are skipped; `--force` overrides |
| 4 | Missing / invalid parameters produce a clear error | `ValidationError` (a `ConfigError` subclass) with an explicit hint; exit 1 |
| 5 | Graded errors | `ConfigError` (params / credentials) / `AuthError` (401/403 IAM) / `ApiError` (API / network), each with an actionable message |
| 6 | CLI first, SDK fallback | KooCLI is primary; `huaweicloudsdkbss` v2 `create_partner_coupons` is used transparently when `hcloud` is absent |
| 7 | Unified credential loading | `scripts/config.py` resolves the hcloud profile (CLI) / standard environment variables (SDK); secrets are never echoed |
| 8 | Write-operation safety | Live send requires explicit `--confirm`; `--dry-run` previews without side effects; only the issue operation can execute |
| 9 | Offline tests | `python3 -m unittest discover -s tests -v` — validation, batch, idempotency, error grading, SDK fallback, output modes |
| 10 | Passes the Huawei Cloud Skill Specification | `validate-skill.sh -s <skill>`: required sections, frontmatter, reference docs, CLI command format, size/extension limits |

## Out of scope

Coupon queries (read-only sibling skill), coupon reclaim / freeze / cancel, and
the account-to-account transfer semantic.

## Residual / QA notes

- A real live issuance requires partner credentials + a funded coupon quota and
  an explicit user confirmation; it is not performed in the coding session.
- The exact IAM action name for the issue-coupon API should be confirmed in the
  IAM console (see `references/iam-policies.md`).