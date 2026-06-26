# Linear CLI Command Reference

## Commands

{{COMMANDS_LIST}}

## Quick Reference

```bash
# Discover the v3 agent-native runtime surface
linear capabilities
linear capabilities --compat v1

# Resolve refs before preview/apply
linear resolve issue ENG-123
linear resolve pack --issue ENG-123 --workflow-state started --label Bug
linear resolve team ENG
linear issue update ENG-123 --context-file slack-thread.json --apply-triage --dry-run --json
linear issue update ENG-123 --context-file slack-thread.json --autonomy-policy suggest-only --dry-run --json

# Get help for any command
linear <command> --help
linear <command> <subcommand> --help
```

## Agent Workflow

Use the CLI in this order when possible:

1. Discover command traits with `linear capabilities`, and only use `--compat v1` when an older consumer still needs the legacy trimmed shape
2. Read state with default-JSON core surfaces or `--json`
3. Preview writes with `--dry-run --json`
4. Apply writes with `--json`
5. Inspect exit codes plus `operation`, `receipt`, and `error.details` for retries or reconciliation

Use `--text` only for human-readable terminal inspection. Use `--profile human-debug --interactive` only for human/debug prompt flows. Agent-controlled runs should pass explicit flags, stdin, or file inputs.

Treat command surfaces in three buckets:

- `stable`: startup-contract or automation-contract surface
- `partial`: shared dry-run or machine-readable helper surface without a full stable contract
- `escape_hatch`: raw API or explicit human/debug-only escape hatch fallback

For concrete v2-to-v3 command fixes, see [../../docs/v2-to-v3-migration-cookbook.md](../../docs/v2-to-v3-migration-cookbook.md).
