# Install Checklist

Use this reference when the user is installing, packaging, or validating the skill.

## Definition Of Done

Treat the skill as installed only when all of these are true:
- `lark-cli` is installed and runnable on `PATH`
- the required read-only user scopes are authorized
- at least one live Lark read loop succeeds for the kind of source this skill will use
- the workspace has a usable `HEARTBEAT.md` task block for this skill

Do not treat "skill folder copied successfully" as done.

## Checklist 1: CLI Ready

- [ ] `lark-cli` is available on `PATH`
- [ ] `lark-cli --help` runs successfully
- [ ] if missing, install it through OpenClaw onboarding metadata or manually with `npm i -g @larksuite/cli`

## Checklist 2: Read-Only Auth Ready

- [ ] run `./scripts/request-readonly-auth.sh`
- [ ] keep this skill read-only
- [ ] if a runtime permission error happens later, request only the missing read-only scope(s)

Do not use this skill to request write scopes.

## Checklist 3: Live Validation

- [ ] do not use `lark-cli auth status` as the pass signal
- [ ] run `./scripts/validate-readiness.sh`
- [ ] also verify one or two lightweight live read loops that match real usage

Good enough examples:
- docs: `docs +search` then `docs +fetch`
- wiki: `spaces list` then `nodes list` or `spaces get_node`
- minutes: `minutes +search` then `minutes get`

Use judgment. The goal is to prove the skill can actually read what it needs, not to exhaustively test every path.

## Checklist 4: Workspace Ready

- [ ] if the workspace already has `HEARTBEAT.md`, merge in the task block from [../assets/HEARTBEAT.md](../assets/HEARTBEAT.md)
- [ ] if `HEARTBEAT.md` is missing, copy the template into the workspace root
- [ ] treat `HEARTBEAT.md` as the source of truth for this skill's cadence and task prompts
- [ ] keep the shipped heartbeat style unless the workspace already has a stronger local convention
