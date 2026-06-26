# Init Setup

## Overview

Triggered when:

1. No usable `openmath-env.json` is found through the shared resolution order -> full authz submission setup
2. The selected `openmath-env.json` exists but one or more required identity fields are missing -> missing-fields setup

Required identity fields:

- `prover_address` (`OpenMath Wallet Address`)
- `agent_key_name`
- `agent_address`

Default local agent key name: `agent-prover`

This is a hard gate for authz submission. Until setup is complete and `python3 scripts/check_authz_setup.py [--config <selected-path>]` returns `Status: ready`, do not generate stage 1 or stage 2 authz submission commands.

Before any step that writes `openmath-env.json` or creates or recovers a local `shentud` key, get explicit user approval. For least-privilege operation, treat these as manual setup steps and have the user run the file-copy or key-creation commands themselves. `shentud` installation should also stay a manual user action outside the default skill flow.

Shared config resolution order:
1. `--config <path>`
2. `OPENMATH_ENV_CONFIG`
3. `./.openmath-skills/openmath-env.json`
4. `~/.openmath-skills/openmath-env.json`

If `OPENMATH_ENV_CONFIG` is set, treat it as the selected config path. If that file is missing or invalid, fix it or unset it instead of silently falling back.

## Setup Flow

```text
No project/global config found        Config found, required fields missing
            |                                       |
            v                                       v
  +------------------------+              +------------------------+
  | AskUserQuestion        |              | AskUserQuestion        |
  | (full setup)           |              | (missing fields only)  |
  +------------------------+              +------------------------+
            |                                       |
            v                                       v
  +------------------------+              +------------------------+
  | Local agent key check  |              | Local agent key check  |
  +------------------------+              +------------------------+
            |                                       |
            v                                       v
  +------------------------------+        +------------------------------+
  | User creates openmath-env    |        | User updates openmath-env    |
  | manually from the template   |        | manually in the chosen file  |
  +------------------------------+        +------------------------------+
            |                                       |
            v                                       v
  +------------------------+              +------------------------+
  | Guide website authz    |              | Guide website authz    |
  +------------------------+              +------------------------+
            |                                       |
            v                                       v
  +------------------------+              +------------------------+
  | Run check_authz_setup  |              | Run check_authz_setup  |
  +------------------------+              +------------------------+
            |                                       |
            v                                       v
         Continue                                Continue
```

## Flow 1: No Usable `openmath-env.json` (Full Authz Setup)

**Language**: Use the user's input language or saved conversation language preference.

If `--config` or `OPENMATH_ENV_CONFIG` already selects a specific config path, do not ask the user to choose Project vs User first. Guide the user to create or edit that selected file manually in place.

Use AskUserQuestion with all independent questions in one call:

### Question 1: Save Location

```yaml
header: "Save"
question: "Where should OpenMath submission preferences be saved?"
options:
  - label: "Project (Recommended)"
    description: "./.openmath-skills/openmath-env.json, only for the current repository"
  - label: "User"
    description: "~/.openmath-skills/openmath-env.json, reused across repositories"
```

### Question 2: Preferred Language

```yaml
header: "Language"
question: "Preferred OpenMath theorem language?"
options:
  - label: "Lean (Recommended)"
    description: "Use Lean theorems and Lean scaffolds by default"
  - label: "Rocq"
    description: "Use Rocq theorems and Rocq scaffolds by default"
```

### Question 3: OpenMath Address

```yaml
header: "OpenMath"
question: "What is the OpenMath wallet address for this account?"
options:
  - label: "Copy From Profile (Recommended)"
    description: "Use the Wallet Address shown in the OpenMath Profile page"
  - label: "Need Lookup"
    description: "Pause and guide the user to the OpenMath Profile page first"
```

Collect the copied Wallet Address into `prover_address`.

How to find it:

