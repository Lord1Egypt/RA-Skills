# Workspace Layout

Directory structure created and managed by this skill.

## Intake Layer: `.learnings/`

Raw capture. All events land here first.

```
.learnings/
├── LEARNINGS.md          # Corrections, insights, knowledge gaps, best practices
├── ERRORS.md             # Command failures, integration errors, exceptions
├── FEATURE_REQUESTS.md   # User-requested capabilities
└── REVIEW_QUEUE.md       # Items pending promotion (auto-populated during review)
```

## Memory Layer: `.self-improving/`

Structured memory with tiers.

```
.self-improving/
├── HOT.md                # Always-loaded rules (≤80 lines)
├── INDEX.md              # Topic index with file locations and line counts
├── heartbeat-state.md    # Last review timestamp and stats
├── domains/              # Domain-specific memory
│   ├── coding.md
│   ├── communication.md
│   ├── ops.md
│   └── writing.md
├── projects/             # Project-specific memory
│   └── <project-name>.md
└── archive/              # Cold storage for demoted entries
    └── YYYY-MM.md
```

## Promotion Targets (existing workspace files)

These files are NOT created by this skill — they already exist in the OpenClaw workspace.
The skill only appends to them when a pattern is stable enough.

```
workspace/
├── SOUL.md       # Behavioral patterns, communication style
├── AGENTS.md     # Workflow rules, operational patterns
├── TOOLS.md      # Tool gotchas, integration notes
├── MEMORY.md     # User preferences, decisions, long-term context
└── memory/
    └── YYYY-MM-DD.md  # Daily notes (used by OpenClaw core, not this skill)
```

## File Size Targets

| File | Target max |
|------|-----------|
| `HOT.md` | 80 lines |
| `domains/*.md` | 200 lines each |
| `projects/*.md` | 200 lines each |
| `LEARNINGS.md` | No hard limit (compact during review) |
| `ERRORS.md` | No hard limit (resolve and archive old entries) |
| `REVIEW_QUEUE.md` | Should be near-empty after each review |
