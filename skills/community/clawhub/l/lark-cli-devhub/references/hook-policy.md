# Hook Policy

The hook is a gate, not the writer. Agents should write knowledge before commit or push. Hooks only check for evidence.

## Accepted Evidence

The gate accepts one of:

- `# kb-updated` in the git command after a real Feishu write.
- `.devhub/receipts/*.json` created by `devhub.py`.
- `.devhub/outbox/*.json` created after a failed write attempt.
- `# kb-skip: reason` when writing is intentionally skipped.

## Modes

`shadow` mode:

- Warns on missing writeback.
- Does not block commits or pushes.
- Best for the first week while prompts and fields are still settling.

`enforced` mode:

- Blocks missing writeback with exit code `2`.
- Use after the team trusts the workflow.

Mode lives in:

```text
$HOME/.codex/devhub/config.json
```

## Trigger Rules

The default gate triggers on:

- `git push` to `main` or `master`
- `git commit` whose command text includes `fix`, `bug`, or `release`

The gate intentionally avoids network calls and large Feishu writes inside git hooks. Network writes are brittle in hook contexts and can make normal development feel stuck.

## Codex / Claude Code Integration

For Codex or Claude Code hook systems that pass tool-call JSON to a shell script, point the hook to:

```bash
$HOME/.codex/devhub/bin/kb-gate.sh
```

For plain git hooks, call:

```bash
python3 "$HOME/.codex/devhub/bin/devhub.py" hook-check --command "$*" --cwd "$PWD"
```

Project-local runtime folders:

```bash
mkdir -p .devhub/receipts .devhub/outbox
```
