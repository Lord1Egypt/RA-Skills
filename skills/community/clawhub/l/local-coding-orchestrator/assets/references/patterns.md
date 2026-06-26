# Local Coding Orchestrator Patterns

## Recommended role split

- Codex -> implementation lead
- Claude Code -> audit / architecture / review
- OpenCode -> alternate approach / session continuation

## Auto-routing modes

### continue
- best default: OpenCode

### review
- best default: Claude Code

### implement
- best default: Codex

### prototype
- best default: Codex first, then optional Claude review

### maintainable-project
- best default: Claude first for stack validation, then Codex for implementation

## Directory discipline

Always prefer a dedicated subdirectory for the task.

Bad:
- dumping generated files into the workspace root
- allowing tools to drift into a different mounted path without noticing

Good:
- create a focused project directory first
- pass that directory explicitly to the wrappers

## Progress reporting

For long-running work:
- run tool workers in background when possible
- use OpenClaw cron or system-event wakeups for periodic checks
- stop progress checks once all workers are done
- treat cron stop-after-completion as coordinator logic, not a native external-worker completion primitive

## Known operational issues

- Some tool workers may not share the same visible filesystem mount set.
- Multi-tool aggregation is currently a structured sequential collector, not a true parallel process supervisor.
- Output cleaning is heuristic and may leave shell-specific noise in summaries.
- Windows PowerShell profiles or constrained language behavior can interfere with some CLI invocations.

## Lightweight prototype path

Use this path when speed matters most:
- HTML
- CSS
- JS
- browser-native runtime
- Three.js CDN for 3D

Use heavier stacks only when they pay for themselves.
