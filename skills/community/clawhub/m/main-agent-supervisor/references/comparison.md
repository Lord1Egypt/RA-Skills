# Comparison: Existing Skills vs Needed Supervisor

## Existing public skills inspected

### claude-code-supervisor
Strengths:
- detects stuck/error/completion states
- uses a smart pre-filter before heavier triage
- designed for long-running sessions
- closest public fit in spirit

Reusable ideas to integrate:
- `FINE | NEEDS_NUDGE | STUCK | DONE | ESCALATE` triage states
- cheap pre-filter for obvious cases
- watchdog role separate from human escalation

Gaps for this use case:
- focuses on Claude Code / tmux monitoring
- not centered on chat permission loops or obvious-decision suppression

### task-supervisor
Strengths:
- tracks long tasks and progress
- useful for checkpointing and status reporting
- has a simple task-file model that helps pause/resume and progress visibility

Reusable ideas to integrate:
- task-state/checkpoint files
- step-based progress updates
- explicit paused/done states

Gaps:
- more task manager than reply gate
- not designed as a user-attention filter

### self-review
Strengths:
- evaluates output quality
- useful as a passive review layer

Gaps:
- focuses on quality/structure, not escalation policy
- does not decide whether the agent should keep going vs ask

## Legacy EasyClaw supervisor docs

Observed documents:
- `~/.easyclaw/workspace/SUPERVISOR.md`
- `~/.easyclaw/workspace/SUPERVISOR_PLAYBOOK.md`

Strong ideas worth reusing:
- AUTO / CONFIRM / ESCALATE split
- worth-trying auto-approval
- coach + judge instead of pure gatekeeper
- anti-permission-loop design
- one-question escalation format

Weaknesses to avoid:
- too much file/task plumbing in the first version
- over-specific queue/log paths too early
- coupling to old EasyClaw scripts before proving the core policy

## Recommendation
Build a custom skill for this workspace using:
- policy ideas from the old EasyClaw supervisor docs
- passive review ideas from `self-review`
- stuck/watchdog concepts from `claude-code-supervisor`
- task-state/checkpoint ideas from `task-supervisor`

Do not start with a large automation stack. Start with:
1. classifier
2. pre-send gate
3. triage/watchdog states
4. coaching fields
5. lightweight task-state files for larger tasks
6. simple audit notes
