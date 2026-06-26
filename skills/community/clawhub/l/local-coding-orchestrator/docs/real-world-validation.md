# Real-world validation

This document records practical validation runs for `local-coding-orchestrator`.

## Case 1 — Static marketing site under read-only worker runtime

### Repo
- `D:\data\code\fengyun-marketing-web`

### Goal
Validate strict supervisor-only orchestration on a real static site task using:
- probe
- implement
- review
- harden

### What happened
- The supervisor created and tracked a real task.
- Probe confirmed the repo shape and local reachability.
- Review identified bounded issues: encoding corruption risk, placeholder contact details, incomplete focus styling, missing favicon.
- Harden produced an exact patch plan.
- Worker runtime could inspect and reason, but could not write due to read-only / policy-blocked execution.

### Correct classification
- blocker type: `policy`
- near-terminal outcome: `awaiting-writable-runtime`

### Lesson
A worker that can read and analyze but cannot write should not be treated as a semantic failure. Preserve the patch artifact and classify the task as blocked by runtime write capability.

---

## Case 2 — Forum build validation under real multi-tool worker checks

### Repo
- `D:\data\code\forum-orchestrator-demo`

### Goal
Validate that the orchestrator can support a real delivery workflow for a new forum project in `D:\data\code`.

### Supervisor intent
- create repo on D drive
- initialize task via orchestrator
- probe runtime and repo
- confirm which local coding tools can actually start and write files
- prefer real delivery over abstract rule editing

### Tool availability checks
Observed on host:
- `claude` available
- `codex` available
- `opencode` available

### Minimal write tests
The supervisor ran a write-file test in the forum repo for each tool.

#### OpenCode
- Result: success
- Wrote: `TOOLCHECK_OPENCODE.txt`
- Conclusion: can perform real write operations in repo

#### Claude Code
- Result: partial
- Tool started, but requested permission before writing `TOOLCHECK_CLAUDE.txt`
- Conclusion: runnable, but not yet confirmed for unattended write flow

#### Codex
- Result: partial failure
- Tool started and attempted write operations
- Blocked by Windows sandbox refresh failure during patch or shell write path
- Conclusion: installed and runnable, but write path is not yet stable on this host

### Current capability matrix
- OpenCode: runnable + writable
- Claude Code: runnable + write requires approval path
- Codex: runnable + write path unstable due to sandbox issue

### Lesson
Do not treat “tool installed” as sufficient validation.
The orchestrator should validate at least three layers:
1. tool exists
2. tool launches
3. tool can land repo changes

If only one or two layers pass, report the exact capability level instead of claiming the worker is fully operational.

### Practical supervisor recommendation
For immediate delivery on this host:
- use OpenCode as the primary implementation worker
- use Claude Code as reviewer after write path is clarified
- keep Codex in the pool, but treat it as not yet production-ready on this Windows runtime until sandbox write issues are resolved
