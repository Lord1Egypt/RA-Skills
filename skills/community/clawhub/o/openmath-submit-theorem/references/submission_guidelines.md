# Shentu Proof Submission Guidelines

## 0. Config
Before any proof submission, confirm the local Shentu CLI environment is ready.

Required components:
*   `python3` is installed and available in `PATH`
*   `shentud` is installed and available in `PATH`
*   The target key already exists in the local keyring
*   The RPC endpoint is reachable from the current machine

Recommended checks:

```bash
command -v python3
python3 --version
command -v shentud
shentud version
shentud keys list --keyring-backend os
```

Least-privilege default: `shentud` installation and local key creation or recovery are manual prerequisites. The default skill flow may run read-only checks such as `command -v shentud`, `shentud version`, and `shentud keys show`, but it should not auto-install binaries or auto-create or recover keys.

If `shentud` is missing or the keyring is not configured, stop here and install/configure the Shentu environment first. Do not start Stage 1 until these checks pass.
First check whether plain `shentud` already works. If `command -v shentud` fails, the default path is broken, or `shentud version` cannot run, prefer either a manual install of a vetted binary or setting `OPENMATH_SHENTUD_BIN` to a trusted absolute path.

### Install `shentud` if Missing
Recommended default:

1. Download a trusted release binary from the official Shentu releases page:
   `https://github.com/shentufoundation/shentu/releases`
2. Choose the binary that matches the current machine operating system and CPU architecture.
   Common filename patterns include:
   - macOS Apple Silicon: `*_arm64_macos`
   - Linux x86_64: `*_linux_amd64`
   Check the current machine with:

```bash
uname -s
uname -m
```

3. Rename it to `shentud`.
4. Install it to the user-local path `$HOME/bin/shentud`.
5. Add `$HOME/bin` to `PATH` for the current shell.
6. Verify with:

```bash
command -v shentud
shentud version
```

The preferred install target is:

```bash
$HOME/bin/shentud
```

This keeps the install user-local and avoids requiring system-wide write permissions.

Only use a system-wide location such as `/usr/local/bin/shentud` if the user explicitly wants that and understands the higher-privilege write.

### Example Setup
macOS Apple Silicon quick download example for `v2.17.0`:

```bash
curl -L https://github.com/shentufoundation/shentu/releases/download/v2.17.0/shentud_2.17.0_arm64_macos -o shentud
chmod +x shentud
```

Linux x86_64 quick download example for `v2.17.0`:

```bash
wget https://github.com/shentufoundation/shentu/releases/download/v2.17.0/shentud_2.17.0_linux_amd64 -O shentud
chmod +x shentud
```

Recommended user-local install without editing a shell rc file:

macOS (`zsh`):

```bash
mkdir -p "$HOME/bin"
mv shentud "$HOME/bin/shentud"
export PATH="$HOME/bin:$PATH"
command -v shentud
shentud version
```

Linux (`bash`):

```bash
mkdir -p "$HOME/bin"
mv shentud "$HOME/bin/shentud"
export PATH="$HOME/bin:$PATH"
command -v shentud
shentud version
```

If `command -v shentud` prints a path and `shentud version` succeeds, the CLI is ready for this skill.

If you want the `PATH` change to persist across new shells, review and edit the relevant shell rc file manually as a separate explicit step.

### Alternative Install Locations
Use one of these only if the default `$HOME/bin/shentud` path is not what the user wants:

1. An existing directory that is already on `PATH`
2. A trusted explicit path used via `OPENMATH_SHENTUD_BIN`
3. A system-wide location such as `/usr/local/bin/shentud`

Keep the executable name as `shentud` in all cases.

### Explicit Binary Path Fallback
If the user does not want to modify `PATH`, or wants the skill to use a specific vetted binary, set an explicit path instead:

```bash
export OPENMATH_SHENTUD_BIN=/absolute/path/to/shentud
```

Then verify the exact binary the skill will use:

```bash
"$OPENMATH_SHENTUD_BIN" version
```

### Config and Local Key Gate
This document assumes the authz submission environment is already configured.

If any of the following is missing, stop here and go to `references/init-setup.md`:

- `openmath-env.json`
- `prover_address`
- `agent_key_name`
- `agent_address`
- a usable local `os` key for `agent_key_name`

After setup, validate before returning to this document:

```bash
python3 scripts/check_authz_setup.py [--config <selected-path>]
```

Do not run `generate_submission.py` in authz mode until that command returns `Status: ready`.

## 1. Network Defaults
Chain settings are read from `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL` (default: `shentu-2.2`, `https://rpc.shentu.org:443`).

## 2. Prerequisites
Before submitting, ensure:
*   **Proof Integrity**: Your Lean/Rocq proof is complete and locally verified.
*   **Environment**: The `Config` checks above already pass.

### Pre-Submission Checklist
Before generating or broadcasting any submission command, confirm all 6 items below:

1. **`shentud` is available**
   ```bash
   command -v shentud
   shentud version
   ```
