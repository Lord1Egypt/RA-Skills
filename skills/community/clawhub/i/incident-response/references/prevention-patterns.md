# Prevention Patterns

## Pattern 1: Config Field Guard (config-validate.sh)

Use when a config field must not decrease/disappear silently.

Add to the `--merge` block in `config-validate.sh`, before `apply`:

```bash
# Guard: block if <field> count decreases
curr_count=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(len(d.get('FIELD', [])))" 2>/dev/null || echo 0)
new_count=$(python3 -c "import json; d=json.load(open('$merged')); print(len(d.get('FIELD', [])))" 2>/dev/null || echo 0)
if [ "$new_count" -lt "$curr_count" ]; then
    echo "❌ BLOCKED: FIELD count would drop $curr_count → $new_count."
    echo "   Add fields explicitly via --merge. To force, use --apply directly."
    rm -f "$merged"
    exit 1
fi
```

**Real example:** Binding guard added 2026-03-04 after bindings dropped 17→1.

## Pattern 2: SOUL.md Hard Rule

Use when an agent repeatedly makes the same mistake autonomously.

```markdown
## [Area] — Hard Restriction (HR-NNN)

**NEVER [do X].** This causes [Y consequence].

- Correct approach: [what to do instead]
- Why: [root cause context]
- Learned: [date] — [brief incident description]
```

**Real examples:**
- HR-008: Validate schema before writing any config key
- HR-009: Config change process — always use config-validate.sh --merge
- HR-010: No self-restart or self-config (revoked after 3 incidents)

## Pattern 3: rules.md Hard Rule

Use when the agent needs a persistent system-wide rule.

File: `~/.openclaw/learnings/rules.md`

```markdown
### HR-NNN: [Title]
[What happened] — [date]
**Rule:** [Imperative statement of what to always/never do]
- **Trigger:** [When this applies]
- **Action:** [What to do]
- **Learned:** [date + incident summary]
```

## Pattern 4: Git Audit Enforcement

Use when config changes are being made without traceability.

```bash
# Add to config-validate.sh apply() function, after writing the file:
(
    cd ~/.openclaw && git add openclaw.json 2>/dev/null && \
    ACTOR="${OPENCLAW_AGENT_ID:-${USER:-unknown}}" && \
    TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)" && \
    git diff --cached --quiet 2>/dev/null || \
    git commit -m "config: ${TIMESTAMP} by ${ACTOR}" --quiet 2>/dev/null
) || true
```

This gives full actor+timestamp+diff for every change.

## Pattern 5: Valid Keys Guard

Use when agents write invalid config keys (causing gateway crashes).

Add to `config-validate.sh` validate() function:
```python
# Valid account-level keys (check schema via DeepWiki before updating)
valid_acct_keys = set(['token', 'groupPolicy', 'streaming', 'dmPolicy', 'allowFrom', 'guilds', 'dm'])
for key in acct.keys():
    if key not in valid_acct_keys:
        print(f"Invalid account key: {key}", file=sys.stderr)
        sys.exit(1)
```

**Always verify against DeepWiki before adding to valid_keys list:**
```bash
~/.openclaw/skills/deepwiki/scripts/deepwiki.sh ask openclaw/openclaw "valid config keys for channels.discord.accounts"
```

## Pattern 6: Chmod Protection

Use for critical config files on multi-agent machines.

```bash
chmod 444 ~/.openclaw/openclaw.json  # read-only; config-validate.sh handles unlock/relock
```

Prevents direct writes; forces all changes through config-validate.sh which has guards.
**Note:** Adapt chmod strategy to your machine setup — some setups give specific agents controlled self-modify rights.
