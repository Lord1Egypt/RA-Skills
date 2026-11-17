---
name: lyra-brain
description: "LYRA 3-Brain local memory (working/library/outer). Explicit only: user must ask to log, grow, or recall on disk. Writes under LYRA_CORE_ROOT/memory after --i-consent. No secrets. No auto-publish. Not for casual chat. Read references/SECURITY.md first."
version: 2.1.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🧠"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
    requires:
      anyBins: [python, python3]
  lygo: true
  lyra: true
  memory: true
  p0: true
  signature: "Δ9Φ963-LYRA-BRAIN-v2.1.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lyra-brain"
  security_audit: "skillspector-2026-07-29-v2.1.0"
  permissions_declared:
    filesystem_read: "LYRA_CORE_ROOT modules + memory (user-set path)"
    filesystem_write: "LYRA_CORE_ROOT/memory and graph only with --i-consent"
    env: "LYRA_CORE_ROOT or LYRA_CORE (path only, never secrets)"
    network: false
    process_spawn: false
    shell: false
    social_autopublish: false
    git_push: false
---

# LYRA 3-Brain Memory v2.1.0

## ⚠️ Persistent local storage (read before use)

This skill can **write files on disk** under a tree you choose with `LYRA_CORE_ROOT`:

- `memory/YYYY-MM-DD.md` — daily index  
- `memory/YYYY-MM-DD-<slug>.md` — topic snips  
- `memory/reference/*.ref.txt` — outer pointers  
- `lyra_brain_graph.json` (via grow) — graph growth  

**Data can outlive the chat session.** Do not grow secrets, tokens, private keys, or personal data you would not store on that machine.  

**Disable / delete:** stop calling write CLIs; delete or move files under `$LYRA_CORE_ROOT/memory` (and graph file) yourself — this skill never auto-wipes.  

**Consent:** write CLIs require **`--i-consent`**. Agents must **not** log or grow unless the user explicitly asks to remember / log / grow / recall **from disk**.

---

## When to load this skill (narrow triggers)

Load **only** when the user clearly wants **disk memory** or 3-brain ops, for example:

- “log this session to lyra-brain” / “write a daily snip”  
- “grow into the 3-brain graph”  
- “recall from LYRA memory” / “brain_recall …”  
- “run session_log_snip” / “3-brain memory”  

**Do not** activate for casual “remember that…” in conversation-only context, or for “log” meaning application logging. Prefer **in-chat notes** unless the user asks for **persistent** memory.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lyra-brain
export LYRA_CORE_ROOT=/absolute/path/to/LYRA_CORE   # must contain modules/lyra_brain.py
```

`LYRA_CORE_ROOT` is **required**. Scripts do not guess other users’ home trees without that env (or explicit flag).

Read: `references/SECURITY.md` · `references/AGENT_CONTRACT.md` · `references/MEMORY_LAYOUT.md`

---

## Three brains (model)

| Brain | What | Where |
|-------|------|--------|
| **Working** | Session RAM | Runner only (not this skill’s disk) |
| **Library** | Grown nodes, seals | graph + daily md under `LYRA_CORE_ROOT` |
| **Outer** | URLs, IDs, merkle pointers | `memory/reference/*.ref.txt`, topic snips |

---

## Write commands (consent required)

### Session snip

```bash
cd scripts
python session_log_snip.py --i-consent --slug moltx-hub --title "Moltx hub thread" \
  --lines "root 6073bbc0" "how map 68ebf941" --grow --ref-to MOLTX_HOW
```

Without `--i-consent` the script **refuses** to write.

### Grow / recall

```bash
python brain_grow_cli.py --i-consent "2026-07-03 COMPLETE: lattice ALIGNED …"
python brain_recall_cli.py "Moltx how it works" --limit 5
# recall is read-only — no --i-consent required
```

---

## Interactive runner (full power — outside skill package)

```bash
cd "$LYRA_CORE_ROOT"
python -B lyra_boot.py
```

| Command | Action |
|---------|--------|
| `brain_grow <text>` | Ingest → P0/Oath → graph |
| `brain_recall <q>` | Keyword/tag recall |
| `brain_heartbeat` | Guardian + prune weak edges |

---

## Agent rules

1. **Ask first** before any disk write / grow.  
2. Snips = small DONE facts (ids, urls, paths, merkle) — no essays.  
3. **No secrets** in memory or grow text.  
4. No auto git / HF / ClawHub / social publish.  
5. Do not claim **LATTICE ALIGNED** without stack verify.  
6. Do not treat vague “remember” as consent to write disk memory.

## Skill chain

`lygo-protocol-stack-operator` → **`lyra-brain`** ↔ `lyra-open-claw` → `lygo-ollama-army`

## Version

| Ver | Change |
|-----|--------|
| 2.0.0 | ClawHub public mirror |
| **2.1.0** | Explicit permissions; narrow triggers; persistent-storage warnings; `--i-consent` on writes; require `LYRA_CORE_ROOT` |

**Δ9Φ963 — remember with consent and refs, not fear.**
