# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v2/promotions/benefits/coupons` —
  `hcloud BSS ListSubCustomerCoupons`
- SDK fallback: `huaweicloudsdkbss` v2 `BssClient.list_sub_customer_coupons`
  (same REST path, global endpoint)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `bss:coupon:list` | GET /v2/promotions/benefits/coupons | List BSS vouchers / coupons |

`bss:coupon:list` is the read-only action name for the BSS coupon-list API. If
your account uses a system policy, assign the corresponding **BSS ReadOnly**
policy of your IAM domain instead of the custom policy below. Verify the exact
action / policy name in the IAM console (权限及授权项说明) before production use.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:coupon:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 BSS 代金券，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency with BSS access.
2. Grant `bss:coupon:list` (custom policy above) or the domain's BSS read-only
   system policy.
3. Re-run `python3 scripts/list_voucher.py`.
