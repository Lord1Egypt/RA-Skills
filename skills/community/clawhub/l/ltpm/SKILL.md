# Long-term Task Progress Management (LTPM)

**Skill Name**: `long-term-task-progress`  
**Version**: 2.1  
**License**: MIT-0  
**Author**: OpenClaw Community
**Purpose**: A universal protocol for managing long-term, multi-stage projects in OpenClaw. Ensures that any project can be resumed seamlessly after days or weeks of pause.  
**Trigger**: When user initiates a project that will span multiple sessions, or explicitly asks for progress management.

---

## Overview

The **LTPM (Long-term Task Progress Management)** protocol transforms OpenClaw's short-term conversation memory into structured long-term documents. It ensures that when you return to a project after days or weeks, you can instantly understand:

1. **What** the project aims to achieve
2. **Where** you left off
3. **What** needs to be done next

### Design Philosophy

This skill is designed for **OpenClaw's always-on background service** architecture:
- **Passive Mechanism (保底)**:利用 HEARTBEAT.md 原生机制，防止非预期中断导致的进度丢失
- **Active Mechanism (增强)**: 关键里程碑时的主动记录，确保重要决策路径被精准保留
- **Dual-track Collaboration**: 被动保底 + 主动增强，平衡系统健壮性与 Token/上下文资源开销

---

## Quick Start

When you start a new long-term project:

1. Create the project directory structure (see below)
2. Initialize the Core Triad documents
3. Configure auto-save settings
4. Update MEMORY.md with project index

```bash
# Example project initialization
projects/
└── {project_name}/
    ├── MISSION.md        # Required: Project goals
    ├── PROGRESS.md       # Required: Current status
    └── NEXT_STEPS.md     # Required: Action items
```

---

## 1. Universal Project Structure

### Core Triad (Required for ALL projects)

These three documents are **mandatory** for any project managed under LTPM:

| File | Purpose | Updates |
|------|---------|---------|
| **`MISSION.md`** | Project definition: goals, success criteria, deliverables, constraints | Only when goals change |
| **`PROGRESS.md`** | Current status: stage, completed milestones, blockers, recent activity | Every session / milestone |
| **`NEXT_STEPS.md`** | Action queue: prioritized atomic tasks, next immediate action | After each work session |

### Optional Extensions (By Project Type)

Add folders/files as needed based on project nature:

| Project Type | Optional Folders/Files |
|--------------|------------------------|
| **Code Development** | `architecture.md`, `docs/`, `tests/`, `src/` |
| **Artistic Creation** | `assets/`, `references/`, `style_guide.md` |
| **Long-form Writing** | `outline.md`, `research/`, `chapters/` |
| **Business Operations** | `config/`, `scripts/`, `logs/` |
| **Research** | `hypothesis.md`, `findings/`, `data/` |

---

## 2. Document Templates

### MISSION.md Template

```markdown
# {Project Name}

**Created**: {YYYY-MM-DD}
**Version**: {x.y}
**Status**: Active / Paused / Completed

## Vision
What are we building/creating? Why does it matter?

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Deliverables
- Primary: {main output}
- Secondary: {supporting outputs}

## Constraints
- Budget / Time / Resources
- Technical limitations
- Dependencies

## Stakeholders
- Owner: {name}
- Contributors: {names}
```

### PROGRESS.md Template

```markdown
# Progress Tracker: {Project Name}

**Last Updated**: {YYYY-MM-DD HH:MM}
**Overall Progress**: {x%}

## Current Stage
{Stage Name} - {Brief description}

## Milestones

### ✅ Completed
- [YYYY-MM-DD] Milestone 1
- [YYYY-MM-DD] Milestone 2

### 🔄 In Progress
- [YYYY-MM-DD] Current task...

### ⏳ Pending
- [ ] Future milestone 1
- [ ] Future milestone 2

## Blockers
- 🚧 Blocker 1: {description}
- 🚧 Blocker 2: {description}

## Recent Activity
- {YYYY-MM-DD HH:MM}: {What was accomplished}
- {YYYY-MM-DD HH:MM}: {What was discussed}

## Notes
{Cross-session context that must be preserved}
```

