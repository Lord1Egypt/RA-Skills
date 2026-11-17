# Data Flow

```mermaid
flowchart TD
    A[Agent / operator] --> B[python3 scripts/send_voucher.py]
    B --> C{--dry-run?}
    C -- yes --> D[Print request preview\nno issuance]
    C -- no --> E{--confirm?}
    E -- no --> F[Stop: danger confirmation required exit 2]
    E -- yes --> G{targets already in\nidempotency ledger?}
    G -- all skipped --> H[Exit 0\nall_skipped_by_idempotency]
    G -- some pending --> I{hcloud installed?}
    I -- yes --> J[hcloud BSS CreatePartnerCoupons\nPOST /v2/promotions/benefits/partner-coupons]
    I -- no --> K[huaweicloudsdkbss v2\nBssClient.create_partner_coupons\nGlobalCredentials + global endpoint]
    J --> L[Parse coupon_infos / error_details]
    K --> L
    L --> M[Record issued customers\ninto idempotency ledger]
    M --> N[Human summary or --json\nsuccess / errors / skipped]
```

Notes:

- The idempotency ledger is consulted **before** any API call, so a retry of a
  partially failed batch only sends the customers that were not yet issued.
- The `--dry-run` preview shows both the skipped and the pending targets and
  never touches the ledger.
- Credentials are never part of the data flow of this script: the CLI path uses
  the active `hcloud` profile, the SDK path reads the standard environment
  variables via `config.py`.