1. Open [https://openmath.shentu.org](https://openmath.shentu.org)
2. Connect the wallet and enter `Profile`
3. Find `Wallet Address`
4. Copy that address into `prover_address`

The fee granter is not configured separately. It always defaults to `prover_address`.

## Local Agent Key Resolution

After the user provides `prover_address`, do not ask them to type `agent_key_name` first.
Use the default local key name `agent-prover` and resolve it locally:

```bash
shentud keys show agent-prover -a --keyring-backend os
```

### If the key exists

Resolve this without asking for alternate key names first:

1. Save `agent_key_name` as `agent-prover`
2. Save the detected bech32 address as `agent_address`
3. Continue to website authorization

### If the key does not exist

Stop and ask the user whether to create a new local key or recover an existing one. For least-privilege setup, do not run `shentud keys add` from the skill. Instead, show one of the following commands for the user to run manually after review.

Create a new key:

```bash
shentud keys add agent-prover --keyring-backend os
```

Recover an existing key:

```bash
shentud keys add agent-prover --recover --keyring-backend os
```

Then:

1. Tell the user to securely save any mnemonic or recovery material shown by `shentud`
2. Save `agent_key_name` as `agent-prover`
3. Save the resulting bech32 address as `agent_address`
4. Continue to website authorization

Only ask for a different key name or different `agent_address` if the user explicitly wants to override the default `agent-prover` flow.

## Save Locations

| Choice | Path | Scope |
|--------|------|-------|
| Project | `./.openmath-skills/openmath-env.json` | Current repository / workspace only |
| User | `~/.openmath-skills/openmath-env.json` | Reused across repositories |

### `openmath-env.json` Template

```json
{
  "preferred_language": "lean",
  "prover_address": "shentu1...",
  "agent_key_name": "agent-prover",
  "agent_address": "shentu1..."
}
```

Manual setup commands:

Project-local config:

```bash
mkdir -p .openmath-skills
cp references/openmath-env.example.json .openmath-skills/openmath-env.json
```

User-local config:

```bash
mkdir -p ~/.openmath-skills
cp references/openmath-env.example.json ~/.openmath-skills/openmath-env.json
```

After copying, have the user open the selected file and fill in the required fields manually.

## Flow 2: Config Exists, Required Fields Missing

Do not create a second config file. Have the user update the existing file in place.

Use AskUserQuestion only for the missing fields.

### Missing OpenMath Address (`prover_address`)

```yaml
header: "OpenMath"
question: "What is the OpenMath wallet address for this account?"
options:
  - label: "Copy From Profile (Recommended)"
    description: "Use the Wallet Address shown in the OpenMath Profile page"
  - label: "Need Lookup"
    description: "Pause and guide the user to the OpenMath Profile page first"
```

Lookup flow:

1. Open [https://openmath.shentu.org](https://openmath.shentu.org)
2. Connect the wallet and enter `Profile`
3. Copy `Wallet Address`
4. Save it into `prover_address`

### Missing `agent_address`

If `agent_key_name` or `agent_address` is missing, prefer the default local key name `agent-prover`:

```bash
shentud keys show agent-prover -a --keyring-backend os
```

If it exists, save:

- `agent_key_name`: `agent-prover`
- `agent_address`: the detected address

If it does not exist, stop and ask the user whether to create a new key or recover an existing one. For least-privilege setup, do not run `shentud keys add` from the skill. Instead, show one of the following commands for the user to run manually after review.

Create a new key:

```bash
shentud keys add agent-prover --keyring-backend os
```

Recover an existing key:

```bash
shentud keys add agent-prover --recover --keyring-backend os
```

Then save:

- `agent_key_name`: `agent-prover`
- `agent_address`: the resulting address

Only ask the user for a different key name or different `agent_address` if they explicitly want to override the default.

After the answers:

1. Have the user update the existing `openmath-env.json` manually in place
2. Run the local default key resolution step if needed
3. Continue to website authorization

## Website Authorization

Only guide the user to the website after both `prover_address` and `agent_address` are known. Here `prover_address` means the user's OpenMath Wallet Address copied from Profile.

Recommended flow:

1. Open [https://openmath.shentu.org/OpenMath/Profile](https://openmath.shentu.org/OpenMath/Profile)
2. Scroll to the bottom and find `AI Agent Authorization`
3. Enter `agent_address`
4. Click `Authorize`
5. Confirm the wallet transaction(s) for authz and feegrant
6. Run `python3 scripts/check_authz_setup.py [--config <selected-path>]`
7. Only after `Status: ready`, continue to `generate_submission.py`

If the website flow is unavailable, use `references/authz_setup.md`.

## Runtime Defaults

Runtime chain settings are not stored in `openmath-env.json`.

Defaults:

- `SHENTU_CHAIN_ID`: `shentu-2.2`
- `SHENTU_NODE_URL`: `https://rpc.shentu.org:443`

Only mention these environment variables when the user explicitly wants non-default chain or RPC values.

## After Setup

Expected behavior after setup:

1. `openmath-env.json` exists and contains the required identity fields
2. The local `agent_key_name` resolves to the configured `agent_address`
3. `python3 scripts/check_authz_setup.py [--config <selected-path>]` returns `Status: ready`
4. Only then may `generate_submission.py` in authz mode continue

## Notes

- Prefer asking all independent questions in one call; only split when local key creation introduces a dependency
- Do not ask the user to type `agent_key_name` or `agent_address` if the default local key flow can resolve them automatically, but do ask before creating or recovering any local key
- User-facing language naming is `rocq`
- Reward querying can stay read-only, but authz submission must respect this gate
