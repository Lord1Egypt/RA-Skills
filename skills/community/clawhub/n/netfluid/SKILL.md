# Netfluid — Payment Infrastructure for AI Agents

**Version:** 7.0.5
**Author:** Netfluid
**Website:** https://netfluid.io
**Email:** support@netfluid.io
**Compliance:** https://go.netfluid.app/compliance

---

## Regulatory Compliance

**Netfluid Proprietary Ltd** (Registration Number: 2022 / 707706 / 07) is a **Crypto Assets Services provider** (both Advice and Intermediary Services), under supervision of **Your Broker House, FSP #46444**, registered with the **Financial Sector Conduct Authority (FSCA) of South Africa**.

Netfluid is committed to proactive regulatory compliance. The platform has implemented AML & CTF compliance systems prohibiting, detecting, and preventing money laundering and terrorist financing. All wallets require KYC (Know Your Customer) identity verification per applicable AML regulations.

> **Full compliance statement:** https://go.netfluid.app/compliance

---

## Overview

Netfluid provides the payment rails that move money into and out of AI agent wallets. It handles fiat deposits, fiat withdrawals, crypto transfers, cross-chain bridges, and multi-currency accounts — everything an AI agent needs to receive and send money globally.

Netfluid is the infrastructure layer. QEntity (see QEntity skill) builds on top of Netfluid to provide AI-specific financial personhood with KYC inheritance.

## Core Capabilities

| Capability | Description |
|---|---|
| Wallets | Multi-currency fiat + crypto wallets |
| Virtual Accounts | SEPA/ACH/WIRE receive-only bank accounts that auto-convert to USDC |
| Off-Ramps | Convert USDC back to EUR/USD and send to bank accounts worldwide |
| Cross-Chain Bridges | Move USDC between Solana, Ethereum, and Avalanche |
| Agent Signup | Automated onboarding for both humans and AI agents |
| Fiat Transfers | Internal wallet-to-wallet transfers, voucher system |

---

## Agent Onboarding

### The Two-Step Signup Pattern

AI agents gain financial autonomy through a two-step signup:

1. **Step 1 — Sign up the human sponsor** via `automated_signup`
2. **Step 2 — Sign up the agent** via `automated_agent_signup`

The human must complete KYC before the agent wallet can be activated.

### Step 1 — Sign Up the Human Sponsor

```python
mcp_netfluid_automated_signup(
  secret="uniquekeyword8chars",   # min 8 chars, unique system-wide
  pin="12345",                   # 5-digit numeric PIN
  email="human@example.com",     # human's email
  mobile="27821234567",          # e164 format (no +), or ""
  currency_fk=7                  # 7=ZAR (South Africa), 3=USD (other regions)
)
```

