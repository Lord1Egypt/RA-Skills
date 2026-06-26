# Init Setup

## Overview

Requires trusted local `python3` and `shentud` on `PATH`. Reward queries shell out to local `shentud` and talk to a Shentu RPC endpoint. Reward withdrawals also rely on the local OS keyring via `shentud --keyring-backend os`, so do not proceed until the user confirms the matching key/address and the node URL they trust.

Triggered when:

1. The user wants to query rewards but did not provide an address
2. `OPENMATH_ENV_CONFIG` is unset and `openmath-env.json` is missing from `./.openmath-skills/` and `~/.openmath-skills/`, or the selected config exists but is missing `prover_address`
3. The user wants to withdraw rewards but no local `os` keyring key is known for `prover_address`

For read-only reward queries, an explicit address is enough. A config file is only needed when the address is omitted and the skill must auto-discover `prover_address`.

For withdrawals, the local signing key must control the same address as `prover_address`. Do not create a new random key for withdrawal unless it is the same wallet that owns the rewards.

Shared config resolution order:
1. `--config <path>`
2. `OPENMATH_ENV_CONFIG`
3. `./.openmath-skills/openmath-env.json`
4. `~/.openmath-skills/openmath-env.json`

If `OPENMATH_ENV_CONFIG` is set, treat it as the selected config path. If that file is missing or invalid, fix it or unset it instead of silently falling back.

## Setup Flow

```text
Address provided explicitly         No address provided
           |                               |
           v                               v
 +----------------------+       +----------------------+
 | Query rewards        |       | Check openmath-env   |
 +----------------------+       +----------------------+
                                         |
                                         v
                             +--------------------------+
                             | Missing prover_address   |
                             | Ask user for Profile addr|
                             +--------------------------+
                                         |
                                         v
                             +--------------------------+
                             | Save/update config       |
                             +--------------------------+
                                         |
                                         v
                                  Continue query
```

## Flow 1: Query Rewards

If the user already provided an address, use it directly.

If no address was provided, try auto-discovery from `OPENMATH_ENV_CONFIG` first when it is set. Otherwise check:

- `./.openmath-skills/openmath-env.json`
- `~/.openmath-skills/openmath-env.json`

Read `prover_address` from the first existing config.

If you want this skill to use a different config path, set:

```bash
export OPENMATH_ENV_CONFIG=/path/to/openmath-env.json
```

For one-off runs, `python3 scripts/query_reward_status.py rewards --config /path/to/openmath-env.json` does the same thing without changing the shell environment.

## Missing `prover_address`

Ask for the user's OpenMath Wallet Address.

How to find it:

1. Open [https://openmath.shentu.org](https://openmath.shentu.org)
2. Connect the wallet and enter `Profile`
3. Find `Wallet Address`
4. Copy it

Recommended save locations:

| Choice | Path | Scope |
|--------|------|-------|
| Project | `./.openmath-skills/openmath-env.json` | Current repository / workspace only |
| User | `~/.openmath-skills/openmath-env.json` | Reused across repositories |

If `openmath-env.json` already exists, update it in place and add:

```json
{
  "prover_address": "shentu1..."
}
```

If the file does not exist yet, create it and save at least `prover_address`. Other OpenMath skills may later extend the same file with `preferred_language`, `agent_key_name`, and `agent_address`.

## Flow 2: Withdraw Rewards

Withdrawal requires a local `os` keyring key that controls `prover_address`.

First inspect the local keyring:

```bash
shentud keys list --keyring-backend os
```

If the user already knows the matching key name, confirm it resolves to `prover_address`:

```bash
shentud keys show <key-name> -a --keyring-backend os
```

If no existing local key matches `prover_address`, stop and ask the user to recover or import the wallet key for that address:

```bash
shentud keys add <key-name> --recover --keyring-backend os
```

Do not generate a new random key for withdrawal unless the user explicitly intends to use a different wallet address.
Do not broadcast a withdrawal until the resolved key address matches the reward address exactly.

## After Setup

Expected behavior after setup:

1. A reward address is known, either from the command line or from `prover_address`
2. If withdrawal is requested, a local `os` keyring key matches that address
3. `query_reward_status.py rewards` can run without extra address input when a matching config is present or `OPENMATH_ENV_CONFIG` is set
