# Multi-worker supervision

This document defines how `local-coding-orchestrator` should supervise multiple local coding tools at the same time.

## Goal

Use different worker tools for distinct roles while keeping the supervisor responsible for:
- coordination
- periodic progress checks
- blocker detection
- reviewer consensus
- next-step routing

The supervisor should not disappear after launch.
Launching workers is only the start of orchestration, not the end.

## Recommended multi-worker role split

Use role separation whenever practical.

### Primary implementer

Default purpose:
- make repo changes
- ship the next usable increment
- keep scope aligned with the active phase

Examples:
- OpenCode as primary implementation worker on hosts where it has confirmed write capability
- Codex when sandboxed write paths are stable

### Reviewer / planner

Default purpose:
- inspect the current codebase
- identify architecture and migration risks
- define the minimum acceptable shape for the next implementation step
- keep implementation from wandering

Examples:
- Claude Code for planning, review, and requirements refinement
- Codex or OpenCode as a second reviewer when comparison is useful

### Secondary reviewer or alternate implementer

Default purpose:
- provide a second opinion
- compare recommended persistence/storage paths
- validate whether the primary worker is over-scoping or under-scoping
- take over a bounded follow-up task if the primary worker is blocked

## Supervisor responsibilities during execution

The supervisor must keep checking on active workers.
Recommended loop:
1. launch workers with explicit role briefs
2. wait a reasonable interval
3. inspect progress logs or process output
4. detect blockers, stalls, or completed outputs
5. coordinate the next step
6. repeat until a stable outcome is reached

The supervisor should look for:
- whether files are actually being created or updated
- whether the worker is only thinking or truly writing
- whether package installation or runtime verification succeeded
- whether the worker has become stuck on a narrow issue
- whether reviewers agree on the next implementation boundary

## Periodic supervision checks

Periodic checks can be manual, heartbeat-driven, or scheduler-driven.

At each check, report at least:
- worker status: running / completed / stalled / blocked
- what each worker has contributed since the last check
- active blocker classification
- whether coordination is needed
- recommended next action

Good examples of supervisor interventions:
- narrowing scope after reviewer feedback
- telling an implementer to land persistence before edit/delete flows
- rerouting to a different worker when the current worker cannot write files
- stopping a worker that is looping without producing repo changes

## Consensus handling

When multiple reviewers are active, do not just quote them.
The supervisor should synthesize.

Recommended synthesis pattern:
- note where reviewers agree
- note where they differ
- choose a working implementation order
- explain why that order is safer or faster

Example:
- Claude recommends persistence first
- Codex recommends a repository boundary first, then persistence
- Supervisor synthesis: create a minimal storage boundary and place persistence behind it before broader CRUD expansion

## Escalation and rerouting

If a worker stalls or hits a narrow blocker, the supervisor should intervene instead of waiting indefinitely.

Typical rerouting patterns:
- adapter failure -> relaunch through a simpler path
- write-blocked runtime -> reroute to a worker with confirmed write capability
- semantic drift -> send a tighter retry brief
- reviewer disagreement -> freeze implementation scope and request a focused comparison

## Completion expectations

A multi-worker run is not complete just because a single worker exits.
The supervisor should confirm:
- repo changes landed
- the app still runs
- review feedback has been incorporated or explicitly deferred
- blockers are classified and documented
- the next action is clear

## Practical pattern validated in local runs

A practical validated pattern is:
- OpenCode implements when real write capability is confirmed
- Claude Code reviews and plans the next increment
- Codex performs a secondary technical assessment
- the supervisor periodically checks all three and coordinates the implementation order

This pattern is especially useful on hosts where tool write capabilities differ in practice.
