# Verification Method

How `huawei-cloud-voucher-send` and its behaviour were researched and verified
(creator Step 2: CLI → SDK → API, trusted sources only).

## 1. Operation & REST path (verified from the official SDK)

Verified against the official `huaweicloudsdkbss` v2 client
(`huaweicloudsdkbss/v2/bss_client.py`,
`_create_partner_coupons_http_info`):

| Item | Value |
| ------ | ------- |
| Operation | `CreatePartnerCoupons` ("发放优惠券") |
| REST | `POST /v2/promotions/benefits/partner-coupons` |
| Request body | `CreatePartnerCouponsReq` (`quota_id`, `customer_ids`, `face_value`, `valid_time`, `expire_time`, `cloud_service_types`, `product_ids`, `memo`, `indirect_partner_id`) |
| Response | `CreatePartnerCouponsResponse` (`coupon_infos` = successful customer→coupon list, `error_details` = failed customers) |
| Scope | Partner issues coupons to 代售子客户 within an available coupon quota |

### Spec correction (Step 2 finding)

The Issue Spec's placeholder CLI operation `SendSubCustomerCoupons` **does not
exist** in the official BSS API (nor in the `huaweicloudsdkbss` client). The
actual issue-coupon operation is `CreatePartnerCoupons`; the skill uses that
name and normalises the placeholder as an accepted alias.

### Coupon-code note

A newly issued coupon has no 券码 before issuance: the API selects the source by
**coupon quota** (`quota_id`, queried with `ListQuotaCoupons`) and the amount by
`face_value`, and **returns** the generated `coupon_id` / 券码 per target. The
BSS issue API therefore has no `coupon_code` request parameter; the skill
parameterises the request with `quota_id` + `face_value` accordingly (asserted by
the unit test `test_no_coupon_code_parameter`).

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
  issuance).
- Offline unit tests (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: parameter validation (quota / customers / face value / time),
operation alias + guard, batch command construction (indexed array parameters;
no `coupon_code`), failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc 0), JSON extraction, response parsing, idempotency key +
ledger load/save/prune, `send_coupons` (dry-run / confirm-required / success +
ledger / retry-skip / force / partial error / SDK fallback), and every `main()`
mode including exit codes.

## 4. Not covered here (handed to QA)

A real live issuance (requires partner credentials, a funded coupon quota and an
explicit user confirmation) is **not** performed in the coding session; it is a
write, money-moving operation. Functional verification with real (or mock)
credentials is the QA agent's stage.