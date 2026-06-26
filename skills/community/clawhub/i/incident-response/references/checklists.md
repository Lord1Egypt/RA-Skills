# Quick Diagnosis Checklists

## Gateway Crash

1. `launchctl list | grep openclaw` — exit code 0 (running) or 1 (crashed)?
2. `tail -30 ~/.openclaw/logs/gateway.err.log | grep -E 'Unrecognized|invalid|Error'`
3. `openclaw doctor` — lists all invalid keys
4. If `Unrecognized key: X` → check what changed: `git log --oneline -5`
5. `openclaw doctor --fix` → restarts automatically
6. If doctor fails → restore from backup: `config-validate.sh --merge < good-backup.json`

**Common causes ranked:**
- Invalid key at wrong schema level (account vs guild vs channel)
- `env` key added to agents.list (not a valid key)
- `agents.list` wiped by `config.patch` that included full array

## Binding Loss

1. Count current bindings: `python3 -c "import json; d=json.load(open('openclaw.json')); print(len(d.get('bindings',[])))"
2. Check config-backups timeline (see Phase 1 script in SKILL.md)
3. Find the drop timestamp — that's your incident window
4. Check which session was active at that time: `ls -lt ~/.openclaw/agents/main/sessions/*.jsonl`
5. Search that session for gateway config.apply or direct file writes
6. Restore from backup at timestamp just before the drop

**Prevention:** binding count guard in config-validate.sh --merge (see prevention-patterns.md Pattern 1)

## Config Key Disappeared

1. `grep -r "KEYNAME" ~/.openclaw/config-backups/` — find when it was last present
2. `cd ~/.openclaw && git log --all -p -- openclaw.json | grep "KEYNAME"` — find commit that removed it
3. Check git commit author — which agent/session
4. Add back via: `echo '{"key":"value"}' | config-validate.sh --merge`

**Most common cause:** A config.patch that wrote a partial config, replacing entire sections.

## Agent Routing Wrong (Wrong Agent Responding)

1. `/status` in the channel — shows `agent:ID:discord:channel:CHANNEL_ID`
2. Check bindings: `python3 -c "import json; [print(b) for b in json.load(open('openclaw.json')).get('bindings',[])]"`
3. Find missing binding → add via Python + config-validate.sh --merge
4. Restart gateway

**Note:** `Activation: mention` in /status = slash command triggered it, not a routing config issue.

## Vector Search Not Finding Content

1. `openclaw memory status` — check indexed count vs total files
2. If indexed << total: `openclaw memory index --force --agent AGENT_ID`
3. If stuck: delete sqlite → `rm ~/.openclaw/memory/AGENT.sqlite` → restart gateway
4. Check config: `python3 -c "import json; d=json.load(open('openclaw.json')); print(d['agents']['defaults'].get('memorySearch',{}))"`
5. Verify `sources: ["memory","sessions"]` and `extraPaths` are present

**Common cause:** Config was replaced without `memorySearch` block → defaults back to memory-only.

## Session Orphaned Tool Calls (LLM request rejected)

Error: `` `tool_use` ids were found without `tool_result` blocks ``

```bash
# Find session file
python3 -c "import json; s=json.load(open('~/.openclaw/agents/AGENT/sessions/sessions.json')); print(s.get('agent:AGENT:discord:channel:CHANNEL_ID'))"

# Reset session
mv ~/.openclaw/agents/AGENT/sessions/SESSION.jsonl \
   ~/.openclaw/agents/AGENT/sessions/SESSION.jsonl.reset.$(date -u +%Y-%m-%dT%H-%M-%S.000Z)
```

**Cause:** Session interrupted mid-tool-call (gateway crash, timeout). History has tool_use with no result.
