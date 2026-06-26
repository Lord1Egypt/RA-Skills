# Memory Structure

MemClaw organizes memory using a multi-dimensional structure with three-tier retrieval layers.

## URI Structure

All memory resources are addressed using the `cortex://` URI scheme:

```
cortex://
├── resources/{resource_name}/           # General resources (facts, knowledge)
├── user/{user_id}/                      # User-specific data (default user_id: "default")
│   ├── preferences/{name}.md            # User preferences
│   ├── entities/{name}.md               # People, projects, concepts
│   ├── events/{name}.md                 # Decisions, milestones
│   └── personal_info/{name}.md          # User profile info
├── agent/{agent_id}/                    # Agent-specific data
│   ├── cases/{name}.md                  # Problem-solution cases
│   ├── skills/{name}.md                 # Acquired skills
│   └── instructions/{name}.md           # Instructions learned
└── session/{session_id}/
    ├── timeline/
    │   ├── {YYYY-MM}/                   # Year-month directory
    │   │   ├── {DD}/                    # Day directory
    │   │   │   ├── {HH_MM_SS}_{id}.md   # L2: Original message
    │   │   │   ├── .abstract.md         # L0: ~100 token summary
    │   │   │   └── .overview.md         # L1: ~2000 token overview
    │   │   └── .abstract.md             # Day-level L0 summary
    │   └── .abstract.md                 # Session-level L0 summary
    │   └── .overview.md                 # Session-level L1 overview
    └── .session.json                    # Session metadata
```

## Dimensions

| Dimension | Purpose | Examples |
|-----------|---------|----------|
| `resources` | General knowledge, facts | Documentation, reference materials |
| `user` | User-specific memories | Preferences, entities, events, profile |
| `agent` | Agent-specific memories | Cases, skills, instructions |
| `session` | Conversation memories | Timeline messages, session context |

## Three-Layer Architecture

Each memory resource can have three representation layers:

| Layer | Filename | Tokens | Purpose |
|-------|----------|--------|---------|
| **L0 (Abstract)** | `.abstract.md` | ~100 | Quick relevance check, filtering |
| **L1 (Overview)** | `.overview.md` | ~2000 | Understanding gist, moderate detail |
| **L2 (Detail)** | `{name}.md` | Full | Exact quotes, complete implementation |

**Layer Resolution:**
- For files: `cortex://user/default/preferences/typescript.md` → layers are `.abstract.md` and `.overview.md` in same directory
- For directories: `cortex://session/default/timeline` → layers are `.abstract.md` and `.overview.md` in that directory

**Access Pattern:**
```
1. Start with L0 (quick relevance check)
2. Use L1 if L0 is relevant (more context)
3. Use L2 only when necessary (full detail)
```

## Session Memory

### session_id Configuration

`{session_id}` is a memory isolation identifier for separating different conversation contexts:

| Configuration Location | Field Name | Default Value |
|-----------------------|------------|---------------|
| OpenClaw plugin config | `defaultSessionId` | `"default"` |

**Configuration Example** (`openclaw.json`):
```json
{
  "plugins": {
    "entries": {
      "memclaw": {
        "config": {
          "defaultSessionId": "my-project"
        }
      }
    }
  }
}
```

**Usage Rules:**
- `session_id` parameter in tools is optional; defaults to configured value
- Different session_ids provide memory isolation for multi-project/multi-topic management
- Replace `{session_id}` in URIs with actual value, e.g., `cortex://session/default/timeline`

### Timeline Organization

Timeline messages are organized hierarchically by date:

```
session/{session_id}/timeline/
├── 2024-03/                     # Year-Month
│   ├── 15/                      # Day
│   │   ├── 10_30_45_abc123.md   # Message at 10:30:45
│   │   ├── .abstract.md         # Day-level L0
│   │   └── 16/
│   │       └── ...
│   └── .abstract.md             # Month-level L0
├── .abstract.md                 # Session-level L0
└── .overview.md                 # Session-level L1
```

**Message File Format:** `{HH_MM_SS}_{random_id}.md`

## User Memory Categories

| Category | Description | URI Pattern |
|----------|-------------|-------------|
| `preferences` | User preferences by topic | `cortex://user/{user_id}/preferences/{name}.md` |
| `entities` | People, projects, concepts | `cortex://user/{user_id}/entities/{name}.md` |
| `events` | Decisions, milestones | `cortex://user/{user_id}/events/{name}.md` |
| `personal_info` | User profile information | `cortex://user/{user_id}/personal_info/{name}.md` |

## Agent Memory Categories

| Category | Description | URI Pattern |
|----------|-------------|-------------|
| `cases` | Problem-solution pairs | `cortex://agent/{agent_id}/cases/{name}.md` |
| `skills` | Acquired skills | `cortex://agent/{agent_id}/skills/{name}.md` |
| `instructions` | Learned instructions | `cortex://agent/{agent_id}/instructions/{name}.md` |

## Session Metadata

Each session has a `.session.json` file containing:

```json
{
  "thread_id": "session_id",
  "status": "active|closed|archived",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T12:45:00Z",
  "closed_at": null,
  "message_count": 25,
  "participants": ["user_001", "agent_001"],
  "tags": ["typescript", "api-design"],
  "title": "Optional session title",
  "description": "Optional description"
}
```

## Layer Generation

Layers are generated **asynchronously** to avoid blocking agent responses:

1. **L2 (Detail)**: Created immediately when memory is added
2. **L0/L1**: Generated when `cortex_commit_session` is called or via background maintenance

**When to call `cortex_commit_session`:**
- After completing a significant task
- After user shares important preferences
- When conversation topic shifts
- Every 10-20 exchanges