2. **The local agent execution key exists**
   ```bash
   shentud keys show agent-prover -a --keyring-backend os
   ```
   If the key is missing, stop and go back to `references/init-setup.md`. Do not run `shentud keys add` as part of the default submission flow.
3. **The OpenMath Wallet Address owner (`prover_address`) has enough `uctk`**
   ```bash
   shentud q bank balance --denom uctk --address <FEE_GRANTER_ADDRESS> --node <shentu_node_url>
   ```
   Use `SHENTU_NODE_URL` or the built-in default `https://rpc.shentu.org:443`. Make sure the balance covers the proof deposit and gas fees.
   If plain `shentud` already works, keep using it. If it does not, either fix `PATH` for the current shell or set `OPENMATH_SHENTUD_BIN` to a trusted absolute path before running the submission scripts.
4. **The authz + feegrant setup is ready**
   ```bash
   python3 scripts/check_authz_setup.py [--config <selected-path>]
   ```
   Confirm that the required authz grants exist and the feegrant allows `/cosmos.authz.v1beta1.MsgExec`. `generate_submission.py` in authz mode should be treated as blocked until this returns `Status: ready`.
5. **The proof file is the right local file**
   ```bash
   test -f <proof-path>
   ```
   The file should match the target theorem, use the correct language, and be locally checked before submission.
6. **The theorem ID is correct**
   ```bash
   shentud q bounty theorem <theorem-id> --node <shentu_node_url>
   ```
   Confirm that the theorem exists and that you are submitting against the intended theorem ID.

### Shortest Submission Flow
If the environment, authz config, balance, proof file, and theorem ID are already confirmed, the shortest end-to-end flow is:

1. Verify authz readiness:
   ```bash
   python3 scripts/check_authz_setup.py [--config <selected-path>]
   ```
2. Generate the Stage 1 commands:
   ```bash
   python3 scripts/generate_submission.py hash <theoremId> <proofPath> <proverKeyOrAddress> <proverAddr>
   ```
3. Run the emitted `proofhash.json` generation command.
4. Broadcast Stage 1 with the emitted `shentud tx authz exec proofhash.json ... --fee-granter <prover-address>` command and record the returned `txhash`.
5. Wait `5-10` seconds, then query the tx:
   ```bash
   python3 scripts/query_submission_status.py tx <txhash> --wait-seconds 6
   ```
6. Confirm the proof exists on-chain and is in `PROOF_STATUS_HASH_LOCK_PERIOD`, then record the returned `proof_id`.
7. Generate the Stage 2 commands:
   ```bash
   python3 scripts/generate_submission.py detail <proofId> <proofPath> <proverKeyOrAddress>
   ```
8. Run the emitted `proofdetail.json` generation command.
9. Broadcast Stage 2 during the hash-lock window with the emitted `shentud tx authz exec proofdetail.json ... --fee-granter <prover-address>` command and record the returned `txhash`.
10. Wait `5-10` seconds, then query the Stage 2 tx:
   ```bash
   python3 scripts/query_submission_status.py tx <txhash> --wait-seconds 6
   ```
11. Wait another `5-10` seconds, then query the theorem status:
   ```bash
   python3 scripts/query_submission_status.py theorem <theoremId> --wait-seconds 6
   ```
12. Treat `THEOREM_STATUS_PASSED` as the successful final state.

## 3. Wallet & Balance Check
### Check Keys
Verify the local agent execution key exists and get its address:
```bash
shentud keys show <agent-key-name> -a --keyring-backend os
```

This address should match `agent_address` in `openmath-env.json`.
If the key is missing, go back to `references/init-setup.md` and complete the local key setup first.

### Check Balance
Proof submission requires:

- the OpenMath Wallet Address owner (`prover_address`) to cover the proof deposit
- the feegranter allowance to cover outer `authz exec` gas

Verify the `prover_address` `uctk` balance:
```bash
shentud q bank balance --denom uctk --address <PROVER_ADDRESS> --node <shentu_node_url>
```
*   **Precision**: 1 CTK = 1,000,000 uctk (6 decimal places).
*   Ensure you have enough `uctk` for both the deposit and gas fees.

## 4. Two-Stage Submission Process

### Stage 1: Submit Proof Hash (Commitment)
Prevents front-running and proof leakage while securing your spot.
*   **Message**: `MsgSubmitProofHash`
*   **Parameters**: `theorem_id`, `prover` (address), `proof_hash`, `deposit`.

#### Proof Hash Calculation (Go Logic)
The `proof_hash` is a hex-encoded SHA256 hash of the marshaled `ProofHash` struct:
```go
func (k Keeper) GetProofHash(theoremID uint64, prover, detail string) string {
    proofHash := &types.ProofHash{
        TheoremId: theoremID,
        Prover:    prover,
        Detail:    detail,
    }
    bz := k.cdc.MustMarshal(proofHash)
    hash := sha256.Sum256(bz)
    return hex.EncodeToString(hash[:])
}
```
*   `theoremID`: The ID of the theorem.
*   `prover`: Your OpenMath Wallet Address on Shentu.
*   `detail`: The actual proof content string.

