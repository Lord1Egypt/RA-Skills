# Setup - OpenTable

Read this when `~/opentable/` is missing or empty.
Keep setup practical and non-blocking.

## Operating Priorities

- Answer the immediate reservation or operations question first.
- Confirm how OpenTable is used today before suggesting structural changes.
- Keep recommendations implementable by the current team.

## First Activation Flow

1. Confirm business context:
- single venue or multi-venue operation
- service model (casual, fine dining, hybrid)
- current booking lead time and peak windows

2. Confirm success criteria for this cycle:
- occupancy target
- no-show reduction target
- guest satisfaction objective
- revenue mix objective

3. Confirm operational constraints:
- seating capacity and turn assumptions
- staffing limits by daypart
- cancellation policy and communication standards
- event or holiday exceptions already scheduled

4. If context is approved, initialize local workspace:
```bash
mkdir -p ~/opentable
touch ~/opentable/{memory.md,reservation-log.md,guest-signals.md,incidents.md}
chmod 700 ~/opentable
chmod 600 ~/opentable/{memory.md,reservation-log.md,guest-signals.md,incidents.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Start with one optimization objective per week.
- Prefer reversible changes first.
- Track outcomes before expanding rollout.
- Keep incident handling templates ready before peak windows.

## What to Save

- current objective and active constraints
- recent pacing and inventory changes
- no-show and guest friction signals
- incident causes, mitigations, and open prevention tasks

## Guardrails

- Never request raw credentials or private tokens in chat.
- Never claim impact without measurable before/after evidence.
- Never recommend capacity expansions that operations cannot support.
