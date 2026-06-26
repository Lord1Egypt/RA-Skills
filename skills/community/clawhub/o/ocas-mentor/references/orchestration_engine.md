# Mentor Orchestration Engine

## Goal Decomposition
Break goals into task graphs with explicit dependencies. Each task has a candidate skill, expected artifacts, and priority.

## Scheduling
Execute only tasks whose dependencies are complete. Prioritize critical-path tasks. Bounded parallelism. Avoid unnecessary fan-out.

## Skill Selection
Select the most appropriate skill for each task. Record model and provider when available for later pairing analysis.

## Failure Repair
1. Retry same task with refined framing
2. Retry with alternate compatible skill
3. Split task into smaller tasks
4. Revise task ordering/dependencies
5. Escalate to strategy loop
Every repair action must be journaled. Never retry indefinitely.
