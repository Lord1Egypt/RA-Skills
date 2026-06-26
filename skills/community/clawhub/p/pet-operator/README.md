# Pet Operator

Delegate Aavegotchi petting rights to AAI while keeping full ownership.

## What It Does

This repo helps users approve AAI's operator wallet as pet operator on Base:
- AAI operator wallet: `0xb96B48a6B190A9d509cE9312654F34E9770F2110`
- Aavegotchi Diamond: `0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`

Approval call:
- `setPetOperatorForAll(address operator, bool approved)`

## Scripts

- `scripts/check-approval.sh <wallet>`
  - Returns `approved` / `not_approved`
- `scripts/generate-delegation-tx.sh <wallet>`
  - Prints transaction details for `approved=true`
- `scripts/generate-revoke-tx.sh <wallet>`
  - Prints transaction details for `approved=false`
- `scripts/add-delegated-wallet.sh <wallet> [name]`
  - Verifies approval, fetches wallet gotchi IDs, upserts into pet-me-master config (`delegatedWallets`; legacy `wallets` if present)
- `scripts/remove-delegated-wallet.sh <wallet>`
  - Removes wallet from pet-me-master config tracking arrays

## Notes

- This skill does not move NFTs or tokens.
- Users can revoke anytime by sending the revoke transaction.
- Pet-me-master now supports dynamic wallet/delegation discovery; config writes are mainly operational bookkeeping.
