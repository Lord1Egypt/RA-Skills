# IAM Policies (least privilege, coupon issuance)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `POST /v2/promotions/benefits/partner-coupons` —
  `hcloud BSS CreatePartnerCoupons`
- SDK fallback: `huaweicloudsdkbss` v2 `BssClient.create_partner_coupons`
  (same REST path, global endpoint)

This is a **write** operation: it issues a coupon from one of the partner's
coupon quotas to a sub-customer account, moving a benefit (money) to that
account. Grant only the issue action — do not grant the wider partner /
coupon-administration policies.

## Required IAM action (recommended)

| Action | API | Purpose |
| -------- | ----- | ------- |
| `bss:coupon:send` | POST /v2/promotions/benefits/partner-coupons | Issue a new coupon to a sub-customer |

The exact action / system-policy name for the partner issue-coupon API must be
confirmed in the IAM console (**权限及授权项说明**) for your account before
production use — the least-privilege policy below is the recommended baseline,
not a substitute for that verification. If your account uses a system policy,
assign the corresponding **BSS partner coupon-issue** policy instead.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:coupon:send"
      ],
      "Resource": "*"
    }
  ]
}
```

Also confirm the calling identity is actually a **partner / distributor** of the
target sub-customer accounts: the API can only issue coupons to
代售子客户 (resold sub-customers) of the caller, and only within an available
coupon quota.

## 403 troubleshooting

If the script reports `无权限发放 BSS 代金券，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a partner/distributor user with BSS access.
2. Grant `bss:coupon:send` (custom policy above) or the domain's BSS partner
   coupon-issue system policy.
3. Confirm a usable coupon quota exists
   (`hcloud BSS ListQuotaCoupons --cli-region=cn-north-1`).
4. Re-run `python3 scripts/send_voucher.py ... --confirm`.