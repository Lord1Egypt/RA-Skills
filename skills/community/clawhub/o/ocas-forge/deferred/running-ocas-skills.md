# Deferred: belongs in a runtime-harness skill, not in ocas-forge. Content preserved here until a proper home is created.

This content describes how the agent **runs** and **delegates** OCAS skills — toolset inheritance, MCP traps, cron scheduling, venv setup, and verification of external side effects. That is runtime-harness guidance (concerns of the orchestration layer, not the skill builder). It was removed from `ocas-forge/SKILL.md` during the 2026-04 refactor and is kept here so the material isn't lost until a proper runtime-harness skill is created.

---

## Running OCAS skills correctly

How to correctly execute OCAS skills — manually, via delegation, and via cron.

### Rules

1. **NEVER write a throwaway Python script to implement logic that a skill's SKILL.md already documents.** Run the skill as-is through the agent's orchestration layer. Skills are declarative specifications executed by the LLM — they are not Python packages with executable code.

2. **NEVER use `cronjob run` when the user says "run X now."** That triggers a cron schedule, not an immediate execution. Use `delegate_task` with the skill loaded (or run the logic directly if you have the tools).

3. **When delegating an OCAS skill that depends on MCP tools (mempalace, spotify, etc.), you MUST either:**
   - Omit the `toolsets` parameter entirely so the child inherits ALL parent tools including MCP, OR
   - Explicitly include the MCP toolset (e.g., `mcp-mempalace`) in the toolsets list.

   If you pass only toolsets like `["terminal", "file", "web"]`, MCP tools are excluded and the subagent will **simulate or hallucinate** writes instead of performing them. This is the #1 cause of "ran but nothing happened" failures.

4. **The cron scheduler creates AIAgent instances with `disabled_toolsets=["cronjob", "messaging", "clarify"]`** only. This means cron jobs inherit all other tools including MCP — they will work correctly IF the MCP server's command path is correct.

5. **When a sub-agent or cron job reports a "tool issue" or "permission error", 99% of the time it's because you gave it the wrong toolsets.** Do NOT assume the tool itself is broken. Check toolset inheritance first.

### Verification after skill runs

After running a skill that writes to an external store (MemPalace, Weave, etc.):

1. Check the store directly — not just the skill's journal. Journal writes mean nothing if the external call failed silently.
2. For MemPalace: `mempalace status` (check drawer count), `mempalace search "<expected content>"`, and `~/.mempalace/wal/write_log.jsonl` (check recent timestamp).
3. For the skill's own files: check `ingestion_log.jsonl` and `decisions.jsonl` in the data directory to confirm the processing cursor advanced.

### Delegate task pattern

```
delegate_task(
  goal="...",
  skills=["ocas-<skill-name>"],  # loads the SKILL.md
  # NO toolsets parameter — inherits all parent tools including MCP
)
```

If you must restrict toolsets, always include the MCP server the skill needs:
```
toolsets=["terminal", "file", "mcp-mempalace"]  # explicit MCP inclusion
```

---

## Runtime setup (venv, cron, data files)

Much of what `ocas-skill-initialization` described is actually runtime-harness work — creating the venv, touching JSONL files on disk, registering cron jobs. A skill package should not prescribe this; the harness that installs the skill should. Preserved here pending a proper home.

### Verify skill state

```bash
ls -la ~/.hermes/commons/data/{skill-name}/
cat ~/.hermes/commons/data/{skill-name}/config.json
ls -la ~/.hermes/commons/data/{skill-name}/*.jsonl
hermes cron list | grep {skill-name}
```

### Create directory structure

```bash
mkdir -p ~/.hermes/commons/data/{skill-name}/
mkdir -p ~/.hermes/commons/data/{skill-name}/reports/
mkdir -p ~/.hermes/commons/journals/{skill-name}/
```

### Create JSONL data files

```bash
cd ~/.hermes/commons/data/{skill-name}/
touch signals.jsonl items.jsonl links.jsonl decisions.jsonl extractions.jsonl
```

Common JSONL files:
- `signals.jsonl` — Consumption or activity signals
- `items.jsonl` — Item records (entities, tracks, venues)
- `links.jsonl` — Cross-domain connections
- `decisions.jsonl` — Decision records
- `extractions.jsonl` — Raw extractions from external sources

### Python virtual environment

```bash
cd ~/.hermes/commons/data/{skill-name}/
apt update && apt install -y python3.13-venv
python3 -m venv venv
source venv/bin/activate
pip install {dependency1} {dependency2}
```

### Scripts directory

```bash
mkdir -p ~/.hermes/commons/data/{skill-name}/scripts/
chmod +x ~/.hermes/commons/data/{skill-name}/scripts/*.py
```

### Register cron jobs

```bash
hermes cron create --name {skill-name}:task --skill {skill-name} "0 6 * * *" "command"
hermes cron create --name {skill-name}:scan --skill {skill-name} "0 6 * * *" "cd <hermes-home>/commons/data/{skill-name} && source venv/bin/activate && python3 scripts/scan.py"
```

### Common pitfalls

1. **Incomplete config**: write full config with all default fields from skill spec
2. **Missing JSONL files**: create all required JSONL files with `touch`
3. **Venv installation fails**: install the venv package first (`apt install python3.13-venv`)
4. **Cron job syntax errors**: use proper `hermes cron create` syntax with `--name`, `--skill`, schedule, and command

### Verification checklist

- [ ] Data directory exists: `~/.hermes/commons/data/{skill-name}/`
- [ ] Full config.json with all fields
- [ ] All JSONL files created (empty is OK)
- [ ] Subdirectories created (reports/, etc.)
- [ ] Python venv created and dependencies installed
- [ ] Scripts directory exists and scripts are executable
- [ ] Cron jobs registered and visible in `hermes cron list`
- [ ] Manual test run succeeds