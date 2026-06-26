# Setup `MARKETUP_API_KEY` (preflight)

When `MARKETUP_API_KEY` is missing, execute the setup script at `../scripts/setup-marketup-api-key.sh` before any Marketup API task.

Do not inline or improvise setup logic in chat. Use the script so behavior stays consistent.
Do not ask the user to run the script manually. The agent must execute the script itself and only ask the user for the key input prompted by the script.
Do not prematurely terminate the script execution.

## What the script does

1. Prompts the user to enter `MARKETUP_API_KEY`.
2. Creates `~/.openclaw/.env` if it does not exist.
3. Updates existing `MARKETUP_API_KEY` when present, otherwise appends `MARKETUP_API_KEY=<user_input>`.
4. Prints a success message when key is saved.
5. Prints a "no key entered" message and exits non-zero when input is empty.

## Agent behavior after execution

- Re-check whether `MARKETUP_API_KEY` exists in environment.
- If present, continue with the user task.
- If still missing, do not call Marketup APIs; return guidance-only response and ask user to retry setup.
