---
name: forge-token-deployer
description: Deploy new tokens on Cross Forge and create liquidity pools via CrossToken CLI.
---

# Forge Token Deployer

Deploy tokens by selecting authentication method and wallet type via CrossToken CLI.

## Options Matrix

| Options | Auth | Wallet | Behavior |
|---------|------|--------|----------|
| `--auth=client --wallet=user` | ClientKey | User wallet | Token deploy + unsigned tx returned |
| `--auth=client --wallet=tmp` | ClientKey | Temp wallet | Token deploy + pool creation |
| `--auth=vendor --wallet=user` | Vendor | User wallet | Token deploy + unsigned tx returned |
| `--auth=vendor --wallet=tmp` | Vendor | Temp wallet | Token deploy + pool creation **(default)** |

### Auth Methods

- **client**: Authenticate with ClientKey/Secret from RampConsole (https://cross-ramp-console.crosstoken.io). Requires `.env` setup.
- **vendor**: No sign-up or credentials needed. Works out of the box.

### Wallet Types

- **user**: User's real wallet becomes token owner. Pool creation requires signing unsigned tx on frontend.
- **tmp**: Creates a temporary wallet and completes pool creation automatically. Owner permissions are not reusable.

## Important Notes

- Symbols are globally unique and case-insensitive.
- **Agent token (`ai_agent` category)**: Always use `--wallet=user` with the agent EOA.
- `--wallet=tmp`: The temporary wallet becomes token owner. Owner permissions are **not reusable**.
- `--wallet=user`: Pool creation is **not automatic**. The unsigned tx must be signed by the user's wallet.
- Always confirm parameters with the user before executing the deploy command.
