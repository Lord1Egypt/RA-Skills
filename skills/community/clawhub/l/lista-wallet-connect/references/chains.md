# Supported Chains & Tokens

## EVM Chains

| Chain | CAIP-2 ID | Native | Notes |
|-------|-----------|--------|-------|
| Ethereum | `eip155:1` | ETH | Mainnet |
| BSC | `eip155:56` | BNB | BNB Smart Chain (Lista Lending) |

## Tokens

### Ethereum

| Token | Decimals | Address |
|-------|----------|---------|
| USDC | 6 | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| USDT | 6 | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| WETH | 18 | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |
| DAI | 18 | `0x6B175474E89094C44Da98b954EedeAC495271d0F` |
| WBTC | 8 | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` |

### BSC (Lista Lending)

| Token | Decimals | Address |
|-------|----------|---------|
| WBNB | 18 | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |
| BTCB | 18 | `0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c` |
| USD1 | 18 | `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d` |
| USDT | 6 | `0x55d398326f99059fF775485246999027B3197955` |
| USDC | 6 | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |

## EVM Methods

- `personal_sign` — sign a message (used for auth/consent)
- `eth_sendTransaction` — send a transaction (native or token transfer)
- `eth_signTypedData_v4` — EIP-712 typed data signing