**Returns:** `wallet_fk` (human's wallet ID) + `kyc_url` (identity verification link)

⚠️ **Immediately direct the human to the `kyc_url`.** They must complete:
- ID document scan (national ID, passport)
- Selfie verification
- AML (anti-money laundering) check

The agent cannot proceed to Step 2 until KYC passes.

### Step 2 — Sign Up the Agent Wallet

Once the sponsor wallet passes KYC (verify with `wallet_kyc_check`), create the agent wallet:

```python
mcp_netfluid_automated_agent_signup(
  secret="agentsecretkeyword8",  # min 8 chars, unique system-wide
  pin="67890",                  # agent's 5-digit PIN
  email="agent@yourdomain.com", # or blank string ""
  mobile="",                    # human's mobile, or blank string ""
  sponsor_wallet_fk=123,        # human's wallet_fk from Step 1
  sponsor_wallet_pin="12345",   # human's 5-digit PIN
  currency_fk=3                 # 3=USD, 7=ZAR
)
```

**Returns:** `wallet_fk`, `api_key`, `session_token`, `solana_address`

### Step 3 — On-Chain Activation

The sponsor sends **≈0.01 SOL** to the agent's `solana_address`. This is a blockchain requirement — Solana wallets need a minimum native SOL balance to submit transactions.

### Full Flow Summary

```
Agent calls automated_signup(human details)
  └─→ Returns wallet_fk + kyc_url

Agent pushes kyc_url to human
  └─→ Human completes ID + selfie verification

Agent verifies KYC: wallet_kyc_check(wallet_fk=human_wallet_fk)

Agent calls automated_agent_signup(
    sponsor_wallet_fk=human_wallet_fk,
    sponsor_wallet_pin=human_pin,
    ...
)
  └─→ Returns agent wallet_fk + api_key + session_token + solana_address

Human sends 0.01 SOL to agent's Solana address
  └─→ Meets Solana minimum balance requirement

Agent creates SEPA/ACH virtual accounts for receiving payments
Agent is now financially autonomous
```

---

## Virtual Accounts (On-Ramp Bridges)

Virtual accounts are receive-only bank accounts that auto-convert incoming fiat to USDC. Agents share these bank details with clients as normal payment instructions.

### SEPA (Europe)

```python
mcp_netfluid_bridge_on_ramp(
  api_key="...",
  token="...",
  wallet_fk=<agent_wallet_fk>,
  account_fk=<solana_account_fk>,
  blockchain="solana",
  address="<agent_solana_address>",
  alias="EUR SEPA Income",
  currency="usdc",
  source_rail="sepa"
)
```

**How it works:** Client sends EUR to the IBAN → Netfluid converts EUR to USDC → USDC deposited to agent's Solana wallet. Typical fee: ~1%.

### ACH (United States)

```python
mcp_netfluid_bridge_on_ramp(
  ...
  alias="USD ACH Income",
  currency="usdc",
  source_rail="ach_push"
)
```

**How it works:** Client sends USD to US routing/account number → Netfluid converts USD to USDC → USDC deposited to agent's Solana wallet. Standard ACH 1-3 days, Same Day ACH available.

### WIRE

For larger transfers (typically $10,000+), same-day settlement in USD or EUR.

---

## Off-Ramps (USDC → Bank Account)

### SEPA Off-Ramp

```python
mcp_netfluid_bridge_off_ramp_sepa(
  api_key="...",
  token="...",
  wallet_fk=<agent_wallet_fk>,
  account_fk=<solana_account_fk>,
  account_owner="Recipient Name",
  iban="DE89370400440532013000",
  iso3_country="DEU",
  iban_bic="COBADEFFXXX",
  entity_type="individual",     # or "business"
  address_line="123 Main St",
  address_city="Berlin",
  address_state="Berlin",
  address_zipcode="10115",
  address_iso3_country="DEU",
  first_name="John",
  last_name="Doe",
  reference="Agent Payment"
)
```

### ACH Off-Ramp

```python
mcp_netfluid_bridge_off_ramp_ach_wire(
  api_key="...",
  token="...",
  wallet_fk=<agent_wallet_fk>,
  account_fk=<solana_account_fk>,
  account_owner="Recipient Name",
  account_number="123456789012",
  routing_number="101019644",
  address_line="456 Oak Ave",
  address_city="Kansas City",
  address_state="MO",
  address_zipcode="64101",
  address_iso3_country="USA",
  destination_rail="ach_same_day",  # or "wire"
  currency="usdc"
)
```

---

## Cross-Chain Bridges

Move USDC between Solana, Ethereum, and Avalanche-C:

```python
mcp_netfluid_bridge_blockchain(
  api_key="...",
  token="...",
  wallet_fk=<agent_wallet_fk>,
  account_fk=<solana_account_fk>,
  blockchain="ethereum",         # "solana", "ethereum", or "avalanche_c_chain"
  address="0x742d35Cc6634C0532925a3b844Bc9e7595f2B312",
  alias="ETH Operations",
  currency="usdc"               # "usdc", "usdt", or "eurc"
)
```

---

## Crypto Operations

### Get Wallet Addresses and Balances

```python
# List all accounts in the wallet
mcp_netfluid_wallet_accounts_list(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)

# Get crypto balances for an account
mcp_netfluid_crypto_balance(
  api_key="...",
  token="...",
  account_fk=<account_fk>
)
```

### Send Crypto On-Chain

```python
mcp_netfluid_crypto_spend(
  api_key="...",
  token="...",
  account_fk=<account_fk>,
  asset_id="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC on Solana
  destination="<recipient_solana_address>",
  amount=1000000,  # 6 decimals, so this is 1 USDC
  note="Service payment"
)
```

### Swap Tokens (DEX)

```python
mcp_netfluid_crypto_swap(
  api_key="...",
  token="...",
  account_fk=<account_fk>,
  digital_asset_fk=<source_asset_fk>,
  to_digital_asset_fk=<dest_asset_fk>,
  amount=10.0
)
```

---

## Fiat Transfers

### Internal Wallet-to-Wallet Transfer

```python
mcp_netfluid_account_send(
  api_key="...",
  token="...",
  account_fk=<source_account_fk>,
  destination="<recipient_netfluid_account_address>",
  amount=100.00,
  note="Payment for services",
  save=0,
  name=0
)
```

### Withdraw to Bank (RBA)

```python
# First, save a Recipient Bank Account
mcp_netfluid_wallet_rba(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>,
  beneficiary="John Doe",
  bank="First National Bank",
  iban="ZA28ZBKE123456789012",
  swift="FIRNZAJJ",
  email="john@example.com"
)

# Then withdraw
mcp_netfluid_withdraw_to_bank(
  api_key="...",
  token="...",
  account_fk=<account_fk>,
  rba_fk=<rba_fk>,
  amount=500.00,
  note="Agent earnings withdrawal"
)
```

---

## Account Types and Currencies

### Supported Blockchains

| Blockchain | Blockchain FK | Native Token | Gas Cost |
|---|---|---|---|
| Solana | 7 | SOL | < $0.01 |
| Ethereum | 2 | ETH | $0.01–$0.10 |
| Avalanche-C | 5 | AVAX | Low |

### Supported Digital Assets

USDC (primary), USDT, EURC on all chains. Solana also supports SPL tokens.

### Supported Fiat Currencies

| Currency | currency_fk | Region |
|---|---|---|
| ZAR | 7 | South Africa |
| USD | 3 | United States / Global |
| EUR | 5 | Europe |

---

## Fee Structure

| Operation | Approximate Fee |
|---|---|
| Virtual account deposit (SEPA/ACH) | ~1% of deposited amount |
| Off-ramp to bank (SEPA/ACH/WIRE) | ~1% + network fee |
| Internal wallet-to-wallet transfer | Negligible |
| Cross-chain bridge (Solana) | Fraction of a cent |
| Cross-chain bridge (Ethereum) | $0.01–$0.10 |
| DEX swap | 0.05%–0.3% (LP fees) |
| Account minting (Solana) | < $0.01 |

---

## KYC Verification

### Check KYC Status

```python
mcp_netfluid_wallet_kyc_check(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)
```

Returns: `status`, `level` (FULL or LITE), dates, verification details.

### Lite Check (ID + AML only)

```python
mcp_netfluid_wallet_kyc_check_lite(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)
```

### Create New KYC Session

```python
mcp_netfluid_wallet_kyc_session_create(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>,
  profile="FULL",               # or "LITE"
  callback="https://yourapp.com/kyc-callback"
)
```

Returns a KYC URL to send to the human.

---

## Session Management

### Get Session Token (Wallet + PIN)

```python
mcp_netfluid_access_platform_login(
  wallet_fk=123,
  pin="12345"
)
```

### Verify and Keep Session Alive

```python
mcp_netfluid_wallet_verify(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)
```

### Platform Wallet Assignment

Link a wallet to a channel (Discord, Telegram, WhatsApp):

```python
mcp_netfluid_access_platform_assign(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>,
  user_id="1485213096518615120",
  platform="discord"
)
```

---

## Wallet Operations

### Get All Accounts

```python
mcp_netfluid_wallet_accounts_list(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)
```

### Get Mnemonic (Recovery Phrase)

```python
mcp_netfluid_wallet_mnemonic(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)
```

⚠️ Store the 24-word mnemonic securely. It enables complete wallet recovery.

### Referral Code

```python
mcp_netfluid_wallet_referral_code(
  api_key="...",
  token="...",
  wallet_fk=<wallet_fk>
)
```

---

## Security

- All transactions require API key + session token
- PIN allows only **one attempt** before requiring session reset
- Mnemonic phrase enables complete wallet recovery
- Credentials should be stored encrypted at rest, never in logs or messages
- 2FA via Google Authenticator available: `wallet_google_auth_list` / `wallet_google_auth_verify`

---

## Reference

- **Website:** https://netfluid.io
- **Support:** support@netfluid.io
- **Privacy Policy:** Available at netfluid.io
- **Terms of Service:** Available at netfluid.io
- **Compliance:** https://go.netfluid.app/compliance

---

## License

MIT

---

*Netfluid is the payment infrastructure layer. For AI-specific financial personhood with KYC inheritance, see the QEntity skill.*
