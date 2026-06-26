---
name: keychain-access
description: "macOS Keychain helpers (list/get/set/delete) via the security CLI. Trigger this skill when the user needs to inspect, store, update, or remove generic passwords from the Keychain with explicit confirmation on destructive ops and guarded secret disclosure."
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins:
        - security
---

# Keychain Access Skill

Manage macOS Keychain items in a safe, scriptable way. Use the bundled `keychain-access/keychain-access.sh` helper for all operations: it wraps `security` calls, enforces confirmations for updates and deletions, masks secrets unless explicitly requested, and supports dry-run previews.

## Safety Constraints

- Never print secrets unless the user explicitly asks to reveal them (`--raw`). Routine `get` calls only report metadata with the password hidden.
- Ask the user to confirm before modifying or deleting existing entries. The script prompts by default and accepts `--yes` to skip the prompt for automation.
- Support a `--dry-run` mode so agents can preview the `security` command without touching the Keychain.
- Supply secrets via `--password-stdin`, `--password-env`, or the hidden interactive prompt. The legacy `--password` option leaves values in shell history and process listings (the helper warns when it's used), so prefer the safer inputs; `--password-env VAR` reads the var and unsets it immediately to keep the secret out of the environment.
- Operate on a specific keychain when provided (`--keychain`); otherwise, the default search list is used. Avoid leaking system passwords by defaulting to explicit service/account filters.

## Supported Operations

1. **list** – Summaries of matching entries.
   ```bash
   ./skills/keychain-access/keychain-access.sh list \
     [--keychain /path/to/keychain] [--service NAME] [--account NAME]
   ```
   - Scans the chosen keychain via `security dump-keychain` and prints service/account/label rows.
   - Filters can target a specific service or account (substring match).
   - Use `--dry-run` to review the `security dump-keychain` invocation without running it.

2. **get** – Display metadata for a generic password.
   ```bash
   ./skills/keychain-access/keychain-access.sh get \
     --service SERVICE --account ACCOUNT [--keychain PATH] [--raw] [--dry-run]
   ```
   - Requires both `--service` and `--account` to avoid ambiguity.
   - Password output is masked by default; add `--raw` only when the user explicitly needs the secret value.
   - Returns command diagnostics even if the password is hidden (e.g., matching record, keychain path).
   - Use `--dry-run` to review the `security find-generic-password` invocation without reaching into the keychain.

3. **set** – Create or update a generic password entry.
   ```bash
   printf '<SERVICE_SECRET>' | ./skills/keychain-access/keychain-access.sh set      --service SERVICE --account ACCOUNT      --password-stdin      [--keychain PATH] [--yes] [--dry-run]
   ```
   - Supply the password via `--password-stdin`, `--password-env VAR`, or the hidden interactive prompt that runs when stdin is a terminal and no source is provided. The legacy `--password` flag still works but is insecure because its value appears in shell history and process listings, so the helper prints a warning if it is used.
   - `--password-env VAR` reads the named env var, unsets it immediately after reading, and keeps the secret out of the command line and environment dumps.
   - When a matching service/account already exists, the helper announces the pending update and prompts for confirmation before overwriting (use `--yes` to skip the prompt once you have authorized the change).
   - `--dry-run` prints the `security add-generic-password ...` invocation with the password redacted and exits before checking for an existing entry or prompting.

4. **delete** – Remove a matching generic password.
   ```bash
   ./skills/keychain-access/keychain-access.sh delete \
     --service SERVICE --account ACCOUNT [--keychain PATH] [--yes] [--dry-run]
   ```
   - Always prompts before deletion; `--yes` bypasses the prompt if the user already authorized removing the credential.
   - The helper verifies the entry exists before asking for confirmation.
   - Combine with `--dry-run` to preview the `security delete-generic-password` invocation while keeping the keychain untouched; the helper exits before verifying the entry or prompting.

## Request Examples

- "Store a new API token for `terraform` under account `ci-bot`." → run `set` for that service/account, pipe `<TERRAFORM_TOKEN>` into `--password-stdin` (or set `TERRAFORM_TOKEN` and pass `--password-env TERRAFORM_TOKEN`), then confirm the update if prompted.
- "Show everything stored for `smtp` credentials." → run `list --service smtp` and then `get` with `--raw` only if the user explicitly needs to read the password.
- "Rotate the password for `deploy-bot` and remove the old entry." → use `set` with `--service deploy` and `--account deploy-bot`, supply the new secret through one of the safe input options, allow the helper to prompt for confirmation, then `delete` the old credential with confirmation when the rotation is complete.
- "Preview the delete command for the app key without running it." → use `delete --service app-key --account release-bot --dry-run`.

## Testing Transcript (safe context)

```bash
# Prepare a disposable keychain (password = <KEYCHAIN_PASSWORD>)
security create-keychain -p <KEYCHAIN_PASSWORD> /tmp/keychain-access-test.keychain
security unlock-keychain -p <KEYCHAIN_PASSWORD> /tmp/keychain-access-test.keychain

# 1) List entries (empty keychain)
./skills/keychain-access/keychain-access.sh list   --keychain /tmp/keychain-access-test.keychain
# Output:
No matching entries found.

# 2) Set a credential (confirms before update)
printf '<SERVICE_SECRET>' | ./skills/keychain-access/keychain-access.sh set   --service test-service --account test-user   --password-stdin --keychain /tmp/keychain-access-test.keychain --yes
# Output:
Stored credential for 'test-service' / 'test-user'.

# 3) Get the credential (masked by default, raw only when asked)
./skills/keychain-access/keychain-access.sh get   --service test-service --account test-user   --keychain /tmp/keychain-access-test.keychain --raw
# Output:
password: "<SERVICE_SECRET>"
keychain: "/private/tmp/keychain-access-test.keychain"
version: 256
class: "genp"
attributes:
    0x00000007 <blob>="test-service"
    0x00000008 <blob>=<NULL>
    "acct"<blob>="test-user"
    ... (remaining metadata omitted for brevity)

# 4) Delete the credential (prompts confirmation)
./skills/keychain-access/keychain-access.sh delete   --service test-service --account test-user   --keychain /tmp/keychain-access-test.keychain --yes
# Output:
Deleted credential for 'test-service' / 'test-user'.

# Cleanup
security delete-keychain /tmp/keychain-access-test.keychain
```

Include this transcript in reports so the main agent knows the commands and their expected output shape.
