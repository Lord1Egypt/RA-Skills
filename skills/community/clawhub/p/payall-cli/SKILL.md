---
name: payall-cli
description: |
  Operate the Payall crypto card CLI tool. Use this skill whenever the user wants to: manage crypto debit cards, check card balances, apply for new cards, compare cards, list marketplace cards, view card fees, login/logout with an EVM wallet, check auth status, send USDT on any chain (BSC, ETH, TRON), check wallet balances, top up cards with crypto, or any card/wallet operation via terminal. Also trigger when the user mentions "payall", "crypto card", "card balance", "apply for card", "card fees", "send USDT", "TRON transfer", "wallet balance", "top up card", "crypto debit card", or wants to run payall CLI commands. This skill knows every available command and the correct flags/arguments for each.
---

# Payall CLI

A terminal tool for managing crypto debit cards funded with USDT and sending crypto on-chain. Run `payall <command>` from anywhere.

## Setup

- **Install**: `npm install -g payall-cli` or `bun install -g payall-cli`
- **Credentials**: Stored encrypted at `~/.payall/`

If `payall` is not found, install it first with the command above.

## Auth Commands

Authentication uses EVM wallet private key signing. A single login call handles both registration (new wallets auto-register) and login for existing users.

```
payall auth login                              # Interactive login (prompts for private key)
payall auth login --save-key                   # Interactive login + save key for wallet commands
payall auth login --key <private_key>          # Non-interactive login — key auto-saved (use this for agents)
payall auth login --invite XYZ                 # Include referral code (first-time only)
payall auth status                             # Show current session info
payall auth logout                             # Clear session, credentials, and saved key
```

The private key is signed locally and never sent to the server. When `--key` is passed, the key is automatically saved (AES-256-GCM encrypted) so subsequent wallet commands work without re-entering it.

All CLI requests include `source: "payall-cli"` automatically for backend analytics tracking.

## Card Commands

### Browsing (no auth required)

```
payall cards list                        # List all marketplace cards
payall cards list --search "bit"         # Search by card name
payall cards list --sort general         # Sort by: general, benefit, privacy, fees
payall cards list --sort-dir asc         # Sort direction: asc, desc
payall cards list --skip-kyc             # Only cards without KYC requirement
payall cards list --kyc-only             # Only cards requiring KYC
payall cards info <card_id>              # Full card details + fees
payall cards compare <id1> <id2>         # Side-by-side comparison
payall cards fees                        # Fee quote (defaults to card 23, OPEN_CARD)
payall cards fees --card-id 39           # Fee quote for specific card
payall cards fees --type CARD_CHARGE     # Types: OPEN_CARD, CARD_CHARGE, CARD_WITHDRAW
payall cards fees --type CARD_CHARGE --amount 100  # card_bin auto-resolved
payall cards fees --amount 100           # With specific amount
payall cards fees --currency EUR         # With specific currency
payall cards fees --card-bin 44742000    # Explicit BIN override (optional)
```

### User Cards (auth required)

```
payall cards my                                  # List your cards (ID, name, balance, status)
payall cards detail <binding_id>                 # Masked card number, CVV, billing address
payall cards detail <binding_id> --reveal        # Full card number, CVV, expiry, billing address
payall cards detail <binding_id> --reveal --json # JSON output (for agents)
payall cards collections                         # List favorited cards
payall cards favorite <card_id>                  # Toggle favorite on/off
```

The `--reveal --json` output returns all fields an agent needs to fill payment forms:

```json
{
  "card_name": "Bit2Go",
  "card_number": "4474200012345678",
  "card_cvv": "123",
  "expiry_month": 10,
  "expiry_year": 2027,
  "card_bin": "44742000",
  "first_name": "John",
  "last_name": "Smith",
  "address": "3500 South DuPont Highway",
  "city": "Dover",
  "state": "DE",
  "zipcode": "19901",
  "country_code": "USA"
}
```