### NEXT_STEPS.md Template

```markdown
# Next Steps: {Project Name}

**Last Updated**: {YYYY-MM-DD HH:MM}

## Immediate Priority (Next Session)
1. [ ] {Atomic task 1}
2. [ ] {Atomic task 2}

## Short-term (This Week)
- [ ] Task A
- [ ] Task B

## Medium-term (This Month)
- [ ] Task C
- [ ] Task D

## Waiting On
- ⏳ {Item}: Waiting for {who/what}
```

---

## 3. Dual-Track Auto-Save Mechanism

This skill implements a **dual-track collaboration** mechanism, combining passive background monitoring with active milestone tracking:

### Track A: Passive Snapshot (利用 HEARTBEAT.md)

**Design Philosophy**: Designed for OpenClaw's always-on background service. This is a **low-power, high-compatibility** solution that works transparently without requiring user intervention.

**Trigger**: Detection of `HEARTBEAT.md` changes + time threshold exceeded

**Action**:
1. Monitor HEARTBEAT.md for updates (background service behavior)
2. When heartbeat updates but PROGRESS.md hasn't been synced for a while:
   - Read current workspace state (last modified files, recent error logs)
   - Record `[Auto-Sync]` snapshot in `PROGRESS.md`
3. **Advantage**: Prevents progress loss without user awareness, saves token consumption

**Technical Implementation**:
- This can be integrated into OpenClaw's HEARTBEAT.md mechanism
- Or implemented as a periodic background check

#### 3.1 Dynamic Threshold Configuration

Silence thresholds are **adaptive** based on project complexity and session activity:

**Project Complexity Factors**:
| Complexity | File Count | Indicators | Base Threshold |
|------------|:----------:|------------|----------------|
| Simple | < 10 files | Single module | 15 min |
| Medium | 10-50 files | Multiple modules | 10 min |
| Complex | 50-200 files | Multi-layer architecture | 5 min |
| Very Complex | > 200 files | Distributed system | 3 min |

**Session Activity Indicators**:
- **High Activity** (frequent tool calls, file edits): Reduce threshold by 50%
- **Normal Activity**: Use base threshold
- **Low Activity** (long idle periods): Increase threshold by 100%

**Adaptive Threshold Calculation**:
```
effective_threshold = base_threshold × activity_multiplier × complexity_factor
```

**Silence Thresholds** (configurable, default values):
- **Simple Project + High Activity**: 7 minutes → Generate incremental session summary → update PROGRESS.md "Recent Activity"
- **Medium Project + Normal Activity**: 10 minutes → Generate incremental session summary → update PROGRESS.md "Recent Activity"
- **Complex Project + High Activity**: 3 minutes → Generate incremental session summary → update PROGRESS.md "Recent Activity"
- **60 minutes (any project)**: Update progress percentage → sync to MEMORY.md project index

**Configuration File** (`.ltpm/config.json`):
```json
{
  "thresholds": {
    "simple": 15,
    "medium": 10,
    "complex": 5,
    "very_complex": 3
  },
  "activity_multipliers": {
    "high": 0.5,
    "normal": 1.0,
    "low": 2.0
  }
}
```

#### 3.2 Passive Trigger Optimization (File Watcher Fallback)

When system resource consumption is low, use **file system watcher** instead of heartbeat mechanism:

**Detection Logic**:
```python
# Pseudocode for trigger mode selection
if system_resources_available():
    use_file_watcher = True
    trigger_mode = "file_watcher"  # fswatch/inotify
else:
    use_file_watcher = False
    trigger_mode = "heartbeat"  # Default HEARTBEAT.md
```

**File Watcher Configuration**:
| Tool | Platform | Command |
|------|----------|---------|
| `fswatch` | macOS/Linux | `fswatch -o projects/` |
| `inotifywait` | Linux | `inotifywait -m -r projects/` |
| `FileSystemWatcher` | Windows | PowerShell API |

