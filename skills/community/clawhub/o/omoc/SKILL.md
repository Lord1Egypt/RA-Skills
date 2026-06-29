---
name: "openclaw-ralph-suite"
description: "OMOC runtime for /goal, /ralplan, /team, /ralph, memory, leases, verifiers, and non-overlapping loops."
---

# OMOC - Oh My OpenClaw

OMOC is an OpenClaw-native port of the useful Oh My Codex workflow concepts. It is a runtime protocol plus helper scripts, not just trigger phrases.

OMOC composes:

- `/goal`: durable objective and story ledger
- `/ralplan`: Planner -> Architect -> Critic consensus planning
- `/team`: scheduler, workers, verifiers, tasks, leases, mailbox, loop/gate
- `/ralph`: bounded persistence and verification pressure
- `/neverstop`: non-overlapping hot-loop recurrence
- `/review`: independent completion gates
- memory: compact resumability so long workflows do not crash context

State lives under `.omoc/` with workflow, memory, goals, team, Ralph, and review artifacts. Use `scripts/omoc.py` for mutation.

Key commands:

```bash
python scripts/omoc.py compose init --objective "Ship X" --modes goal,ralplan,team,ralph
python scripts/omoc.py memory add --kind decision --text "..."
python scripts/omoc.py memory compact --max-events 50
python scripts/omoc.py goal init --brief "G001 implement\nG002 verify"
python scripts/omoc.py team init --name ship-x --task "Complete G001" --goal-id G001 --workers worker-1,verifier
python scripts/omoc.py team add-task --team ship-x --subject "Implement" --description "..." --role worker
python scripts/omoc.py team loop --team ship-x --goal-id G001
python scripts/omoc.py team gate --team ship-x --goal-id G001
python scripts/omoc.py ralph init --loop-id ship-x --objective "Drive ship-x to goal completion"
```

`/team` is not ordinary subagents. It is durable coordinated execution: task state, worker roster, claim leases, mailbox, verifier lane, events, and summary. `team loop` may add verifier work when implementation is done but verifier evidence is missing. `team gate` decides `continue`, `wait`, `needs_verifier`, `blocked`, or `checkpoint_goal`.

`/goal + /ralplan + /team + /ralph` is the intended powerful composition: goal owns intent, ralplan owns consensus, team owns parallel execution, Ralph keeps non-overlapping cycles moving, memory preserves continuity.

Memory rules: add durable events for decisions/evidence/blockers, compact before worker handoff or when event logs grow, pass workers bounded summaries rather than raw logs.

Safety rules: no external actions without confirmation, no overlapping Ralph/team loops, no worker-owned goal mutations, no completion without verifier/review evidence, no hiding failed tasks.
