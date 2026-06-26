# Keychain Access Skill

## Purpose
Manage macOS Keychain generic passwords through the bundled `keychain-access.sh` helper. The script wraps the native `security` CLI, enforces confirmations for changes, masks secrets by default, and exposes dry-run previews so other agents or users can safely inspect or adjust stored credentials.

## Install & use overview
1. Clone or pull this repository and ensure the helper is executable:
   ```bash
   cd <repo-root>
   chmod +x keychain-access.sh
   ```
2. Run the script directly from the repository (or add it to your PATH) with one of the supported verbs (`list`, `get`, `set`, `delete`).
3. Provide all required filters (service and account) and, for mutations, a secure password input method, confirmation flags, and `--dry-run` when you only want to preview the underlying `security` command.

## Command examples
### list
```bash
./keychain-access.sh list --service my-app --account automation-bot
```
Filters the requested keychain (default search list or `--keychain PATH`) and prints service/account/label rows for matching entries. Add `--dry-run` to see the `security dump-keychain` invocation.

### get
```bash
./keychain-access.sh get --service my-app --account automation-bot --keychain /tmp/my.keychain --raw
```
Returns metadata for a generic password. Password output is masked unless `--raw` is supplied, so omit `--raw` unless you explicitly need the secret.

### set
```bash
printf '<SECRET>' | ./keychain-access.sh set --service my-app --account automation-bot --password-stdin --yes
```
Creates or updates a credential while prompting before overwriting an existing entry (use `--yes` to skip). Supply the secret via `--password-stdin`, `--password-env VAR`, or the interactive hidden prompt to keep values out of shell history. `--dry-run` previews the `security add-generic-password` call without touching the keychain.

### delete
```bash
./keychain-access.sh delete --service my-app --account automation-bot
```
Prompts before removing a credential that matches the provided filters. Add `--yes` to automate, and `--dry-run` to preview the `security delete-generic-password` command without deleting anything.

## Security notes
- `get` masks passwords by default; only force plaintext output with `--raw` after confirming the requester truly needs the secret.
- Prefer `--password-stdin`, `--password-env VAR`, or the hidden interactive prompt for `set`. These keep secrets out of process listings and shell history. The legacy `--password` flag still works but triggers a warning because it exposes the value in command arguments.
- All mutations (`set`, `delete`) prompt for confirmation before altering or removing entries. Use `--yes` only when you have explicitly authorized the change and understand the impact.
- `--dry-run` is available for any verb to preview the underlying `security` invocation without touching the keychain or prompting for confirmation.