**File Watcher Behavior**:
- Monitor: `.`, `*.md`, `*.json`, `*.yaml` in project directory
- Trigger: Any file change → check if PROGRESS.md needs update
- Debounce: Wait 2 seconds after last change to batch updates
- Filter: Ignore `.git/`, `node_modules/`, `__pycache__/`

**Resource Check**:
- CPU usage < 20%: Enable file watcher
- Memory usage < 50%: Enable file watcher
- Otherwise: Fall back to heartbeat mechanism

#### 3.3 Conflict Resolution

**Last-Write-Wins + Timestamp-Based Detection**:

**Conflict Detection**:
```python
def detect_conflict(progress_file):
    current_mtime = get_modified_time(progress_file)
    last_known_mtime = get_stored_mtime(progress_file)

    if current_mtime != last_known_mtime:
        # External modification detected
        return True
    return False
```

**Resolution Strategy**:
1. **Timestamp Comparison**: Compare file modification times
2. **Last-Write-Wins**: The most recent write always wins
3. **Backup Preservation**: Keep `.auto-save` backup before overwriting

**Conflict Resolution Flow**:
```
[Write Attempt]
    ↓
[Check if file modified since last read]
    ↓ (yes)
[Create .auto-save backup]
    ↓
[Write new content]
    ↓
[Update stored timestamp]
```

**Backup File Naming**:
- Format: `PROGRESS.md.auto-save.{timestamp}`
- Retention: Keep last 5 backups
- Cleanup: Delete oldest when exceeding limit

### Track B: Active Milestone (主动增强)

**Design Philosophy**: Complement to passive mechanism. Ensures important decision paths are precisely captured.

**Trigger**: 
- Agent completes key items in NEXT_STEPS.md
- Agent achieves阶段性成果 through execution instructions

**Action**:
1. Call `update_progress` directive
2. Record:
   - Achieved goals
   - Verified logic
   - Encountered obstacles
   - Next correction plan
3. **Advantage**: Precisely captures decision logic, provides high-quality context for handoff

#### 3.4 Backup Mechanism (.auto-save)

**Automatic Backup**:
- **Trigger**: Before any write operation to PROGRESS.md
- **Location**: Same directory as PROGRESS.md
- **Naming**: `PROGRESS.md.auto-save.{YYYYMMDD-HHMMSS}`
- **Retention**: Keep last 5 backups (configurable)

**Backup Configuration**:
```json
{
  "backup": {
    "enabled": true,
    "max_count": 5,
    "directory": "."
  }
}
```

**Backup Restoration**:
```bash
# List backups
ls -la PROGRESS.md.auto-save.*

# Restore from backup
cp PROGRESS.md.auto-save.20240315-143022 PROGRESS.md
```

#### 3.5 Explicit Active Trigger Prompts

Add clear trigger prompts to remind users when to actively record:

**Trigger Prompt Template (EN)**:
```
┌─────────────────────────────────────────────────────────────┐
│ 📌 **Time to Record Progress!**                             │
│                                                             │
│ Consider updating PROGRESS.md when you:                     │
│ ✓ Complete a significant task (file edits, code changes)   │
│ ✓ Make an important decision or discover something         │
│ ✓ Finish a work session / "talk to you later"              │
│ ✓ Achieve a milestone or stage completion                   │
│                                                             │
│ Quick Commands:                                              │
│   /checkpoint - Save current progress                      │
│   /mark_milestone - Mark key milestone                      │
└─────────────────────────────────────────────────────────────┘
```

**触发提示模板 (中文)**:
```
┌─────────────────────────────────────────────────────────────┐
│ 📌 **记录进度时机!**                                         │
│                                                             │
│ 以下情况请主动更新 PROGRESS.md：                             │
│ ✓ 完成重要任务（文件编辑、代码修改）                         │
│ ✓ 做出重要决定或发现新信息                                  │
│ ✓ 结束工作会话 / "下次再聊"                                 │
│ ✓ 达成里程碑或阶段完成                                      │
│                                                             │
│ 快速命令：                                                  │
│   /checkpoint - 保存当前进度                                │
│   /mark_milestone - 标记关键里程碑                          │
└─────────────────────────────────────────────────────────────┘
```

