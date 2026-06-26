# Tracker workflow mapping (example)

Use an issue tracker as the durable operational record when collaboration, comments, ownership visibility, and explicit workflow state changes matter.

This file uses Linear-style names as examples only.
Treat all team names, workflow states, priority values, and labels as environment-specific mappings.

## Example workflow mapping
- TRIAGED -> Backlog
- ASSIGNED -> In Progress
- RESOLVED -> Done

## Example priority mapping
- high -> 2
- medium -> 3
- low -> 4

## Example labels
- Bug
- Feature
- Improvement

## Recording pattern
1. Put Issue Skeleton + Quick Triage in the issue description.
2. Add comment when moving to ASSIGNED.
3. Add comment for no-response follow-up.
4. Add comment for recovery / resolution.
5. Move tracker state as the case progresses.

## Example title patterns
- [incident][high] Payment confirmation delayed
- [permission][medium] Team workspace access missing after payment
- [support][low] Billing email change request