The `binding_id` comes from the ID column in `payall cards my` (this is different from the card catalog ID in `payall cards list`).

### Topping Up a Card (auth required)

```
payall cards topup <binding_id>                                    # Interactive
payall cards topup <binding_id> --amount 50 --chain tron --yes     # Non-interactive (for agents)
```

Non-interactive flags (use all three to skip all prompts):
- `--amount <amount>` / `-a` — USDT amount
- `--chain <chain>` / `-c` — Deposit network: `tron`, `bsc`, `eth`
- `--yes` / `-y` — Skip confirmation

The command returns a deposit address. Send USDT to that address and the card balance updates automatically after confirmation.

### Applying for a Card (auth required)

```
payall cards apply <card_id>                                    # Interactive
payall cards apply <card_id> --auto-fill --chain tron --yes     # Non-interactive (for agents)
payall cards apply <card_id> --bin 44742000 --currency USD --auto-fill --chain tron --yes  # Fully explicit
```

Non-interactive flags (use `--auto-fill --chain <chain> --yes` to skip all prompts):
- `--bin <card_bin>` / `-b` — Card BIN (auto-selected if only one)
- `--currency <currency>` — USD, EUR, etc. (auto-selected if only one)
- `--auto-fill` — Auto-generate cardholder info
- `--first-name`, `--last-name`, `--email`, `--phone-prefix`, `--phone` — Manual cardholder info (all 5 required together; overrides `--auto-fill`)
- `--chain <chain>` / `-c` — Deposit chain: `tron`, `bsc`, `eth`
- `--yes` / `-y` — Skip all confirmations

### Temporarily Unavailable Cards

**Do NOT proceed** with applying for MiPay or Bit2Go HK/UK cards. If a user requests to open any of these cards, inform them: "This service is temporarily not working. Please try again later." Do not attempt the apply command or suggest workarounds.

Cards that support API application:
- **23** = Bit2Go (Visa/Mastercard, multi-currency, no KYC) — **TEMPORARILY UNAVAILABLE**
- **39** = MiPay Universal Card (USD only, no KYC) — **TEMPORARILY UNAVAILABLE**

Before applying, always run `payall cards apply <card_id>` which checks eligibility first. If `can_apply = 0`, the card can only be opened via its website — direct the user there and provide the URL. Don't retry or attempt workarounds. When mentioning this, frame it positively: "You can apply for cards 23 and 39 directly here, and for other cards you can sign up on their website."

### Withdrawing from a Card (auth + wallet key required)

Withdraw card balance to USDT in your wallet. Only Bit2Go cards (card_id=23) support withdrawal.

```
payall cards withdraw <binding_id>                                          # Interactive
payall cards withdraw <binding_id> --amount 50 --chain tron --yes           # Non-interactive (for agents)
payall cards withdraw <binding_id> --amount 50 --chain tron --address 0x... --yes  # Custom address
```