**When to Show Trigger Prompts**:
- On session start (first message after idle > 30 min)
- Before session end (user says goodbye)
- After completing >3 file modifications
- After running scripts > 60 seconds

#### 3.6 Natural Language Triggers

**Chinese Triggers** (触发词):
| Category | Keywords |
|----------|----------|
| Start | "开始项目", "新建任务", "启动" |
| Progress | "进度", "完成", "做到了", "搞定了" |
| Pause | "暂停", "先这样", "下次继续" |
| End | "结束", "再见", "回头聊", "先撤了" |
| Milestone | "里程碑", "阶段完成", "搞定了" |

**English Triggers**:
| Category | Keywords |
|----------|----------|
| Start | "start project", "new task", "begin" |
| Progress | "progress", "completed", "done", "finished" |
| Pause | "pause", "continue later", "talk later" |
| End | "end", "goodbye", "see you", "bye" |
| Milestone | "milestone", "stage done", "achieved" |

**Trigger Detection Logic**:
```python
def detect_trigger_intent(user_message):
    chinese_triggers = {
        "start": ["开始", "新建", "启动"],
        "progress": ["进度", "完成", "搞定"],
        "pause": ["暂停", "先这样", "下次"],
        "end": ["结束", "再见", "回头"],
        "milestone": ["里程碑", "阶段"]
    }
    # Return matched category
```

#### 3.7 Structured Format Support (JSON/YAML)

**Optional Format Configuration**:
```json
{
  "format": {
    "default": "markdown",
    "supported": ["markdown", "json", "yaml"]
  }
}
```

**JSON Format Template**:
```json
{
  "project": {
    "name": "Project Name",
    "created": "2024-01-01",
    "version": "1.0",
    "status": "active"
  },
  "progress": {
    "overall": 75,
    "current_stage": "API Implementation",
    "milestones": {
      "completed": [
        {"date": "2024-01-01", "description": "Initial setup"},
        {"date": "2024-01-15", "description": "Database design"}
      ],
      "in_progress": [
        {"date": "2024-02-01", "description": "API endpoints"}
      ],
      "pending": [
        {"description": "Frontend integration"}
      ]
    },
    "blockers": [
      {"description": "API key pending", "severity": "high"}
    ]
  },
  "activity": [
    {"timestamp": "2024-02-01T10:30:00Z", "action": "Completed user auth module"}
  ],
  "next_steps": {
    "immediate": [
      {"task": "Write unit tests", "priority": 1}
    ]
  }
}
```

**YAML Format Template**:
```yaml
project:
  name: Project Name
  created: 2024-01-01
  version: 1.0
  status: active

progress:
  overall: 75
  current_stage: API Implementation
  milestones:
    completed:
      - date: 2024-01-01
        description: Initial setup
      - date: 2024-01-15
        description: Database design
    in_progress:
      - date: 2024-02-01
        description: API endpoints
    pending:
      - description: Frontend integration

blockers:
  - description: API key pending
    severity: high

activity:
  - timestamp: 2024-02-01T10:30:00Z
    action: Completed user auth module

next_steps:
  immediate:
    - task: Write unit tests
      priority: 1
```

**Format Conversion**:
```bash
# Convert Markdown to JSON
ltpm convert --from md --to json projects/myproject/

# Convert JSON to YAML
ltpm convert --from json --to yaml projects/myproject/
```

**When to Trigger Active Milestone**:
- After completing any tool call that modifies >3 files
- After executing a time-consuming script (>60s)
- When user says "Goodbye", "Talk later", or "Next time"
- When task goal is met

### Status Identifiers

In PROGRESS.md, introduce status identifiers:

| Identifier | Source | Meaning |
|------------|--------|---------|
| `[Auto-Sync]` | Passive | Auto-generated snapshot by background mechanism |
| `[Milestone]` | Active | Key milestone recorded by Agent |

---

## 4. Context Compression Strategy

