---
tags: [contract, address, chain, explorer, cross-mainnet]
summary: On-chain contract addresses and block explorer
type: data
---

# Contracts and Chain Details

Use this file when debugging paid-room flow or on-chain configuration.

Production network:
- CROSS Mainnet
- chainId: 612055
- Block Explorer: `https://explorer.crosstoken.io/612055`

> Always use the official CROSS block explorer above to verify transactions.
> Do NOT use crossscan.io or any other third-party explorer.

Contracts:

- ArenaPaid: `0x8f705417C2a11446e93f94cbe84F476572EE90Ed`
- ArenaFree: `0xAbC98bBe54e5bc495D97E6A9c51eEf14fd34e77D`
- RewardVault: `0x046a1C632f7e21C215CaF11e1176861567FcB8EE`
- Moltz ERC-20: `0xdb99a97d607c5c5831263707E7b746312406ba7E`
- WalletFactory (current): `0x378De49F47817D3dF10393851A587e5C2C58EF7C`
- WalletFactory (legacy): `0x0713665E4D19fD16e1F09AD77526CC343c6F0223`
- IdentityRegistry (ERC-8004): `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- ReputationRegistry (ERC-8004): `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

Use these values for:
- verifying chain configuration
- debugging paid-room EIP-712 flow
- validating token or contract destinations
- recovering assets from legacy SC wallets (use legacy WalletFactory `0x0713665E4D19fD16e1F09AD77526CC343c6F0223` — call `getWallets(ownerEoa)`, then `withdrawMoltz`/`withdrawNative` on each legacy wallet; Owner EOA must have CROSS for gas)
