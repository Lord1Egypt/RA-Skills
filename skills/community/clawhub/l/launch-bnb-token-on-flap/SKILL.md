---
name: launch-bnb-token-on-flap
description: Launch a token on Flap BNB
metadata: {"openclaw": {"always": false, "emoji": "🦋", "homepage": "https://docs.flap.sh", "requires": {"anyBins": ["node", "npx", "npm"]}}}
---

# 🦋 Launch a BNB Token on Flap

Launch a token on [Flap](https://docs.flap.sh) (BNB Chain). Execute each step in order. Read each reference file at the step that requires it — do not pre-load them.

---

## ⚠️ Security Notice

This skill requires sensitive capabilities that must be provided:

- **EVM wallet with signing capability** — hardware wallet, browser wallet, MPC, or other secure signing method for BNB Chain (chain ID 56). The skill mainly focuses on constructing transaction data and then the transaction should be signed by the EVM wallet. Always verify transaction details independently before signing.    
- **BNB mainnet RPC endpoint** — a trusted RPC URL for reading blockchain state and broadcasting transactions. If not presently available, this skill will use the public fallback `https://bsc-dataseed.binance.org/`.  

---

## Directory structure

```
skills/launch-bnb-token-on-flap/
├── SKILL.md                        ← this file
└── references/
    ├── preflight.md                ← Step 0: prerequisites
    ├── vault-factory.md            ← Step 2: vault factory setup
    ├── meta-upload.md              ← Steps 3 & 6: metadata upload
    ├── tax-params.md               ← Step 4: tax parameters
    ├── salt-finding.md             ← Step 7: vanity salt mining
    └── construct-tx.md             ← Step 8: transaction construction
```

---

## Step 0 — Preflight check

Before starting, verify that all required reference files are present. If any are missing, you **MUST** obtain them before proceeding: 

**Required files:**

- `references/preflight.md`
- `references/vault-factory.md`
- `references/meta-upload.md`
- `references/tax-params.md`
- `references/salt-finding.md`
- `references/construct-tx.md`

Check each file exists, then read `references/preflight.md` and verify every prerequisite is satisfied before continuing.

---

## Step 1 — Choose token type

Determine the token configuration:

1. **Tax token or standard (non-tax) token?**
2. If tax token: **Use a Vault Factory for revenue management?**

Decision map:

| Choice | Contract to call |
|---|---|
| Standard token | `Portal.newTokenV6` with `tokenVersion = TOKEN_V2_PERMIT` |
| Tax token, no vault | `Portal.newTokenV6` with `tokenVersion = TOKEN_TAXED_V3` |
| Tax token + vault | `VaultPortal.newTokenV6WithVault` with `tokenVersion = TOKEN_TAXED_V3` |

---

## Step 2 — Vault Factory setup *(tax + vault only)*

Read `references/vault-factory.md` to:

1. Determine the vault factory address to use.
2. Call the factory's `vaultDataSchema()` to understand the required `vaultData` encoding.
3. Determine the values needed to encode `vaultData`.

Skip this step for standard tokens or tax tokens without a vault.

---

## Step 3 — Token metadata

Determine the following token metadata fields:

- **Required:** `name`, `symbol`, image file path
- **Optional:** `description`, `twitter` handle, `telegram` handle (omit if not available)

Read `references/meta-upload.md` when ready to upload the image and construct the metadata JSON.

---

## Step 4 — Tax parameters *(tax token only)*

Read `references/tax-params.md` to determine and validate:

- `buyTaxRate`, `sellTaxRate`
- `taxDuration`, `antiFarmerDuration`
- `mktBps`, `deflationBps`, `dividendBps`, `lpBps`
- `minimumShareBalance`
- `beneficiary` address *(only for tax token without vault)*

Skip this step for standard tokens.

---

## Step 5 — Launch buy amount

Determine `quoteAmt`: the amount of BNB to spend on the initial buy at launch (in BNB, will be converted to wei). This becomes both the `quoteAmt` field and the `msg.value` of the transaction. Use `0` to skip the initial buy.

---

## Step 6 — Upload metadata

Follow `references/meta-upload.md` to upload the image and metadata JSON to Flap's upload API. Store the returned IPFS CID as `meta`.

---

## Step 7 — Find the salt

Read `references/salt-finding.md` to mine a vanity salt using CREATE2 prediction:

- Tax token address must end in `7777`.
- Standard token address must end in `8888`.

Save the resulting `salt` (bytes32) and the predicted `tokenAddress`.

---

## Step 8 — Construct the EVM transaction

Read `references/construct-tx.md` to assemble the full calldata, `value`, and `to` address for the correct contract entry point (`Portal` or `VaultPortal`).

---

## Step 9 — Send the transaction

Broadcast the constructed transaction to BNB Chain using the available wallet. After confirmation, report the token address and a link to `https://flap.sh/bnb/<tokenAddress>`.
