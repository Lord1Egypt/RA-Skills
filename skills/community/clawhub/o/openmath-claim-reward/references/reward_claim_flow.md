# OpenMath Reward Claim Reference

Requires trusted local `python3` and `shentud` on `PATH`. Queries use the local `shentud` CLI plus a Shentu RPC endpoint. Withdrawals additionally rely on the local OS keyring through `shentud --keyring-backend os`, so confirm the key name, resolved address, and node URL before broadcasting.

## Query Rewards First
Reward claiming is address-based, not theorem-based. Always query the address first:

```bash
shentud q bounty rewards <address> --node <shentu_node_url>
```

If the address is not provided explicitly, prefer auto-discovering `prover_address` from:

- `--config <path>` when passed to the helper script
- `OPENMATH_ENV_CONFIG` when set
- `./.openmath-skills/openmath-env.json`
- `~/.openmath-skills/openmath-env.json`

If neither config contains `prover_address`, stop and follow `references/init-setup.md`.

If you want to force a specific config file for the helper script, set `OPENMATH_ENV_CONFIG=/path/to/openmath-env.json` or pass `--config /path/to/openmath-env.json`.

Use `SHENTU_NODE_URL` or the built-in default. Example (mainnet):

```bash
shentud q bounty rewards <address> --node https://rpc.shentu.org:443
```

Possible response:

```yaml
imported_rewards:
- amount: "980000.000000000000000000"
  denom: uctk
proof_rewards:
- amount: "123252300.000000000000000000"
  denom: uctk
```

## Reward Buckets
- `imported_rewards`: Rewards earned because a theorem you created was imported or referenced by other theorems.
- `proof_rewards`: Rewards earned because you submitted proofs that passed verification.
- An address may have only `imported_rewards`, only `proof_rewards`, or both.
- If both buckets exist, one `withdraw-rewards` transaction withdraws both together.
- If the chain later returns `no rewards found`, that means the address currently has no claimable rewards left.

## Recommended Withdrawal Flow
1. Query `bounty rewards` for the address.
2. If either reward bucket is non-empty, make sure a local `os` keyring key controls the same address:

```bash
shentud keys list --keyring-backend os
shentud keys show <key-name> -a --keyring-backend os
```

If no local key matches the reward address, stop and recover/import that wallet before continuing.

3. Broadcast:

```bash
shentud tx bounty withdraw-rewards --from <key-name> --keyring-backend os --chain-id <shentu_chain_id> --node <shentu_node_url> --gas-prices 0.025uctk --gas-adjustment 2.0 --gas auto
```

Use `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL` or the built-in defaults. Mainnet defaults: `--chain-id shentu-2.2 --node https://rpc.shentu.org:443`.

4. Wait about `5-10` seconds for block inclusion.
5. Query the tx receipt:

```bash
shentud q tx <txhash> --node <shentu_node_url>
```

6. Query `bounty rewards` again for the same address.
7. Treat either of these as a successful empty post-withdraw state:
- `imported_rewards: []` and `proof_rewards: []`
- RPC returns `no rewards found for address ...`

## Practical Notes
- Rewards are withdrawn per address, so there is no need to specify theorem ID or proof ID when claiming.
- For local signing consistency, always include `--keyring-backend os` in the withdraw command.
- Before withdrawal, verify that `shentud keys show <key-name> -a --keyring-backend os` resolves to the same reward address you queried.
- Do not create a new random local key for withdrawal unless it controls the same reward address.
- The current Shentu flow requires explicit gas settings to avoid broadcast failures:
  `--gas-prices 0.025uctk --gas-adjustment 2.0 --gas auto`
- The helper script `python3 scripts/query_reward_status.py rewards [address]` already treats `no rewards found` as zero claimable rewards, and can auto-discover `prover_address` from `OPENMATH_ENV_CONFIG` or the standard `openmath-env.json` locations.
