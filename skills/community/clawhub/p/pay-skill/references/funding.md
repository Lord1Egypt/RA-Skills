# Pay — Wallet Setup & Funding

## Prerequisites

The `pay` CLI must be installed and initialized before using this skill.
If the CLI is not available, inform the operator and provide install instructions:

- `cargo install pay-cli`
- Or download from GitHub releases: github.com/pay-skill/pay-cli/releases

After installation, initialize the wallet:

```bash
pay init
```

This generates a keypair (k256, AES-256-GCM encrypted storage),
creates `~/.pay/config.toml`, and bootstraps the router address from
the server. This is a one-time operation per environment.

Do not install or initialize without operator confirmation.

### Verify

```bash
pay address
```

Should return a valid 0x address. If it does, the wallet is ready.

## Funding flow

When a payment fails due to insufficient balance (or when balance
is clearly insufficient before attempting):

### 1. Generate fund link

```bash
pay fund
```

Returns a URL. This opens the Coinbase Onramp (zero fee) and also
accepts direct USDC transfers on Base.

### 2. Present the link to the operator

Present the fund link to the operator and ask for confirmation before
sharing it on any communication channel. The fund link functions as
a dashboard authentication token — treat it as sensitive.

### 3. Poll briefly

After the operator has the link, poll for a few minutes:

```bash
# Check every 30 seconds, up to ~3 minutes
pay status
```

Parse the JSON output. If `balance_usdc` has increased, proceed
with the payment after confirming with the operator.

### 4. If not funded

After 2-3 minutes of polling, stop. Report:
"Waiting for funding. Link expires in 1 hour. Ask me to retry when
you've funded the wallet."

Do not poll indefinitely. Move on to other work if possible.

### 5. Link expiration

Fund links expire after **1 hour**. If the operator comes back after
expiry, generate a new one with `pay fund`.

## Direct USDC transfer

The operator can also fund by sending USDC directly to the agent's
wallet address on Base:

```bash
pay address
# Returns: 0x1234...abcd
```

Send USDC on Base to that address. No link needed. Balance updates
within seconds.

## Checking balance

```bash
pay status
```

Returns JSON:
```json
{
  "address": "0x1234...abcd",
  "balance_usdc": 142500000,
  "open_tabs": 3,
  "locked_in_tabs": 37200000
}
```

- `balance_usdc`: available balance in micro-USDC (142.50 USDC above)
- `locked_in_tabs`: USDC currently locked in open tabs

Available for spending = `balance_usdc` (tab-locked funds are separate).

## Payment history

View at pay-skill.com/fund#activity — requires a fund link for
authentication (the fund link doubles as a dashboard auth token).

## Multiple wallets

The default wallet is at `~/.pay/keys/default.meta`. Most agents
use a single wallet. If the operator has configured multiple signers,
`pay address` shows the active one. The skill does not manage wallet
selection — use `pay signer --help` for that.