**Default Authz Flow** (same shape emitted by the bundled script):
```bash
shentud tx bounty proof-hash \
  --theorem-id <theorem-id> \
  --hash <proof-hash> \
  --deposit 1000000uctk \
  --from <prover-address> \
  --fees 5000uctk \
  --gas 200000 \
  --chain-id shentu-2.2 \
  --keyring-backend os \
  --generate-only -o json > proofhash.json

shentud tx authz exec proofhash.json \
  --from <agent-key-name> \
  --fee-granter <prover-address> \
  --gas auto \
  --gas-adjustment 2.0 \
  --gas-prices 0.025uctk \
  --keyring-backend os \
  --chain-id shentu-2.2 \
  --node https://rpc.shentu.org:443 \
  -y
```

The inner `proofhash.json` should be the raw `MsgSubmitProofHash` transaction generated with `--generate-only`.
The outer `authz exec` is the real broadcast transaction, so the feegrant must allow `/cosmos.authz.v1beta1.MsgExec`.
Any fee, gas, signer info, or signatures inside `proofhash.json` are not what the chain uses for the outer broadcast.

**After Broadcast**:
1. Wait about **5-10 seconds** for the next block.
2. Query the tx receipt:
   ```bash
   python3 scripts/query_submission_status.py tx <txhash> --wait-seconds 6
   ```
3. Query the proof and confirm it is in `PROOF_STATUS_HASH_LOCK_PERIOD`. Submit Stage 2 during this hash-lock window; do not wait for the proof `end_time` to pass before revealing.

#### Stage 1 Broadcast Checklist
After broadcasting `proof-hash`, confirm all 5 items below:

1. Record the returned `txhash`.
2. Wait about `5-10` seconds for block inclusion.
3. Confirm the tx query returns `code: 0`.
4. Confirm the outer tx action is `/cosmos.authz.v1beta1.MsgExec`.
5. Query the proof, confirm it is in `PROOF_STATUS_HASH_LOCK_PERIOD`, and record the returned `proof_id` for Stage 2. On the current flow, this matches the submitted proof hash hex string.

### Stage 2: Submit Proof Detail (Reveal)
Submit the actual proof content to claim the bounty after the hash is successfully recorded. Reveal during the `PROOF_STATUS_HASH_LOCK_PERIOD`; do not wait for the hash-lock window to end.
*   **Message**: `MsgSubmitProofDetail`
*   **Parameters**: `proof_id` (received after stage 1; this matches the proof hash hex string), `prover`, `detail` (the actual proof text).
*   **Default Authz Flow** (the bundled script shell-quotes the proof body for you):
    ```bash
    shentud tx bounty proof-detail \
      --proof-id <proof-id> \
      --detail '<proof-content-string>' \
      --from <prover-address> \
      --fees 5000uctk \
      --gas 200000 \
      --chain-id shentu-2.2 \
      --keyring-backend os \
      --generate-only -o json > proofdetail.json

    shentud tx authz exec proofdetail.json \
      --from <agent-key-name> \
      --fee-granter <prover-address> \
      --gas auto \
      --gas-adjustment 2.0 \
      --gas-prices 0.025uctk \
      --keyring-backend os \
      --chain-id shentu-2.2 \
      --node https://rpc.shentu.org:443 \
      -y
    ```

The inner `proofdetail.json` should be the raw `MsgSubmitProofDetail` transaction generated with `--generate-only`.
Only the inner `body.messages` content matters to `authz exec`; the outer tx determines the real signer, gas, and feegrant usage.

**After Broadcast**:
1. Wait about **5-10 seconds** for the next block.
2. Query the tx receipt:
   ```bash
   python3 scripts/query_submission_status.py tx <txhash> --wait-seconds 6
   ```
3. Wait another **5-10 seconds** and query the theorem status:
   ```bash
   python3 scripts/query_submission_status.py theorem <theorem-id> --wait-seconds 6
   ```

#### Stage 2 Broadcast Checklist
After broadcasting `proof-detail`, confirm all 6 items below:

1. Record the returned `txhash`.
2. Wait about `5-10` seconds for block inclusion.
3. Confirm the tx query returns `code: 0`.
4. Confirm the outer tx action is `/cosmos.authz.v1beta1.MsgExec`.
5. Wait another `5-10` seconds and query the theorem status.
6. Confirm the theorem status reaches the expected final state, typically `THEOREM_STATUS_PASSED`.

## 5. Theorem Status Meanings

Use the chain query below to check the canonical theorem status:

```bash
shentud q bounty theorem <theorem-id> --node <shentu_node_url>
```

Important statuses:

*   `THEOREM_STATUS_PASSED`: The theorem proof has passed verification.
*   `THEOREM_STATUS_PROOF_PERIOD`: The theorem is still within the active proof period and is being proven.
*   `THEOREM_STATUS_CLOSED`: The theorem is no longer active and has been closed.