**Problem**: As progress chains grow, context window may overflow

**Solution**: When PROGRESS.md records exceed 5 milestones, Agent MUST execute `consolidate_progress`:

1. Convert old details into "known facts"
2. Store in LEARNINGS.md or PROGRESS.md archive section
3. Keep only: current state + lessons learned + next steps

---

## 5. Document Boundary Matrix

This matrix defines **where** each type of information should be stored:

| Information Type | PROGRESS.md | NEXT_STEPS.md | MISSION.md | Separate Doc |
|------------------|:-----------:|:--------------:|:----------:|--------------|
| **Todo - Current 3 items** | ✅ Summary | ✅ Full list | ❌ | ❌ |
| **Todo - Backlog** | ❌ | ✅ Full list | ❌ | ❌ |
| **Decisions - Conclusion** | ✅ Summary | ❌ | ✅ Archive | ❌ |
| **Decisions - Reasoning** | ❌ | ❌ | ✅ Archive | ✅ (if complex) |
| **Issues - Active Blockers** | ✅ Current | ❌ | ❌ | ❌ |
| **Issues - All Known** | ❌ Summary | ❌ | ❌ | ✅ (ISSUE.md) |
| **Notes - Meeting Points** | ❌ | ❌ | ❌ | ✅ (notes/) |
| **Technical Details** | ❌ | ❌ | ✅ (if core) | ✅ (docs/) |
| **Changelog - Recent 5** | ✅ | ❌ | ❌ | ❌ |
| **Changelog - Full** | ❌ | ❌ | ❌ | ✅ (CHANGELOG.md) |
| **References** | ❌ | ❌ | ✅ (if key) | ✅ (refs/) |

### Key Principles

1. **PROGRESS.md = Dynamic**: Only contains what's actively being worked on
2. **NEXT_STEPS.md = Actionable**: Contains only tasks ready to execute
3. **MISSION.md = Foundational**: Project goals and major decisions
4. **Separate Docs = Archival**: Full details that don't fit in progress tracking

---

## 6. Workflow Integration

### Starting a New Project

1. Ask user: "What is the project goal? What's the success criteria?"
2. Create directory: `projects/{project_name}/`
3. Initialize Core Triad
4. Update MEMORY.md with project index

### During Active Work

1. Update `NEXT_STEPS.md` before tackling each task
2. Mark completed items in `PROGRESS.md` after each milestone
3. Document decisions in MISSION.md when made
4. Use active milestone triggers after key actions

### Before Ending Session

1. Review `NEXT_STEPS.md` - ensure next action is clear
2. Update `PROGRESS.md` with current status
3. Summarize recent activity in PROGRESS.md
4. Update MEMORY.md project index

### When Resuming After Pause

1. Read MEMORY.md to find project index
2. Read PROGRESS.md to understand current state
3. Read NEXT_STEPS.md to know what to do next
4. If blockers exist, address them before proceeding

---

## 7. Multi-Agent Collaboration

Since OpenClaw workspace may have multiple roles (小白, Code-Pilot, Nimo), establish clear principles:

- **Source of Truth**: Project directory's Core Triad documents are the single source of truth
- **Handoff Protocol**: When switching between agents, first step MUST be `resume {project}` (reading the three MD files)
- **Context Transfer**: When handing over, include PROGRESS.md summary in the context

---

## 8. Example Project Structure

```
projects/
└── campaign_system/
    ├── MISSION.md           # Project goals
    ├── PROGRESS.md          # Current status
    ├── NEXT_STEPS.md        # Action queue
    ├── architecture.md      # Technical design
    ├── docs/
    │   └── api_spec.md
    ├── src/
    │   └── (code files)
    └── logs/
        └── (development logs)
```

```
projects/
└── novel_writing/
    ├── MISSION.md           # Book vision
    ├── PROGRESS.md          # Current chapter
    ├── NEXT_STEPS.md        # Next scenes
    ├── outline.md           # Story outline
    ├── research/
    │   └── (background materials)
    └── chapters/
        ├── chapter_01.md
        └── chapter_02.md
```

