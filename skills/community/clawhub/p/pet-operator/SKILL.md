---
name: pet-operator
description: Delegate Aavegotchi petting rights to AAI's wallet on Base. Generate approve/revoke tx data, check approval, and maintain delegated wallet bookkeeping in pet-me-master config.
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
---

# pet-operator

Set or revoke AAI as pet operator for user wallets, and keep delegation bookkeeping aligned.

## Constants

- AAI operator wallet: `0xb96B48a6B190A9d509cE9312654F34E9770F2110`
- Aavegotchi Diamond: `0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`
- Chain: Base mainnet (`8453`)
- RPC default: `https://mainnet.base.org`

Overridable env:
- `AAVEGOTCHI_DIAMOND`
- `AAI_OPERATOR`
- `BASE_RPC_URL`
- `PET_ME_CONFIG_FILE`

## Scripts

- `./scripts/check-approval.sh <wallet>`
  - Checks `isPetOperatorForAll(owner, operator)`.
- `./scripts/generate-delegation-tx.sh <wallet>`
  - Generates call data for `setPetOperatorForAll(AAI_OPERATOR, true)`.
- `./scripts/generate-revoke-tx.sh <wallet>`
  - Generates call data for `setPetOperatorForAll(AAI_OPERATOR, false)`.
- `./scripts/add-delegated-wallet.sh <wallet> [name]`
  - Verifies approval, fetches owned gotchi IDs, upserts into `pet-me-master` config.
- `./scripts/remove-delegated-wallet.sh <wallet>`
  - Removes wallet bookkeeping entries from config.

## Config Bookkeeping

`add-delegated-wallet.sh` writes to:
- `.delegatedWallets` (preferred)
- `.wallets` (legacy compatibility, only if present)

This does not grant on-chain permissions by itself; on-chain approval must already exist.

## Security

- Operator permission only enables petting, not transfer.
- User keeps full ownership.
- Revocation is one on-chain tx away.
