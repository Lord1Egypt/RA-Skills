# OpenClaw Pilot

Compile rough ideas into an executable blueprint and a clean OpenClaw execution packet.

## What this skill does

OpenClaw Pilot is an instruction-first skill built around one core value: compile rough ideas into an executable blueprint and a clean OpenClaw execution packet.

It helps the user convert a fuzzy goal into two tightly scoped outputs:

1. a human-readable blueprint for the current stage
2. a separate pure execution packet that can be handed directly to OpenClaw

It also supports continuation through `/pilot next <pilot_id> ...`, so the user can keep advancing the same pilot without re-explaining the whole project.

## Core output contract

This skill is built around a strict two-message delivery contract.

### Message 1 — human-readable blueprint

The first message is for the human. It should explain:

- the current goal
- the current stage
- why this stage is the right next step
- in-scope vs out-of-scope boundaries
- what feedback should come back to `/pilot`
- the next continuation command

### Message 2 — pure execution packet

The second message must contain only one block:

```text
[OPENCLAW_EXECUTION_PACKET v1]
...
[END_OPENCLAW_EXECUTION_PACKET]
```

No extra prose. No prefix. No suffix. No human commentary mixed into the packet message.

## Use when

Use OpenClaw Pilot when the user:

- has a rough project idea but needs it compiled into an executable plan
- wants a safe, scoped blueprint before execution
- wants a clean packet to pass into OpenClaw
- needs to continue an existing pilot with `/pilot next <pilot_id> ...`
- wants the behavior contract locked down more than host-specific integration tricks

## Do not use for

- unrelated host integration work
- broad plugin-platform refactors when a skill shell is enough
- pretending to execute work that has not been scoped
- merging human-readable explanation into the packet message

## Command patterns

### New pilot

```text
/pilot <goal>
```

Example:

```text
/pilot Build a lightweight OpenClaw workflow for turning vague product ideas into implementation-ready execution packets.
```

### Continue an existing pilot

```text
/pilot next <pilot_id> <feedback>
```

Example:

```text
/pilot next pilot-abc123 STATUS: blocked SUMMARY: docs are clear but the packet needs stricter scope boundaries.
```

## Behavior promises for the public beta

This first public beta skill release promises:

- blueprint-first planning
- strict two-message output contract
- clean packet handoff semantics
- continuation with `/pilot next <pilot_id> ...`
- instruction-first usage with minimal setup burden

It does not promise:

- a heavy plugin companion
- remote host automation as the headline feature
- broad environment/bootstrap orchestration
- perfect immunity to every upstream model-formatting wobble

## Notes for publishers

This skill is intentionally metadata-clean and dependency-light.

- Prefer publishing the skill shell first.
- Keep examples concrete and contract-focused.
- Do not declare extra local binaries unless they are truly required.
- If a future plugin companion is added, keep its boundary separate from this skill’s public contract.
