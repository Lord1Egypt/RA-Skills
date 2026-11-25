# GitHub Copilot CLI

CLI platform: `copilot`.

The [configuration directory reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
documents `disabledSkills` and repository/user union semantics. Removing a user
entry does not cancel a repository disable. The adapter preserves unrelated
JSON values, but normalizes JSONC formatting after backing it up. Native
inventory is preferred when it returns usable JSON; fallback is less complete.

## Operational notes

Use native configuration semantics. --allow-undiscovered is only for an explicitly requested literal host key, never typo correction. Repository disables may still override user state.
