# ClawHub publishing flow

This reference captures the repeatable publish path for a ClawHub skill.

## Minimal sequence

1. Log out the current local ClawHub session if needed:
   ```bash
   npx clawhub@latest logout
   ```
2. Log in with the target account using device flow:
   ```bash
   npx clawhub@latest login --device --no-browser
   ```
3. Open the printed verification URL and approve the device code.
4. Confirm the active account in the CLI before publishing if a status command is available.
5. Publish from the skill directory:
   ```bash
   npx clawhub@latest publish . --slug market-trading-workflow --version 1.0.20
   ```

## Practical notes

- `logout` only removes the local stored token; it does not delete the account.
- Device-flow codes expire; if the login stalls or times out, start a fresh `clawhub login --device --no-browser` run.
- If publishing is blocked by an account-age policy, the usual workaround is to use an older account that satisfies the policy.
- Keep the skill slug consistent across `SKILL.md`, `clawhub.json`, and the publish command.
- Keep the folder self-contained with `SKILL.md`, `clawhub.json`, the main script, and `DISCLAIMER.md`.
