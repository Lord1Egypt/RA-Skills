---
name: OpenTable
slug: opentable
version: 1.0.0
homepage: https://clawic.com/skills/opentable
description: Guide OpenTable availability, booking flows, and guest messaging with conversion-focused listing, pacing, and incident response playbooks.
changelog: Initial release.
metadata: {"clawdbot":{"emoji":"🍽️","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` and confirm service model, reservation goals, and operating constraints before proposing changes.

## When to Use

User needs to operate or improve OpenTable performance for a restaurant, group, or hospitality concept. Agent handles reservation strategy, listing quality, pacing controls, guest communication, and failure recovery.
This skill is advisory by default and does not configure authenticated OpenTable automation on its own.

## Architecture

Memory lives in `~/opentable/`. See `memory-template.md` for setup and status fields.

```
~/opentable/
|-- memory.md                 # Current strategy, goals, and integration state
|-- reservation-log.md        # Demand patterns, pacing changes, and outcomes
|-- guest-signals.md          # No-show patterns, special requests, and friction points
`-- incidents.md              # Overbooking, outage, and recovery records
```

## Quick Reference

Use the smallest relevant file for the task.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Reservation operations | `reservation-playbook.md` |
| Listing and conversion optimization | `listing-optimization.md` |
| Incident and outage response | `incident-response.md` |

## Data Storage

Local notes stay under `~/opentable/`:
- strategy snapshot and current priorities in memory file
- reservation pacing and demand signals in reservation log
- guest behavior patterns in guest signals file
- incident timeline and mitigations in incidents file

## Core Rules

### 1. Anchor Every Change to a Service Goal
Before touching availability or policies, identify the target outcome:
- raise seated covers
- increase average check through better mix
- reduce no-shows and dead inventory
- protect guest experience at peak times

If the goal is unclear, propose options and get confirmation first.

### 2. Keep Inventory Honest Across All Time Windows
Availability must reflect what operations can actually seat.
- do not open slots that kitchen or floor cannot absorb
- separate peak, shoulder, and off-peak strategy
- treat special events and holidays as explicit override windows

Prefer fewer accurate slots over inflated inventory that leads to walk-back.

### 3. Use Pacing and Table Mix as Primary Control Levers
Adjust flow with pacing first, not only with blanket block rules.
- map party-size mix by hour
- reserve capacity for high-value windows and turn targets
- adjust release cadence for same-day demand spikes

Never apply broad slot changes without documenting expected impact.

### 4. Design Guest Messaging to Prevent Friction
Confirmations, reminders, and policy copy should reduce uncertainty.
- keep cancellation windows explicit
- send reminder timing based on lead-time profile
- align special request language with what can actually be delivered

Do not use punitive language when a neutral policy explanation works.

### 5. Run Weekly Experiments With Measurable Hypotheses
Every optimization cycle must include:
- one hypothesis
- one controlled change
- one measurable result window
- one decision to keep, rollback, or iterate

Avoid stacking many changes in the same week when attribution matters.

### 6. Prepare Failure Paths Before They Are Needed
For outages, overbookings, and confirmation failures:
- detect quickly with operational signals
- provide fallback booking or waitlist path
- message affected guests with clear options
- log cause, workaround, and prevention action

Reliability and trust beat short-term occupancy gains.

### 7. Protect Access and Guest Data Boundaries
Use least-privilege access for reservation operations.
- keep account roles scoped to responsibilities
- avoid storing sensitive guest details in long-lived notes
- document only what is required for operational decisions

Never ask users to paste credentials or private account tokens into chat.

## Common Traps

- Chasing occupancy without pacing controls -> service collapses during peak turns
- Opening too much inventory early -> high-value demand displaced by low-yield bookings
- Weak reminder and cancellation copy -> avoidable no-shows and support load
- Editing listing content without testing impact -> conversion drops without clear cause
- Ignoring incident postmortems -> repeated failures and reactive firefighting

## Security & Privacy

Data that leaves your machine by default:
- none required by this playbook itself

Data that stays local:
- operational notes and decisions stored under `~/opentable/`
- local experiment and incident logs without full guest datasets

This skill does NOT:
- configure or execute authenticated OpenTable API access by itself
- request hidden background data collection
- persist credentials in local markdown files
- run undeclared network destinations

## Trust

OpenTable workflows depend on OpenTable services and configured integrations.
Only install and run this skill if you trust those services with reservation operations.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `booking` - booking workflows and reservation operations in adjacent channels
- `customer-support` - guest communication quality and service recovery patterns
- `analytics` - metric design and experiment readouts for operational decisions
- `crm` - guest segmentation and lifecycle handling beyond single reservations
- `travel` - broader travel planning context that intersects with dining reservations

## Feedback

- If useful: `clawhub star opentable`
- Stay updated: `clawhub sync`
