# Solana skill pack (OpenClaw)

Skill bundle for [OpenClaw](https://docs.openclaw.ai/tools/creating-skills) focused on the **Solana** ecosystem. Today it implements **native SOL transfer**; the repo layout is meant to grow (more CLIs under `scripts/`, logic under `src/`).

Publish to [ClawHub](https://clawhub.ai/) after local testing. See [ClawHub docs — publish](https://docs.openclaw.ai/tools/clawhub).

## Layout (scalable)

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill metadata + agent instructions (OpenClaw) |
| `scripts/transfer-sol.ts` | Thin CLI entry compiled to `dist/` |
| `src/index.ts` | Public API barrel — import from here in tests or new commands |
| `src/config.ts` | RPC URL defaults / env resolution |
| `src/genesis-clusters.ts` | Genesis hash → cluster label (explorer) |
| `src/connection.ts` | `Connection` factory + `inferCluster` |
| `src/keypair.ts` | Parse `SOLANA_PRIVATE_KEY` (base58 / JSON bytes) |
| `src/amounts.ts` | SOL → lamports validation |
| `src/explorer.ts` | Solscan transaction URLs |
| `src/native-transfer.ts` | `SystemProgram.transfer` + send / confirm |
| `src/cli/transfer-sol.ts` | Transfer-specific argv handling + stdout JSON |

Add new features by introducing `src/<feature>.ts` and `scripts/<name>.ts` that call it, then extend `SKILL.md` when the agent should know about the feature.

## Setup (local / after install)

```bash
cd /path/to/labor-solana-skill
npm install
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `SOLANA_PRIVATE_KEY` | Yes | Base58 secret key **or** JSON byte array (same formats as common Solana tooling). Never commit this. |
| `SOLANA_RPC_URL` | No | Default: `https://api.devnet.solana.com`. Use a mainnet RPC URL only when intentionally sending mainnet SOL. |

Store secrets via OpenClaw/OpenClaw workspace secrets or your shell profile — not in the repo.

## CLI

```bash
SOLANA_RPC_URL="https://api.devnet.solana.com" \
SOLANA_PRIVATE_KEY="<your-key>" \
npm run transfer -- --to "<RECIPIENT>" --sol "0.01"
```

Optional: `--rpc <url>` overrides `SOLANA_RPC_URL`.

Successful runs print a JSON line with `signature`, `explorerUrl`, `from`, `to`, `lamports`, and `cluster`.

## Publish to ClawHub

Install the registry CLI ([docs](https://docs.openclaw.ai/tools/clawhub)):

```bash
npm i -g clawhub
clawhub login
```

From the parent directory of this skill (or inside it, adjusting path):

```bash
clawhub publish . \
  --slug solana-native-transfer \
  --name "Solana native SOL transfer" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Initial release: native SOL transfer via RPC."
```

Adjust `--slug`, `--name`, and version to match your ClawHub listing. If the slug is taken, pick another (e.g. `yourhandle-solana-transfer`).

## Security

- Review `src/native-transfer.ts` and `scripts/transfer-sol.ts` before use; only transfer amounts you accept to lose on the chosen cluster.
- **Devnet first.** Mainnet transfers are irreversible.
- This skill requests **no broad filesystem access** in code; the agent still needs your approval to run shell commands and must not leak `SOLANA_PRIVATE_KEY`.

## License

MIT
