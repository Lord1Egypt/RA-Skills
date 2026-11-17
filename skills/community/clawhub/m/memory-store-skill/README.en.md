# Memory Store Skill

[中文](README.zh.md)

**Structured memory for multi-session, multi-agent workflows.**

The agent identifies durable decisions, fixes, preferences, workflows, and state. A zero-dependency Node.js CLI validates, stores, retrieves, archives, and restores them. There is no daemon and no background transcript scanner.

Read the [security model](SECURITY.md) before installation. The package has no install lifecycle hook, background process, or automatic network request, and `private` is not an encryption boundary.

## Installation

Node.js 18 or newer is required. The current release is available on npm:

```bash
npm i memory-store-skill
npx memory-store setup --agent codex --mode explicit
```

Installing the npm package does not run lifecycle hooks or modify Agent directories. The explicit second command installs the skill for Codex. Start a new Agent session afterward so the platform can discover it.

Verify the installation:

```bash
npx memory-store version
```

To inspect platform identifiers or install for another platform:

```bash
npx memory-store setup --list
npx memory-store setup --agent codex
```

Other identifiers include `claude`, `gemini`, `opencode`, `workbuddy`, `cursor`, `windsurf`, `qoderworkcn`, and `trae-cn`.

### Memory profiles

| Profile | Behavior |
|---|---|
| `off` | No automatic recall or storage; explicit commands remain available |
| `explicit` | Respond only to explicit remember/recall requests; safe default |
| `balanced` | Automatically retain selected decisions, fixes, workflows, and preferences; up to 3 per conversation |
| `proactive` | Automatically retain a broader set of durable memories; up to 5 per conversation |

Inspect or change the global profile after installation, or add a workspace override:

```bash
npx memory-store mode
npx memory-store mode balanced --global
npx memory-store mode explicit --workspace
npx memory-store mode --reset --workspace
```

## Update

```bash
npm i memory-store-skill@latest
npx memory-store setup --sync
```

The first command explicitly upgrades the npm package. The updater then syncs only existing skill installations from that local package, verifies the copied files, and leaves memory data unchanged. It does not download or execute remote code or turn an uninstalled platform into a new installation.

```bash
# Preview without writing
npx memory-store setup --sync --dry-run

# Update one platform
npx memory-store setup --sync --agent codex

# Update a custom installation directory
npx memory-store setup --sync --target /path/to/memory-store
```

Start a new Agent session after updating. Source users can run `node scripts/install.js --update` in the repository to refresh existing installations from the current source.

### Install from source

Use the source route for development, source inspection, or unreleased changes:

```bash
git clone https://github.com/Revolves/memory-store-skill.git
cd memory-store-skill
node scripts/install.js --all
```

## Core model

| Dimension | Value | Intended use |
|---|---|---|
| scope | `global` | stable cross-project preferences and knowledge |
| scope | `workspace` | project decisions, progress, fixes, and handoffs |
| visibility | `global` | cross-project cooperative visibility |
| visibility | `shared` | workspace cooperative visibility |
| visibility | `private` | returned by the CLI only to the matching `owner_agent` |

> `private` is an agent-identity cooperation filter, not encryption. The JSON files are plaintext and remain readable to users or processes with filesystem access. The CLI does not detect or redact credentials, tokens, keys, or personal information. Do not store secrets.

Eight memory types are supported: `fact`, `decision`, `preference`, `workflow`, `debug_solution`, `state`, `event`, and `relation`.

## Five-minute quick start

The examples below use the npm CLI and do not require entering the installed skill directory.

### 1. Open the guided terminal

```bash
npx memory-store
```

With a real terminal, the no-argument command opens a numbered menu for setup, search, adding memories, profile changes, status, and maintenance preview. Every write shows a summary and defaults to cancellation. Without a TTY it prints compact help and exits without waiting.

### 2. Store a workspace decision

```bash
npx memory-store remember decision "Database choice" "Use SQLite for the local single-user deployment" --workspace
```

### 3. Search

```bash
npx memory-store recall "database choice" --json
```

JSON is written to stdout by default; `--stdout` is only the explicit form. Use `--output result.json` when a file is useful.

### 4. Inspect status

```bash
npx memory-store status
```

Agents and CI can call `remember`, `recall`, `mode`, and `status` directly; explicit commands never open the menu. The compatible low-level interface remains available through `npx memory-store help --advanced`.

## When an agent should search

- **Required:** the user asks about prior discussion, decisions, progress, preferences, conventions, or debugging history; or another agent takes over the task.
- **As needed:** a new session clearly continues existing work, or the current context lacks historical rationale.
- **Skip:** a self-contained one-off request with no historical dependency.

Platform working memory does not replace a targeted search for specific history. If the memory store has no relevant result, inspect project evidence next and identify the source.

## Commands

| Command | Purpose |
|---|---|
| `remember` | add a memory with safe defaults |
| `recall` | search by text or inspect a `mem_...` ID |
| `mode` | inspect or change the memory profile |
| `status` | show version, profile, paths, and counts |
| `setup` | explicitly install or sync the local package |
| `maintain` | preview archive candidates; mutate only with `--apply` |

See [references/cli.md](references/cli.md) for exact options and [references/operations.md](references/operations.md) for lifecycle, privacy, concurrency, backup, and recovery boundaries.

## Important limitations

- Atomic replacement prevents half-written files and temporary-name collisions, but there is no transaction lock around the full read-modify-write cycle. Concurrent writers can still cause a last-write-wins lost update.
- `archive --scope all` processes both stores; use separate runs when they need different thresholds. Inspect and restore with `list --status archived`, `recall`, and `restore`.
- Corrupt JSON causes a non-zero failure and must not be treated as an empty store.
- `compress` extracts candidates; it does not perform semantic summarization or sensitive-data detection.
- Performance varies with hardware, Node.js version, disk, and store size. Benchmark your own workload.

## Documentation

- [SKILL.md](SKILL.md): minimal agent behavior
- [CHEATSHEET.md](CHEATSHEET.md): one-page command reference
- [FAQ.md](FAQ.md): common questions and boundaries

## License

MIT License.
