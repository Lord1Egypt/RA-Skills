# Verification Method

How `huawei-cloud-voucher-claim` and its behaviour were researched and verified
(creator Step 2: CLI → SDK → API, trusted sources only).

## 1. Operation & REST path (verified from the official SDK and KooCLI metadata)

Verified against the official `huaweicloudsdkbss` v2 client
(`huaweicloudsdkbss/v2/bss_client.py`) and the KooCLI operation metadata
(`ClaimEnterpriseMultiAccountCoupon`):

| Item | Value |
| ------ | ------- |
| Operation | `ClaimEnterpriseMultiAccountCoupon` ("企业主账号向企业子账号拨款优惠券") |
| REST | `POST /v2/enterprises/multi-accounts/transfer-coupon` |
| Request body | `TransferEnterpriseMultiAccountCouponReq` (`customer_id`, `coupon_id`, `amount`, `trans_id`) |
| Response | `ClaimEnterpriseMultiAccountCouponResponse` (`sub_coupon_id` — 成功时返回的子券ID) |
| Scope | An enterprise master account transfers an amount of one of its coupons to one of its own enterprise sub-accounts |
| Constraints | Only coupons issued by Huawei (测试类/商务类/活动类) support transfer; the caller must be the enterprise master account (AK/SK or Token) |

Post-claim inventory (read-only):

| Item | Value |
| ------ | ------- |
| Operation | `ListSubCustomerCoupons` |
| REST | `GET /v2/promotions/benefits/coupons` |
| Query params | `coupon_id`, `order_id`, `promotion_plan_id`, `coupon_type`, `status`, `active_start_time`, `active_end_time`, `offset`, `limit`, `source_id`, `indirect_partner_id` |
| Response list | `user_coupons` (`coupon_id`, `coupon_code`, `status`, `coupon_type`, `face_value`, `balance`, `active_time`, `expire_time`, `customer_id`, …) |

### Spec correction (Step 2 finding)

The Issue Spec's CLI operation name is `ClaimEnterpriseMultiAccountCoupon` and
the REST path `POST /v2/enterprises/multi-accounts/transfer-coupon` — both are
**confirmed** in the official SDK/KooCLI metadata. The claim body parameter that
carries the amount is `amount` (总划拨金额), not `face_value`; the coupon source
is `coupon_id`. The skill parameterises the request accordingly (asserted by the
unit test `test_no_face_value_parameter`).

### Post-claim inventory

The coupon-list API has no `customer_id` query parameter, so the skill fetches
the coupon list with the server-side `coupon_id` filter and applies the
`customer_id` filter **client-side** — the inventory therefore reports
券ID / 券码 / 面额 / 余额 / 有效期 / 状态 for the claimed coupon and customer.

## 2. Endpoint

BSS is a global (domain-level) service; the official SDK
`huaweicloudsdkbss/v2/region/bss_region.py` maps `cn-north-1` to
`https://bss.myhuaweicloud.com`. Both the CLI path (`--cli-region=cn-north-1`)
and the SDK fallback (`GlobalCredentials` + `with_endpoints`) target that global
endpoint.

## 3. Structural & functional verification

- Structure / specification: `huawei-cloud-skill-creator/scripts/validate-skill.sh`
  (hard gate: FAIL = 0).
- Functional smoke: `huawei-cloud-skill-creator/scripts/test-cli-commands.sh`
  (write operation → `--help` syntax check + read-only pre-queries only; no real
  claim).
- Offline unit tests (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: amount validation, input validation, deterministic `trans_id`
derivation, operation alias + guard, claim/list command construction (no
`face_value`/`quota_id` parameter), failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc 0, duplicate `trans_id` CBC.99007009), JSON
extraction, claim response parsing, coupon extraction / client-side filter,
idempotency key + ledger load/save/prune, `claim_voucher` (dry-run /
confirm-required / success + ledger / retry-skip / force / list-after-claim /
SDK fallback), and every `main()` mode including exit codes.

## 4. Not covered here (handed to QA)

A real live claim (requires enterprise-master credentials, a transferable coupon
and an explicit user confirmation) is **not** performed in the coding session; it
is a write, money-moving operation. Functional verification with real (or mock)
credentials is the QA agent's stage.