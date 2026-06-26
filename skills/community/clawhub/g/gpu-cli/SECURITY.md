# Security Model — GPU CLI Skill

## Threat Model

This skill executes `gpu` CLI commands on the user's local machine via a guarded wrapper (`runner.sh`). The threat model assumes:

- **Trusted**: The local `gpu` binary, the user's OS environment, ClawHub's sandbox
- **Untrusted**: Agent-generated command strings (may contain injection attempts)

The skill does **not** handle credentials, secrets, or network connections directly — all of that is delegated to the `gpu` binary, which manages its own authentication and encrypted transport.

## Input Sanitization

All agent-supplied input passes through three validation layers before execution:

1. **Prefix check** — command must start with `gpu ` (rejects arbitrary binaries)
2. **Character blocklist** — rejects commands containing shell metacharacters:
   `;`, `&`, `|`, `` ` ``, `(`, `)`, `>`, `<`, `$`, `{`, `}`, and embedded newlines.
   This prevents chaining, redirection, subshells, and variable expansion.
3. **Subcommand allowlist** — only explicitly permitted `gpu` subcommands are accepted:
   `run`, `status`, `doctor`, `logs`, `attach`, `stop`, `inventory`, `config`, `auth`, `daemon`, `volume`, `llm`, `comfyui`, `notebook`

### Direct Execution (No Shell Re-evaluation)

The validated command is split into an argument array and executed via `gpu "${CMD_ARGS[@]}"` — **not** passed through `bash -c` or `eval`. This eliminates shell re-evaluation as an attack vector entirely.

## Permission Minimality

| Permission | Scope | Rationale |
|------------|-------|-----------|
| `Bash(runner.sh*)` | Only the bundled runner script | Cannot execute arbitrary shell commands |
| `Read` | Workspace files | Needed to inspect config files and logs |
| `network: false` | No network access | The `gpu` binary handles its own networking |
| `filesystem: workspace` | Current workspace only | Cannot access files outside the project |

## What This Skill Does NOT Do

- **No credential handling** — does not read, store, or transmit API keys or tokens
- **No obfuscated code** — all logic is in plain Bash, fully auditable
- **No network access** — the skill itself requests no network permissions
- **No persistent state** — no files written, no background processes spawned
- **No privilege escalation** — runs as the current user with no elevated permissions

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General failure |
| 2 | Input validation failure (bad command, missing binary) |
| 4 | Blocked by policy (dry-run, confirmation required, price cap exceeded) |
| 10–15 | GPU CLI-specific errors (auth, quota, resource, daemon, timeout, cancel) |

## Responsible Disclosure

If you discover a security issue in this skill, please report it to:
- **Email**: security@gpu-cli.sh
- **GitHub**: https://github.com/gpu-cli/gpu/security/advisories

## Version History

| Version | Security Changes |
|---------|-----------------|
| 1.2.0 | Expanded injection blocklist (`$`, `{}`, newlines); direct exec replaces `bash -c`; exit code 4 for policy blocks |
| 1.1.1 | Initial release with basic injection protection |
