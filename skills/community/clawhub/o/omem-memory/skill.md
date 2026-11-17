---
name: omem-memory
description: "Trustworthy, self-hosted memory for your agent: remember facts as beliefs with provenance, keep both sides when facts conflict instead of silently overwriting, check the belief state of any claim (BELIEVED_TRUE / CONTRADICTED / UNKNOWN), and prove why anything is believed with an evidence chain. Use when the agent needs to remember something across sessions, check what it knows about a person or entity, detect contradictory information, or produce an audit trail of what it believed and why. All data stays on the user's own OMEM server; this skill phones home to nobody."
metadata:
  openclaw:
    requires:
      env:
        - OMEM_API_KEY
        - OMEM_PROJECT
---

# OMEM memory

Belief-revision memory for this agent, backed by the user's own self-hosted
OMEM server (open source, MIT). Unlike a note file or a vector store, OMEM
keeps both sides when facts conflict, tracks what was believed and when, and
can prove why anything is believed. That makes it memory you can audit, which
matters when this agent acts on someone's behalf.

Security note, worth reading once: this skill is a single stdlib-only Python
script with no dependencies. Its only network calls go to the OMEM server the
user configured in `OMEM_BASE_URL` (their own machine by default). Every line
is in `scripts/omem.py` and takes two minutes to read.

## Setup (once)

The user runs their own server (no account, no cloud):

```bash
pip install omem-infrastructure
omem-server
```

The first run prints an API key and a project id. Set these in the OpenClaw
environment:

```
OMEM_BASE_URL=http://127.0.0.1:8787
OMEM_API_KEY=omem_sk_...
OMEM_PROJECT=proj_...
OMEM_AGENT=openclaw
```

If `OMEM_API_KEY` is not set, tell the user to run the two commands above and
paste the printed key; do not guess or fabricate credentials.

## When to use which command

All commands print JSON. Run them with `python scripts/omem.py ...` from this
skill's directory.

**Remember a fact the user states or you conclude** (a durable belief, not
scratch state):

```bash
python scripts/omem.py remember --about "customer:alice" \
  --claim "prefers_annual_billing" --note "Said in the 2026-09-01 call"
```

Claims are lowercase tokens with underscores. To assert the opposite of a
claim, use the `not:` prefix: `--claim "not:prefers_annual_billing"`.

**Before acting on a remembered fact, check its state** (this is the step
that catches contradictions instead of acting on stale or disputed data):

```bash
python scripts/omem.py believes --about "customer:alice" \
  --claim "prefers_annual_billing"
```

The state is one of BELIEVED_TRUE, BELIEVED_FALSE, CONTRADICTED, UNKNOWN.
Treat CONTRADICTED as "do not act on this without asking the user": the
record holds conflicting information from different sources, and OMEM
deliberately refuses to pick a winner for you.

**Recall what is known about an entity** (including as of a past moment):

```bash
python scripts/omem.py recall --about "customer:alice" --limit 10
python scripts/omem.py recall --about "customer:alice" --as-of "2026-08-25T14:00:00Z"
```

**Prove why something is believed** (the audit trail; each assertion id comes
back from remember, learn, and recall):

```bash
python scripts/omem.py why --id a_1b2c3d4e
```

**List everything currently in dispute:**

```bash
python scripts/omem.py conflicts
```

**Feed free text and let the engine decide what becomes memory** (safer than
remember when the source is a document or message rather than a clear fact):

```bash
python scripts/omem.py observe --text "Alice mentioned she prefers email over calls."
python scripts/omem.py learn --text "The customer wants to upgrade to enterprise." --about "customer:alice"
```

## Rules for this agent

- Remember durable facts about people, entities, and preferences; do not
  remember secrets, credentials, or one-off scratch values.
- Check `believes` before acting on a remembered fact; surface CONTRADICTED
  states to the user instead of resolving them silently.
- When the user asks "why do you think that", run `why` and answer from the
  evidence chain rather than from confidence.
- Never send memory content anywhere except the configured OMEM server.
