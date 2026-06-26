# Install

## Prerequisites

- OpenClaw installed and running
- An Obsidian vault (or willingness to create one)
- Python 3 (for the install script's job setup, if OpenClaw CLI is unavailable)

## Option 1: ClawHub

```bash
npx clawhub@latest install memory-keep-alive-for-obsidian
```

This installs the skill to `~/.openclaw/skills/memory-keep-alive-for-obsidian/`.

After installing from ClawHub, you still need to:

1. **Set up your Obsidian vault:**
   ```bash
   mkdir -p "$HOME/Documents/Obsidian Vault/Tasks/Session-Resume-Workflow"
   ```

2. **Copy the templates into your vault:**
   ```bash
   SKILL_DIR="$HOME/.openclaw/skills/memory-keep-alive-for-obsidian"
   TASKS_DIR="$HOME/Documents/Obsidian Vault/Tasks/Session-Resume-Workflow"
   cp "$SKILL_DIR/templates/TEMPLATE.md" "$TASKS_DIR/"
   cp "$SKILL_DIR/templates/LOOP-STATE.md" "$TASKS_DIR/"
   cp "$SKILL_DIR/examples/WORKFLOW-INDEX.md" "$TASKS_DIR/"
   ```

3. **Add the 5 cron jobs** (replace the vault path with yours):
   ```bash
   openclaw cron add --name "keep-alive-watchdog" --cron "*/15 * * * *" --session isolated --message "Run the watchdog. Vault: $HOME/Documents/Obsidian Vault"
   openclaw cron add --name "keep-alive-replayer" --cron "*/30 * * * *" --session isolated --message "Run the replayer. Vault: $HOME/Documents/Obsidian Vault"
   openclaw cron add --name "keep-alive-escalator" --cron "0 * * * *" --session isolated --message "Run the escalator. Vault: $HOME/Documents/Obsidian Vault"
   openclaw cron add --name "memory-validator" --cron "5 * * * *" --session isolated --message "Run the validator. Vault: $HOME/Documents/Obsidian Vault"
   openclaw cron add --name "memory-smoke-test" --cron "0 */6 * * *" --session isolated --message "Run the smoke test. Vault: $HOME/Documents/Obsidian Vault"
   ```

## Option 2: Git clone + install script

```bash
git clone https://github.com/TechieTer/openclaw-memory-keep-alive-for-obsidian.git
cd openclaw-memory-keep-alive-for-obsidian
./install.sh --vault "$HOME/Documents/Obsidian Vault"
```

This does everything:
1. Installs the skill to `~/.openclaw/skills/memory-keep-alive-for-obsidian/`
2. Creates `Tasks/Session-Resume-Workflow/` in your vault with the template, workflow index, and loop state marker
3. Adds all 5 cron jobs (uses `openclaw cron add` if available, otherwise merges into `jobs.json`)
4. Bakes your vault path into each job prompt automatically

Options:
- `--openclaw PATH` — OpenClaw home directory (default: `~/.openclaw`)

### What gets created

| What | Where |
|------|-------|
| Skill | `~/.openclaw/skills/memory-keep-alive-for-obsidian/SKILL.md` |
| Template | `<vault>/Tasks/Session-Resume-Workflow/TEMPLATE.md` |
| Workflow index | `<vault>/Tasks/Session-Resume-Workflow/WORKFLOW-INDEX.md` |
| Loop state | `<vault>/Tasks/Session-Resume-Workflow/LOOP-STATE.md` |

| Job | Schedule | Purpose |
|-----|----------|---------|
| `keep-alive-watchdog` | */15 * * * * | Detects stalls (only when loop armed) |
| `keep-alive-replayer` | */30 * * * * | Takes one step on stalled task (only when loop armed) |
| `keep-alive-escalator` | 0 * * * * | Forces restart on repeated stalls (only when loop armed) |
| `memory-validator` | 5 * * * * | Repairs missing notes, refreshes index (always runs) |
| `memory-smoke-test` | 0 */6 * * * | System health check (always runs) |

## Option 3: Manual install

1. Copy the `SKILL.md` file and `templates/`, `prompts/`, `examples/` directories into `~/.openclaw/skills/memory-keep-alive-for-obsidian/`.
2. Create `Tasks/Session-Resume-Workflow/` in your Obsidian vault.
3. Copy `templates/TEMPLATE.md`, `templates/LOOP-STATE.md`, and `examples/WORKFLOW-INDEX.md` into that folder.
4. Replace `VAULT_PATH` in each file under `prompts/` with your actual vault path.
5. Create the 5 cron jobs manually using `openclaw cron add` (see table above).

## How to use

**Task memory is automatic.** Once installed, your agent creates RESUME/CHECKLIST/DOCS notes for every task. The validator keeps them healthy. No action needed.

**The keep-alive loop is on-demand.** For long tasks:

1. `/loop-start` — arm the loop
2. Give your agent a task
3. Walk away — the loop keeps it alive
4. `/loop-stop` when done — stops burning tokens

For quick tasks, just let the memory handle it. No need to arm the loop.

## Verify

Ask your OpenClaw agent:

> Run the memory smoke test now.

It should return `smoke-test: pass` if everything is set up correctly.

## Uninstall

```bash
rm -rf ~/.openclaw/skills/memory-keep-alive-for-obsidian
# Then remove the 5 jobs (keep-alive-* and memory-*) using:
openclaw cron remove --name "keep-alive-watchdog"
openclaw cron remove --name "keep-alive-replayer"
openclaw cron remove --name "keep-alive-escalator"
openclaw cron remove --name "memory-validator"
openclaw cron remove --name "memory-smoke-test"
```

The Obsidian vault notes are yours to keep or delete.
