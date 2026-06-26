---
name: planner
description: Local-first planning engine for trips, weeks, launches, projects, schedules, and structured decision-making. Use whenever the user wants to plan something, organize future steps, create a roadmap, map constraints, compare options, or turn a vague goal into a phased plan. Also use when the user says they need a plan, itinerary, schedule, rollout, timeline, or structured next steps. Local-only storage.
---

# Planner: Turn uncertainty into a workable plan.

## Core Philosophy
1. Plans should reduce uncertainty, not create overhead.
2. Start with constraints, then shape the plan.
3. Large plans should become phases, milestones, and next steps.
4. Good planning creates clarity before execution begins.

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Storage
All data is stored locally only under:
- `~/.openclaw/workspace/memory/planner/plans.json`
- `~/.openclaw/workspace/memory/planner/archive.json`

No external sync. No cloud storage. No third-party planning APIs.

## Plan Types
- `trip`: Travel, itinerary, booking sequence, budget-aware planning.
- `week`: Weekly structure, focus themes, time blocks, priorities.
- `project`: Multi-phase roadmap with milestones.
- `launch`: Rollout, preparation, dependencies, timeline.
- `decision`: Option comparison with constraints and tradeoffs.

## Core Fields
- `goal`: What the user wants to achieve
- `constraints`: Budget, time, energy, deadlines, dependencies
- `phases`: High-level stages
- `milestones`: Concrete checkpoints
- `next_steps`: Immediate actionable moves
- `notes`: Additional planning context

## Key Workflows
- **Capture a plan**: `add_plan.py`
- **See best structure**: `suggest_plan.py`
- **Update a plan**: `update_plan.py`
- **Summarize today's planning view**: `daily_plan.py`
- **Review all active plans**: `weekly_map.py`

## Scripts
| Script | Purpose |
|---|---|
| `init_storage.py` | Initialize local storage files |
| `add_plan.py` | Capture a new plan |
| `suggest_plan.py` | Show the best current plan or next phase |
| `update_plan.py` | Update plan status, dates, notes, or phases |
| `daily_plan.py` | Show active plans and immediate next steps |
| `weekly_map.py` | Review all plans across horizons |
