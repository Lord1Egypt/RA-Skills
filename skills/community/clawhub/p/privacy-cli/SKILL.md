---
name: privacy-cli
description: Use the Privacy CLI to create and manage Privacy Virtual Cards directly from the terminal. Trigger this skill whenever the user asks to create, list, pause, update, or close a virtual card, or fetch transaction history for Privacy.com.
compatibility: Requires PRIVACY_API_KEY environment variable and @privacy-com/privacy-cli npm package
metadata:
  required_env_vars:
    - PRIVACY_API_KEY
  required_binaries:
    - npm
    - node
    - privacy
---

# Privacy CLI Skill

This skill allows the agent to interact with the Privacy API via the official CLI to manage Privacy Virtual Cards and view transactions.

## Reference Documentation
For missing information or edge cases, refer to the official documentation: https://developers.privacy.com/docs/privacy-cli

## 1. Installation & Setup
Before executing commands, check if the CLI is installed by running:
`privacy --version`

**If not installed, run the folling:**
`npm install -g @privacy-com/privacy-cli`

## 2. Configuration & Authentication
The Privacy CLI requires an API key (the user must be on a paid Privacy Plan).
Check for authentication by running a harmless command like `privacy cards list --page-size 1 --json`.

If it fails due to missing authentication:
1. Instruct the user to get their API key from https://app.privacy.com/subscriptions.
2. Ask the user to set the `PRIVACY_API_KEY` environment variable in their terminal (e.g., `export PRIVACY_API_KEY="your_api_key_here"`).

The CLI resolves your API key in this order:

1. PRIVACY_API_KEY environment variable
2. ~/.privacy/config file (JSON with api_key field)

## 3. Usage Guidelines for the Agent
- **Output Mode**: **ALWAYS** append the `--json` flag to your commands so you can parse the output programmatically!
- **Interactive Mode**: **NEVER** use the interactive REPL mode (`privacy` or `privacy interactive`). Always use non-interactive one-off commands. Do not prompt the user to use interactive mode either.
- **Security Warning (PAN Data)**: If the user asks for full card details (PAN, CVV, Expiry), you **MUST require explicit user confirmation** before running `privacy cards pan <token> --json`. **Do not log, save, or store the PAN output** in any file; only display it securely to the user in your response.

## 4. Commands Reference

### Cards
- **Create Card:** 
  `privacy cards create --type <SINGLE_USE|MERCHANT_LOCKED> [--memo "label"] [--spend-limit <whole_dollars>] [--spend-limit-duration <TRANSACTION|MONTHLY|ANNUALLY|FOREVER>] --json`
  *(Note: SINGLE_USE closes automatically after the first transaction, MERCHANT_LOCKED locks to the first merchant it is used with).*
- **List Cards:** 
  `privacy cards list [--page <number>] [--page-size <number>] --json`
- **Get Card Details:** 
  `privacy cards get <token> --json`
- **Update Card:** 
  `privacy cards update <token> [--memo "new label"] [--spend-limit <amount>] [--spend-limit-duration <duration>] [--state <OPEN|PAUSED|CLOSED>] --json`
- **Pause/Unpause Card:** 
  `privacy cards pause <token> --json`
  `privacy cards unpause <token> --json`
- **Close Card (Permanent):** 
  `privacy cards close <token> --json`
- **Get Full PAN (Sensitive):** 
  `privacy cards pan <token> --json`

### Transactions
- **List Transactions:** 
  `privacy transactions list [--begin YYYY-MM-DD] [--end YYYY-MM-DD] [--card-token <token>] [--result APPROVED|DECLINED] [--page <number>] [--page-size <number>] --json`
