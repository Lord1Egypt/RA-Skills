# Memory Template

> This file is created in `~/learn-from-experience/memory.md` on first use.
> Keep it <=100 lines. Most-used patterns live here.

## Example Entries

```markdown
# Learn-from-Experience Memory

## Confirmed Preferences
<!-- Patterns confirmed by user, never decay -->

### simplicity_first | 0.98
Simple > complex; experiment proves before adopting complex solutions.

### verify_before_answer | 0.99 | HIGH
Never speculate technical details; read source/config first. Say "let me check" when uncertain.

## Active Patterns
<!-- Patterns observed 3+ times, subject to decay -->

### dataset_stats_first | 0.95
Calculate baseline stats before designing experiments. top-k/total > 10% means too easy.

## Recent (last 7 days)
<!-- New corrections pending confirmation -->
- prefer SQLite for MVPs (corrected 02-14)
```

## Usage

The agent will:
1. Load this file on every session
2. Add entries when patterns are used 3x in 7 days
3. Demote unused entries to WARM after 30 days
4. Never exceed 100 lines (compacts automatically)
5. Confirmed Preferences are auto-synced to the agent's global config for cross-session persistence

## Initial Directory Structure

Create on first activation:

```bash
mkdir -p ~/learn-from-experience/{projects,domains,archive}
touch ~/learn-from-experience/{memory.md,index.md,corrections.md,heartbeat-state.md}
```

## Index Template

For `~/learn-from-experience/index.md`:

```markdown
# Memory Index

## HOT
- memory.md: 0 lines

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last update: never

## Sync Status
Last global config sync: never
memory.md last modified: never
Sync status: pending_first_sync
```

## Corrections Log Template

For `~/learn-from-experience/corrections.md`:

```markdown
# Corrections Log

<!-- Format:
## YYYY-MM-DD
- [HH:MM] Changed X -> Y
  Type: format|technical|communication|project
  Context: What was corrected
  Confirmed: pending (N/3) | yes | no
-->
```

## Heartbeat State Template

For `~/learn-from-experience/heartbeat-state.md`:

```markdown
# Learn-from-Experience Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```
