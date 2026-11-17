---
name: plus-ultra
description: Run a Byzantine 2+1 plan before consequential work and a fresh, plan-blind reality check afterward. Use when the user asks for Plus Ultra, maximum rigor, independent proposals, enforced verification, or help responding to a Plus Ultra hook gate. Claude Code can enforce the loop through the included hook adapter; on Codex and other hosts it is a convention unless separately wired and verified.
---

# Plus Ultra

Go beyond: two independent minds propose, one arbiter rules, reality confirms.

## The loop

```text
task -> proposer A (read-only, blind) --\
                                        -> arbiter -> one plan -> main applies once
task -> proposer B (read-only, blind) --/                         |
                                                                  v
                                               fresh reality verifier (plan-blind)
```

1. Check the host's agent budget. If it cannot support the full loop, say so before degrading.
2. Spawn two isolated, read-only proposers with the same task specification.
   - A must not assume any command succeeded; it reads actual state.
   - B must name an alternative approach it rejected and why.
3. Give both proposals to one arbiter. It returns a single authoritative plan or escalates a
   fundamental disagreement to the human.
4. The main thread applies that plan once. Proposers never mutate live state.
5. Spawn a fresh verifier that has not seen the plan. State only what should now be true and have
   it inspect the world independently.

Each proposal includes exact changes, verification, rollback, and uncertainties. The arbiter must
not average incompatible plans into vague consensus.

## Decision matrix

| Agreement | Arbiter action |
|---|---|
| Full | Apply; confidence 90+ |
| Minor differences | Pick the cleaner plan; confidence 80+ |
| Structural differences | Analyze and merge explicitly; confidence 60-85 |
| Fundamental disagreement | Escalate; do not force a winner |

## Recording an enforced turn

Where the Claude Code hook adapter is installed, record the approved plan before mutation:

```sh
plusultra plan --session "$CLAUDE_SESSION_ID" --arbiter Athena --verdict -
```

After the fresh verifier checks reality:

```sh
plusultra confirm --session "$CLAUDE_SESSION_ID" --verifier Argus --verdict -
```

The commands read verdict text from standard input. If nothing observable exists, record
`unobservable`; that is an outcome, not a pass.

## Enforcement truth

- **Claude Code:** the included hook adapter can deny recognized mutating tool calls until a plan
  exists and block completion after mutation until a reality verdict exists. It is enforced only
  after the three hooks are configured and `plusultra doctor` passes.
- **Codex and other hosts:** this repository ships no verified hook adapter for them. Following the
  loop there is convention-only unless an equivalent host integration is separately built, wired,
  and tested. Never describe convention as an enforced gate.

The command classifier is deliberately conservative but heuristic. It is not a shell parser,
sandbox, permission system, or proof that a command is safe.

## Exemptions and escape hatch

Subagents are exempt from the hook to prevent recursive deadlock. The CLI and recognized read-only
commands are also exempt. Disable with `PLUS_ULTRA=off` or `plusultra off`; every CLI escape is
written to `~/.plus-ultra/audit.jsonl`.

## Limits

- Two proposers can share the same false assumption.
- A verifier can check the wrong observable.
- Model diversity helps reduce correlated failures but does not create independence by itself.
- The hook catches common mutation shapes, not arbitrary code execution or every shell grammar.
