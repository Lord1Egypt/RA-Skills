# Data Flow

```mermaid
flowchart TD
    A[Agent / operator] --> B[python3 scripts/claim_voucher.py]
    B --> C{--dry-run or no --confirm?}
    C -- preview --> D[Print request preview + trans_id\nno claim]
    C -- confirmed --> E{natural key already in\nidempotency ledger?}
    E -- yes --> F[Exit 0\nalready_claimed_in_window]
    E -- no --> G{BSS-capable KooCLI available?}
    G -- yes --> H[KooCLI claim operation ClaimEnterpriseMultiAccountCoupon\nPOST /v2/enterprises/multi-accounts/transfer-coupon]
    G -- no --> I[huaweicloudsdkbss v2\nBssClient.claim_enterprise_multi_account_coupon\nGlobalCredentials + global endpoint]
    H --> J[Parse sub_coupon_id]
    I --> J
    J --> K[Record claim in idempotency ledger]
    K --> L[Read-only post-claim inventory:\noperation ListSubCustomerCoupons\nGET /v2/promotions/benefits/coupons]
    L --> M[Client-side filter by customer_id]
    M --> N[Human table\n券ID/券码/面额/余额/有效期/状态\nor --json]
```

Notes:

- The idempotency ledger is consulted **before** any API call, so a retry inside
  the window does not claim twice. The derived `trans_id` (customer_id |
  coupon_id | amount) additionally lets the server reject a duplicate submission
  (`CBC.99007009`).
- `--dry-run` (or a missing `--confirm`) prints the exact request and the derived
  `trans_id` without claiming anything and never touches the ledger.
- The post-claim inventory is read-only; `customer_id` has no server-side
  parameter and is applied client-side.
- Credentials are never part of the data flow of this script: the CLI path uses
  the active `hcloud` profile, the SDK path reads the standard environment
  variables via `config.py`.