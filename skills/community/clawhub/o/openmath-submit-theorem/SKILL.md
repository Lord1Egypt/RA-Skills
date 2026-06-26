---
name: openmath-submit-theorem
description: Submits proofs to the OpenMath platform using a two-stage commit-reveal flow. Use when the user wants to commit a proof hash or reveal a Lean/Rocq proof on the Shentu network.
version: v1.0.7
requirements:
  commands:
    - python3
    - shentud
side_effects:
  - Reads shared openmath-env.json from --config, OPENMATH_ENV_CONFIG, or the standard project/user config locations
  - Queries and broadcasts to a remote Shentu RPC endpoint; defaults to https://rpc.shentu.org:443 unless SHENTU_NODE_URL overrides it
  - Uses the local OS keyring through shentud --keyring-backend os for key lookups and authz-exec signing
  - Reads PATH and optional OPENMATH_SHENTUD_BIN to discover shentud; may suggest a temporary PATH export or a trusted explicit binary path, but does not install binaries or edit shell startup files
  - Default flow treats openmath-env.json creation or editing, shentud installation, and local key creation or recovery as manual setup steps documented in references
---

# OpenMath Submit Theorem

## Instructions

Use this skill for the two-stage Shentu proof submission flow. 

- Stage 1 submits a proof hash as a commitment so others can see you already know the answer without learning the proof details.
- Stage 2 submits the proof detail to reveal and verify the same proof on-chain.
- This is an operational skill, not an instruction-only note: it shells out to trusted local `python3` and `shentud`, reads shared `openmath-env.json`, queries/broadcasts to a Shentu RPC endpoint, and uses the local OS keyring for signing flows.
- Default: authz + feegrant from `prover_address` (the user's OpenMath Wallet Address).
- Shared config resolution order: `--config <path>` → `OPENMATH_ENV_CONFIG` → `./.openmath-skills/openmath-env.json` → `~/.openmath-skills/openmath-env.json`. If `OPENMATH_ENV_CONFIG` is set, treat it as the selected config path. If that file is missing or invalid, stop and fix it instead of silently falling back.
- Shentu chain/RPC settings come from `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL` or built-in defaults, not from `openmath-env.json`.
- The skill always uses `--keyring-backend os` for local key lookups and generated submission commands.
- Direct signer fallback: `generate_submission.py --mode direct`.
- Required local dependencies are `python3` and `shentud`. Environment variables are optional overrides, not mandatory setup: `OPENMATH_ENV_CONFIG`, `OPENMATH_SHENTUD_BIN`, `OPENMATH_SUBMISSION_MODE`, `OPENMATH_INNER_TX_FEES`, `OPENMATH_INNER_TX_GAS`, `SHENTU_CHAIN_ID`, and `SHENTU_NODE_URL`.

For least-privilege operation, treat `openmath-env.json` creation or editing, `shentud` installation, and local key creation or recovery as manual prerequisites documented in `references/`. The default skill flow may run read-only checks such as `command -v shentud`, `shentud version`, or `shentud keys show`, but it should not auto-install binaries, auto-edit config files, or run `shentud keys add` as part of normal execution.

Before any action that writes `openmath-env.json` or creates or recovers a local key, get explicit user approval. `shentud` installation should stay a manual user step, guided by the reference docs rather than performed by the skill. Prefer the official Shentu releases page plus a user-local install at `$HOME/bin/shentud`, and use `OPENMATH_SHENTUD_BIN` only as an explicit fallback. Do not generate or manage mnemonics on the user's machine without that approval.

### First-run gate

If the selected `openmath-env.json` is missing, or if it exists but is missing `prover_address`, `agent_address`, or `agent_key_name`, **do not proceed**. Follow [references/init-setup.md](references/init-setup.md), and treat any config write or key creation/recovery as an explicit-user-approval step, then validate:

```bash
python3 scripts/check_authz_setup.py [--config <path>]
```

Require `Status: ready` before any submission. Repeat on each new machine or workspace.

This gate is mandatory for authz-mode scripts that advance the submission flow. `generate_submission.py` must not produce authz `proof-hash` or `proof-detail` commands until `check_authz_setup.py` returns `Status: ready`. Read-only status polling via `query_submission_status.py` is exempt.

### Workflow checklist

- [ ] **Manual prerequisites**: If `shentud` is missing, use `references/submission_guidelines.md` for manual binary install. If `openmath-env.json` is missing or incomplete, or the local `os` key does not exist yet, use `references/init-setup.md`. If authz or feegrant is still missing after setup, use `references/authz_setup.md`. The default skill flow should not auto-edit config files, auto-install `shentud`, or auto-create or recover keys.
- [ ] **Env**: `openmath-env.json` exists in `./.openmath-skills/` or `~/.openmath-skills/`, and `check_authz_setup.py` reports `Status: ready`.
- [ ] **Stage 1 (Commit)**: Run `generate_submission.py hash <theoremId> <proofPath> <proverKeyOrAddress> <proverAddr>` only after the first-run gate passes; this generates the commitment hash and the corresponding `shentud tx authz exec proofhash.json ... --fee-granter <prover-address>` flow.
- [ ] **Wait**: 5–10 s, then `query_submission_status.py tx <txhash> --wait-seconds 6`. Confirm proof in `PROOF_STATUS_HASH_LOCK_PERIOD` and record `proof_id`.
- [ ] **Stage 2 (Reveal)**: Run `generate_submission.py detail <proofId> <proofPath> <proverKeyOrAddress>` only after the first-run gate passes; this reveals the proof detail and emits the corresponding `shentud tx authz exec proofdetail.json ... --fee-granter <prover-address>` flow. Do not wait for hash lock expiry.
- [ ] **Verify**: Wait 5–10 s, then `query_submission_status.py theorem <theoremId> --wait-seconds 6`. Confirm theorem reaches `THEOREM_STATUS_PASSED`.

### Scripts

| Script | Command | Use when |
|--------|---------|----------|
| Authz readiness | `python3 scripts/check_authz_setup.py [--config <path>]` | Before first submission and when changing env; validates CLI, keys, RPC, authz, feegrant. |
| Stage 1 commands | `python3 scripts/generate_submission.py hash <theoremId> <proofPath> <proverKeyOrAddress> <proverAddr>` | Generating `proofhash.json` and the broadcast command for the commitment stage. In authz mode, refuses to continue until the first-run gate passes. |
| Stage 2 commands | `python3 scripts/generate_submission.py detail <proofId> <proofPath> <proverKeyOrAddress>` | Generating `proofdetail.json` and the broadcast command for the reveal stage (use `proof_id` from Stage 1). In authz mode, refuses to continue until the first-run gate passes. |
| Query tx | `python3 scripts/query_submission_status.py tx <txhash> [--wait-seconds 6]` | After broadcast to confirm inclusion. |
| Query theorem | `python3 scripts/query_submission_status.py theorem <theoremId> [--wait-seconds 6]` | Final status check. |
| Proof hash (debug) | `python3 scripts/calculate_proof_hash.py <theoremId> <proverAddress> <proofContentOrFile>` | Standalone hash check; normally used by generate_submission. |

`submission_config.py` loads and validates only the identity/authz fields in `openmath-env.json` using the shared config resolution order above. Chain/RPC settings come from `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL`.

Reference split:

- `references/submission_guidelines.md`: manual binary install, pre-submission checks, and the two-stage submit flow
- `references/init-setup.md`: `openmath-env.json`, local key setup, and the normal website authorization flow
- `references/authz_setup.md`: manual authz + feegrant CLI fallback after setup

### Notes

- **Authz**: Default flow uses `shentud tx authz exec` with `--fee-granter <prover-address>`. For direct signer use `--mode direct` on `generate_submission.py`.
- **Commit-reveal**: Stage 1 publishes only the proof hash as a commitment, which reduces proof leakage and front-running risk while reserving your claim. Stage 2 reveals the full proof detail for verification.
- **Key material**: Treat local key creation or recovery as a manual step. If `shentud keys add` is needed, show the user the documented commands in the references instead of running them from the skill, and warn that mnemonics or recovery material may be shown.
- **Binary setup**: Manual binary setup is required. Prefer a trusted release binary installed at `$HOME/bin/shentud`. Verify with `command -v shentud` and `shentud version` before submission.
- **Config editing**: Manual config setup is preferred. Point the user to `references/init-setup.md` and `references/openmath-env.example.json` instead of having the skill rewrite `openmath-env.json`.
- **Binary resolution**: Check the plain `shentud` command first. If `shentud` already works from `PATH`, do not force a separate binary path. Set `OPENMATH_SHENTUD_BIN` only as a fallback when the default `shentud` lookup is missing or broken and you need a specific trusted binary.
- **Advanced env vars**: `OPENMATH_SUBMISSION_MODE` changes the default `generate_submission.py --mode` (`authz` by default). `OPENMATH_INNER_TX_FEES` and `OPENMATH_INNER_TX_GAS` override the generated inner `--generate-only` tx fees/gas in authz mode.
- **Local shell env**: `PATH` affects local `python3` / `shentud` discovery, and references may use `$HOME/bin` when showing non-persistent local install examples.
- **Block wait**: After each broadcast wait ~5–10 s before querying.

## References

Load when needed (one level from this file):

- **[references/init-setup.md](references/init-setup.md)** — Config-first env setup, local key resolution, and the normal website authorization flow.
- **[references/openmath-env.example.json](references/openmath-env.example.json)** — Template for `openmath-env.json`.
- **[references/submission_guidelines.md](references/submission_guidelines.md)** — Manual binary install, pre-submission checks, commit-reveal execution, and status verification.
- **[references/authz_setup.md](references/authz_setup.md)** — Manual authz grants and feegrant fallback after setup.
