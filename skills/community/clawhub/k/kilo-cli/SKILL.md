---
name: kilo-cli
description: Use the Kilo Code CLI for headless code generation and in-process LSP/file/ripgrep diagnostics. Wraps `kilo run` for one-shot delegated work and `kilo debug` for read-only code introspection.
homepage: https://kilo.ai/docs/code-with-ai/platforms/cli-reference
metadata: {'openclaw': {'requires': {'bins': ['kilo']}}}
---

# kilo-cli — headless Kilo Code CLI for coding agents

`kilo` is a Node.js CLI from Kilo Code that ships an interactive TUI, an ACP server, and a non-interactive `run` mode. This skill covers the coding surface only — `kilo run` for one-shot delegated work and `kilo debug` for read-only LSP / ripgrep / file introspection. TUI, ACP server, auth, MCP, agent creation, upgrade, and uninstall paths are out of scope.

Run `kilo <subcommand> --help` for the per-subcommand flag reference when needed.

## Verify it's wired

```bash
command -v kilo              # on PATH
kilo --version               # version string
kilo run --help              # headless usage renders
```

## Headless delegation: `kilo run`

The primary use case — kick off a coding task and consume the result without a TUI.

```bash
kilo run "fix the failing test in src/foo.ts" \
    --dir /path/to/project \
    --format json
```

Key flags:

| Flag                       | Effect                                                                              |
| -------------------------- | ----------------------------------------------------------------------------------- |
| `--dir PATH`               | Working directory. Required for non-interactive delegation.                         |
| `--format {default,json}`  | `json` for pipe-clean agent consumption; `default` for human-readable.              |
| `--model PROVIDER/MODEL`   | Override the default model for this run.                                            |
| `--agent NAME`             | Use a specific agent definition.                                                    |
| `--variant {high,max,...}` | Provider-specific reasoning effort.                                                 |
| `-c, --continue`           | Continue the most recent session.                                                   |
| `-s, --session ID --fork`  | Continue a specific session, optionally forking first.                              |
| `--title TITLE`            | Label the session (truncated prompt if no value).                                   |
| `-f, --file PATH`          | Attach files to the message.                                                        |
| `--thinking`               | Surface reasoning blocks.                                                           |
| `--auto`                   | Auto-approve non-denied permissions (dangerous — see _Common gotchas_).             |
| `--command CMD`            | Run a specific command; the `message` becomes the args.                             |
| `--share`                  | Share the session via a generated URL.                                              |
| `--cloud-fork`             | Fetch the named session from the cloud and continue locally (requires `--session`). |
| `--port PORT`              | Local server port when not using `--attach` (defaults to random).                   |

## In-process diagnostics: `kilo debug`

Read-only LSP, ripgrep, and file introspection — useful when an agent wants kilo's indexed view of a workspace without delegating work.

| Subcommand                              | What it returns                       |
| --------------------------------------- | ------------------------------------- |
| `kilo debug lsp diagnostics <file>`     | LSP diagnostics for one file.         |
| `kilo debug lsp symbols <query>`        | Workspace symbol search.              |
| `kilo debug lsp document-symbols <uri>` | Symbols in a specific document.       |
| `kilo debug rg search <pattern>`        | ripgrep-backed content search.        |
| `kilo debug rg files --query <q>`       | ripgrep-backed file listing by query. |
| `kilo debug file read <path>`           | File contents as JSON.                |
| `kilo debug file list <path>`           | Directory listing.                    |
| `kilo debug file search <q>`            | File search by query.                 |

## Exit codes

`kilo run` propagates the underlying agent's exit code; the `--format json` output on stdout is parseable regardless. Other subcommands exit `0` on success and non-zero on usage / config / transport errors. For control flow, check the exit code rather than parsing stderr.

## Output contract

- **stdout** = data (`--format json` payload, diagnostic JSON, lists).
- **stderr** = progress, warnings, and error messages.

`... | jq` is pipe-clean on `kilo run --format json` and on the JSON-producing `kilo debug` subcommands.

## Recipes

| Intent                                      | Command                                                                    |
| ------------------------------------------- | -------------------------------------------------------------------------- |
| Headless one-shot, parseable output         | `kilo run "$prompt" --dir "$project" --format json`                        |
| Continue the most recent session            | `kilo run "$prompt" --continue --format json`                              |
| Branch off a specific session               | `kilo run "$prompt" --session ID --fork --format json`                     |
| Pull a session from the cloud, branch first | `kilo run "$prompt" --session ID --cloud-fork --format json`               |
| Override the model for one run              | `kilo run "$prompt" --dir "$project" --model PROVIDER/MODEL --format json` |
| More reasoning effort                       | `kilo run "$prompt" --dir "$project" --variant max --format json`          |
| Send to an already-running `kilo serve`     | `kilo run "$prompt" --attach http://localhost:4096 --format json`          |
| LSP errors on one file before commit        | `kilo debug lsp diagnostics path/to/file`                                  |
| Find a symbol by name across the workspace  | `kilo debug lsp symbols "MyClass"`                                         |
| List symbols in a specific document         | `kilo debug lsp document-symbols file:///abs/path/to/file`                 |
| Content search (with ripgrep indexing)      | `kilo debug rg search "TODO" --limit 50`                                   |
| File listing by query                       | `kilo debug rg files --query "*.test.ts"`                                  |

## Common gotchas

- **`kilo run` without `--format json` prints human-friendly output.** For pipelines, always pass `--format json` and parse stdout.
- **`--auto` is dangerous.** It auto-approves every permission not explicitly denied, including shell execution. Use only in disposable sandboxes.
- **Cwd matters.** `kilo run` reads `--dir` for the working dir; omit it and the call falls back to the parent's cwd, which is rarely what you want.
- **TUI / ACP / auth / MCP / agent-create / upgrade / uninstall paths are not in this skill.** Hand them to a human operator or gate them behind explicit per-call approval.