---

## 9. Commands Reference

| Command | Description |
|---------|-------------|
| `init_project {name}` | Initialize LTPM structure for new project |
| `checkpoint` | Manually trigger progress save (active) |
| `sync_memory` | Force MEMORY.md update |
| `resume {project}` | Load project context from docs |
| `next` | Show next immediate action |
| `mark_milestone {desc}` | Mark a key milestone (active) |
| `auto_sync_status` | Check if current state is safely synced |

---

## 10. Best Practices

1. **Atomic Tasks**: Break NEXT_STEPS into tasks taking < 30 min each
2. **Percentage Accuracy**: Keep PROGRESS.md percentage within 5% accuracy
3. **Blocker Visibility**: Always surface blockers in PROGRESS.md "Current Stage"
4. **Decision Traceability**: Every major decision = summary in MISSION.md
5. **Memory Index**: Keep MEMORY.md as the "table of contents" for all projects
6. **Dual-Track**: Both passive (HEARTBEAT.md) and active (milestone) mechanisms work together
7. **Context Compression**: Consolidate progress when too many milestones accumulate

---

## 11. MEMORY.md Index Format

Use compact format in MEMORY.md project index:

```markdown
## 活跃项目索引 (LTPM)
- [P] **Campaign System** (75%) | Next: `Confirm API` | Blocker: None
- [P] **Novel writing** (12%) | Next: `Chapter 3 outline` | Blocker: Research needed
- [On-Hold] **Legacy project** | Reason: Waiting external approval
```

---

## 12. Requirements

This section lists all tools, skills, and installations required to use the extended features of LTPM v2.1.

### 12.1 System Tools (Installs)

| Tool | Purpose | Installation |
|------|---------|--------------|
| **fswatch** | File system watcher for macOS/Linux | `brew install fswatch` (macOS) / `apt install fswatch` (Linux) |
| **inotify-tools** | File system watcher for Linux | `apt install inotify-tools` (Linux) |
| **jq** | JSON processing | `brew install jq` (macOS) / `apt install jq` (Linux) |
| **python3** | Script execution | Pre-installed on most systems |
| **pyyaml** | YAML parsing | `pip install pyyaml` |

### 12.2 Required Skills

| Skill | Purpose |
|-------|---------|
| `file_operations` | Read/write project documents |
| `memory_management` | Update MEMORY.md index |
| `task_tracking` | Manage NEXT_STEPS.md |
| `auto_completion` | Background monitoring |

### 12.3 Configuration Files

Create `.ltpm/config.json` in project root:

```json
{
  "version": "2.1",
  "thresholds": {
    "simple": 15,
    "medium": 10,
    "complex": 5,
    "very_complex": 3
  },
  "activity_multipliers": {
    "high": 0.5,
    "normal": 1.0,
    "low": 2.0
  },
  "trigger_mode": "auto",
  "backup": {
    "enabled": true,
    "max_count": 5,
    "directory": "."
  },
  "format": {
    "default": "markdown",
    "supported": ["markdown", "json", "yaml"]
  },
  "file_watcher": {
    "enabled": true,
    "debounce_seconds": 2,
    "ignore_patterns": [".git/*", "node_modules/*", "__pycache__/*"]
  },
  "natural_language": {
    "enabled": true,
    "languages": ["en", "zh-CN"]
  }
}
```

### 12.4 Optional CLI Commands

For advanced users, add these commands to your shell:

```bash
# Initialize LTPM in current directory
ltpm init

# Convert between formats
ltpm convert --from md --to json

# Check sync status
ltpm status

# Force backup
ltpm backup

# Restore from backup
ltpm restore --latest
```

---

*This skill is designed to be shared across users. It creates a universal protocol for long-term task management in OpenClaw.*

**Version History**:
- v1.0: Initial version
- v2.0: Added dual-track mechanism (passive + active), context compression, multi-agent collaboration principles
- v2.1: Added dynamic thresholds, file watcher, explicit triggers, conflict resolution, backup mechanism, JSON/YAML formats, natural language triggers