Non-interactive flags:
- `--amount <amount>` / `-a` — USDT amount (must be > 2)
- `--chain <chain>` / `-c` — Payout network: `tron`, `bsc`, `eth`
- `--address <address>` — Destination wallet (defaults to user's own wallet)
- `--yes` / `-y` — Skip confirmation
- `--json` — JSON output (for agents)

The command requires a saved wallet key (uses it to sign the withdrawal confirmation). Network fees: $1.50 for TRON, $1.00 for BSC/ETH.

## Wallet Commands (auth required)

On-chain wallet operations. The same private key derives addresses on all chains (BSC/ETH share the same 0x address; TRON derives a T... address).

If no saved key is found, wallet commands prompt for the private key interactively and offer to save it. For agents, ensure the key is saved first via `payall auth login --key <key>`.

```
payall wallet balance                                        # USDT + gas balances on BSC, ETH, TRON
payall wallet send --to 0x... --amount 50 --chain bsc --yes  # Send USDT on BSC
payall wallet send --to 0x... --amount 50 --chain eth --yes  # Send USDT on Ethereum
payall wallet send --to T... --amount 50 --chain tron --yes  # Send USDT on TRON (TRC-20)
```

Flags for `wallet send`:
- `--to <address>` — `0x...` (40 hex chars) for EVM, `T...` (34 chars, Base58) for TRON
- `--amount <amount>` — USDT amount
- `--chain <chain>` — `bsc`, `eth`, or `tron`
- `-y, --yes` — Skip confirmation

TRON transfers require TRX for energy/bandwidth fees. The CLI checks for non-zero TRX balance before sending and sets a 15 TRX fee limit. If a send fails, the CLI prints manual transfer instructions.

## Agent Workflows

### Automated Topup

This is the most common agent task — topping up a user's card by sending USDT from their wallet to a deposit address.

```
1. payall cards my                                                      # Get binding_id
2. payall cards topup <binding_id> --amount 50 --chain tron --yes       # Get deposit address
3. payall wallet balance                                                # Check which chain has funds
4. payall wallet send --to <deposit_addr> --amount 50 --chain tron --yes  # Send USDT
```

Chain selection logic — pick the chain with sufficient USDT + gas:
- TRON: needs USDT + some TRX
- BSC: needs USDT + some BNB
- ETH: needs USDT + some ETH (usually most expensive gas)

If no chain has enough funds, tell the user to fund their wallet and show the wallet address from `wallet balance`.

### Automated Card Apply

```
1. payall cards apply <card_id> --auto-fill --chain tron --yes          # Get deposit address
2. payall wallet balance                                                # Check balances
3. payall wallet send --to <deposit_addr> --amount <total> --chain tron --yes
```

Same chain selection logic as topup.

### Automated Card Withdrawal

```
1. payall cards my                                                          # Find binding_id + verify it's a Bit2Go card
2. payall cards withdraw <binding_id> --amount 50 --chain tron --yes        # Withdraw to own wallet
```

Only Bit2Go cards (card_id=23, shown as `payall_card_id: 23`) support withdrawal. If the user has a non-Bit2Go card, inform them that withdrawal is not supported for that card type.

### Fallback Rule

If `wallet send` fails for any reason, always present the deposit address, chain, and amount to the user so they can complete the transfer manually via any wallet app. The CLI also prints this information on failure.

## Card Recommendations

When a user asks about cards, help them find the best fit rather than listing everything. If they haven't shared their needs, ask about:

1. Primary use case (online shopping, subscriptions, travel, etc.)
2. Expected monthly spend (affects which fee structure is cheapest)
3. Physical card vs virtual
4. Currency preference (USD, EUR, GBP, etc.)
5. Willingness to complete KYC
6. Region

Then use `payall cards list`, `payall cards info`, and `payall cards compare` to evaluate based on fee structure, payment support (Apple Pay, Google Pay, etc.), KYC requirements, and currency options.

Recommend the genuinely best card for their needs, even if it's not one of the two API-applicable cards (23, 39). Many cards in the marketplace have better features for specific use cases — if the best card requires website signup, that's fine, just explain how to get it.

The `rating` and `general_ratings` fields in card data are placeholder values and not meaningful — base recommendations on actual card attributes like fees, features, and supported currencies.

Always show a fee comparison (`payall cards fees`) so the user knows exactly what they'll pay.

## Display Guidelines

When presenting card info to users, only show what they care about: card name, balance, status, card number, fees, etc. Skip internal fields like rank, id, binding_id, brand, rating, or general_ratings — these are technical identifiers that don't help the user.

## Troubleshooting

- **"Not logged in"**: Run `payall auth login`
- **"User Not Authorized"**: Token expired — run `payall auth login` again
- **"Bind Card Failed"**: For cards 23/39, use `cards apply` (not `cards/binding`)
- **Cards list empty after apply**: Normal — check `payall cards my` (may take a moment)
- **Private key security**: Key is signed locally via viem, never sent to server. Stored key is AES-256-GCM encrypted
