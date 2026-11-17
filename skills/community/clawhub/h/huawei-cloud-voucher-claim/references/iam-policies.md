# IAM Policies (least privilege, coupon claim)

The skill invokes exactly two Huawei Cloud OpenAPI operations (the CLI and the
SDK path use the same REST paths):

- claim (write, primary): `POST /v2/enterprises/multi-accounts/transfer-coupon`
  — operation `ClaimEnterpriseMultiAccountCoupon` (service BSS; the skill tries
  the KooCLI path first when a BSS-capable KooCLI is present)
  (SDK: `huaweicloudsdkbss` v2 `BssClient.claim_enterprise_multi_account_coupon`)
- post-claim inventory (read-only):
  `GET /v2/promotions/benefits/coupons` —
  operation `ListSubCustomerCoupons` (service BSS)
  (SDK: `huaweicloudsdkbss` v2 `BssClient.list_sub_customer_coupons`)

The claim is a **write** operation: it transfers (拨款) an amount of a coupon
from an enterprise master account to one of its enterprise sub-accounts, moving
a benefit (money) to that sub-account. Grant only the claim action plus the
read-only coupon-list action — do not grant the wider partner /
coupon-administration policies.

## Required IAM action (recommended)

| Action | API | Purpose |
| -------- | ----- | ------- |
| `bss:enterpriseMultiAccount:claimCoupon` | POST /v2/enterprises/multi-accounts/transfer-coupon | Claim (transfer) an amount of a coupon to an enterprise sub-account |
| `bss:coupon:list` | GET /v2/promotions/benefits/coupons | Read-only coupon list used for the post-claim inventory |

> **Verification note (mandatory before production):** the exact IAM action /
> system-policy name for the enterprise multi-account coupon-transfer API must be
> confirmed in the IAM console (**权限及授权项说明**) for your account, or via
> `hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4
> --service_code=<service_code>`. The names above are the recommended baseline,
> not a substitute for that verification (an authorization schema was not
> returned for BSS on the development host at authoring time).

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:enterpriseMultiAccount:claimCoupon",
        "bss:coupon:list"
      ],
      "Resource": "*"
    }
  ]
}
```

Also confirm the calling identity is an **enterprise master account** of the
target sub-account: the API can only transfer coupons between an enterprise
master and its own enterprise sub-accounts, and only for coupons that support
transfer (华为发放的测试类、商务类、活动类代金券).

## 403 troubleshooting

If the script reports `无权限领取代金券，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to the enterprise master account with BSS access.
2. Grant the claim + list actions (custom policy above) or the domain's
   BSS enterprise multi-account system policy.
3. Confirm a transferable coupon exists and the sub-account belongs to this
   master account.
4. Re-run `python3 scripts/claim_voucher.py ... --confirm`.