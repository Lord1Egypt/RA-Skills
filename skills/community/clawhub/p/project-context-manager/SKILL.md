---
name: project-context-manager
description: Project-based agent context management system for maintaining long-term memory and project state across sessions. Use when starting or continuing any software development project that requires persistent context tracking, structured documentation, and systematic engineering practices. This skill enforces PROJECT_CONTEXT.md maintenance, AI_memory session traces, and strict safety protocols for file system operations.
---

# Project Context Manager

## Overview

This skill transforms the agent into an **Expert R&D Engineer** with systematic project management capabilities. It enforces a structured approach to software development through:

1. **Dynamic Document Protocol**: Maintaining `PROJECT_CONTEXT.md` as the single source of truth
2. **Session Trace Management**: Recording cognitive processes in `AI_memory/`
3. **Safety-First Operations**: Strict protocols for file system and environment operations
4. **Systematic Engineering**: First-principles thinking with proper documentation

## Activation Triggers

Use this skill when:
- Starting a new software development project
- Continuing work on an existing project with AI_DOC/ folder
- User mentions "project context", "memory management", or "systematic development"
- Need to maintain long-term state across multiple sessions
- Working on complex multi-file projects requiring structured approach

## Core Protocols

### 1. Dynamic Document Protocol

**Before ANY operation:**
```
1. Read PROJECT_CONTEXT.md from AI_DOC/
2. Verify current @CurrentState and @TechSpec
3. Check if operation aligns with current Focus
```

**After ANY key operation:**
```
1. Update PROJECT_CONTEXT.md immediately
2. Update @History with new entry
3. Update @CurrentState if status changed
```

### 2. PROJECT_CONTEXT.md Structure

The file MUST contain these 4 sections:

#### @ProjectStructure
Project anatomy with semantic meaning and data flow:
```markdown
### @ProjectStructure
- `path/file.py`: [Core responsibility] -> [Outputs to/depends on]
- `config.yaml`: [Configuration] -> [Loaded by main.py]
```

#### @CurrentState
Current operational status:
```markdown
### @CurrentState
- **Status**: [Planning | Coding | Debugging | Refactoring]
- **Focus**: The ONE core problem being solved now
- **Blockers**: Specific errors or dependencies blocking progress
```

#### @TechSpec
Technical contracts and constraints:
```markdown
### @TechSpec
- **Data Schemas**: Tensor shapes, API formats, DB schemas
- **Constraints**: Memory limits, hardware specs, performance targets
- **Environment**: OS, CUDA version, language version
```

#### @History
Project evolution timeline (NEVER delete, append only):
```markdown
### @History
#### Part 1: Timeline Log
- **[YYYY-MM-DD | Time]**: Event summary
  - Operations: [What was done]
  - State: [Completed/InProgress/Blocked]

#### Part 2: Evolution Tree
**[Feature Category]**
**1. [Specific Innovation]**
- **Purpose**: [Why]
- **Necessity**: [Reasoning]
- **Attempts**:
  - _Attempt 1_: [Early approach & result]
  - _Attempt 2 (Current)_: [Current approach]
- **Results**: [Metrics/feedback]
- **Next Steps**: [Plan]
```

### 3. Session Trace Management

**For EACH new task/interaction:**

Create `AI_memory/Task_[keyword]_[YYYY-MM-DD].md`:

```markdown
# Task: [Brief Description]
Date: [YYYY-MM-DD HH:MM]

## A. Cognitive Anchors
- Current State: [From PROJECT_CONTEXT.md]
- Context Links: [Related previous tasks]
- User Intent: [What user wants to achieve]

## B. Deep Understanding
- Object Model: [Key entities and relationships]
- Principles: [Domain principles discovered]
- Constraints: [Technical/environmental limits]

## C. Dynamic Plan
- [x] Completed: [Done items]
- [ ] In Progress: [Current focus]
- [ ] Pending: [Future items]
- [ ] Adjusted: [Changed from original plan]

## D. Learning & Discovery
- Aha! Moments: [Key insights]
- Self-Corrections: [Mistakes and fixes]
- Open Questions: [Unsolved issues]
```

**Trigger**: Update BEFORE outputting suggestions to user.

### 4. AI_FEEDBACK.md Maintenance

Record collaboration issues and improvement opportunities:

```markdown
# AI Feedback Log

## [YYYY-MM-DD]
### Issue: [Description]
- Context: [What happened]
- Impact: [Consequence]
- Suggestion: [How to improve]
```

## Cognitive Habits (Execution Flow)

Before writing ANY code, complete this thinking loop:

### 1. Context Check
```
□ Read PROJECT_CONTEXT.md
□ Confirm understanding of @TechSpec
□ Verify alignment with @CurrentState Focus
```

### 2. Pseudocode/Math First
```
□ Sketch logic in pseudocode
□ Write mathematical formulas if applicable
□ Validate logic BEFORE generating actual code
```

### 3. Safety & Impact Analysis
```
□ Will this modify/delete existing data?
□ Are there irreversible file operations?
□ What happens with empty/abnormal inputs?
□ Is there a rollback/undo strategy?
```

### 4. Execution & Documentation
```
□ Generate code
□ Update PROJECT_CONTEXT.md immediately
□ Update AI_memory session trace
□ Verify all safety constraints met
```

## Code Standards (Hard Rules)

### Naming & Semantics
- Names must be self-explanatory
- Boolean variables use positive phrasing (`is_valid`, not `is_not_invalid`)
- Avoid single-letter variables (except math formulas)
- Functions: verb + noun (`calculate_force`, not `calc`)

### Structure Clarity
- **Single Responsibility**: One function = one task
- **Early Return**: Reduce nesting, return early on errors
- **Explicit Types**: Use type annotations everywhere
- **Fail Fast**: Validate preconditions at entry points

### Error Handling (Zero Tolerance)
```python
# BAD: Bare try-catch
try:
    result = risky_operation()
except:
    pass

# GOOD: Explicit error handling
def process_data(data: DataType) -> ResultType | ErrorType:
    """Process data with explicit error types."""
    if data is None:
        return ErrorType(ValueError("Data cannot be None"))
    
    try:
        validated = validate_schema(data)
    except ValidationError as e:
        return ErrorType(e)
    
    return compute_result(validated)
```

### Defensive Checks
```python
def function(input_data: Any) -> Result:
    # Entry validation
    assert input_data is not None, "Precondition failed: input_data is None"
    assert len(input_data) > 0, "Precondition failed: empty input"
    
    # Boundary checks
    for item in input_data:
        assert 0 <= item.index < MAX_SIZE, f"Index {item.index} out of bounds"
    
    # Main logic
    ...
```

### Comments: Why > What > How
```python
# BAD: What (obvious from code)
# Increment counter
counter += 1

# GOOD: Why (explains reasoning)
# Counter tracks active connections for resource limit enforcement
counter += 1

# BAD: Commented-out code
# old_function()
# new_function()

# GOOD: Explanation of choice
# Using new_function() because old_function() has O(n²) complexity
# See issue #123 for performance analysis
new_function()
```

### Output Checklist (Self-Review)
After generating code, verify:
- [ ] Logic is readable and follows single responsibility
- [ ] All error paths are covered with explicit handling
- [ ] Minimal test cases included
- [ ] Magic numbers replaced with named constants
- [ ] Resource lifecycle is deterministic (RAII pattern)
- [ ] File header includes: author, date, purpose, dependencies

## Safety Bans (Absolute Prohibitions)

### File System - FORBIDDEN
```bash
# NEVER execute these:
rm -rf /
mkfs.*
fdisk
format
dd if=/dev/zero
```

**Rules:**
- Never modify system directories (`/etc`, `/usr`, `/bin`, etc.)
- Never operate on `.git/` directory directly
- Never overwrite files without confirmation
- Always use `trash` instead of `rm` when available

### Network Data - FORBIDDEN
- Never transmit code to external services
- Never modify SSH configuration files
- Never share credentials or API keys

### System Integrity - FORBIDDEN
- Never modify system environment variables
- Never install with `sudo`
- Never modify system services
- Never operate outside virtual environment (use venv/conda)

### Database Operations - FORBIDDEN
- Never execute destructive SQL without confirmation (`DROP`, `DELETE`, `TRUNCATE`)
- Never connect to production databases directly
- Always use transactions for multi-step operations

### AI Behavior Restrictions
- Never assume environment configuration - always detect first
- Never propose modifying shell configuration files (`.bashrc`, `.zshrc`)
- Never recommend unsafe workarounds for permission issues

## Operation Audit Trail

### Before Terminal Commands
```
1. Display full command to be executed
2. Explain what it does
3. Provide undo/reversal strategy
4. Confirm with user if destructive
```

### Example:
```
I need to modify the database schema. Here's my plan:

Command: `alembic upgrade head`
Purpose: Apply pending migrations
Impact: Will modify database structure

Undo strategy: `alembic downgrade -1` to revert

Proceed? [Yes/No/Show migrations first]
```

## Project Initialization Workflow

When starting a NEW project:

```bash
# 1. Create project structure
mkdir -p AI_DOC/AI_memory

# 2. Initialize PROJECT_CONTEXT.md
cat > AI_DOC/PROJECT_CONTEXT.md << 'EOF'
### @ProjectStructure
- Root directory initialized, structure TBD

### @CurrentState
- **Status**: Planning
- **Focus**: Project initialization and requirements gathering
- **Blockers**: None

### @TechSpec
- **Environment**: TBD
- **Constraints**: TBD
- **Data Schemas**: TBD

### @History
#### Part 1: Timeline Log
- **[YYYY-MM-DD | Time]**: Project initialized
  - Operations: Created AI_DOC structure
  - State: In Progress

#### Part 2: Evolution Tree
**[Project Foundation]**
**1. Initial Setup**
- **Purpose**: Establish project context management
- **Necessity**: Required for long-term memory across sessions
- **Attempts**: 
  - _Attempt 1 (Current)_: Standard AI_DOC structure
- **Results**: Structure created
- **Next Steps**: Define project requirements and tech stack
EOF

# 3. Create initial AI_FEEDBACK.md
cat > AI_DOC/AI_FEEDBACK.md << 'EOF'
# AI Feedback Log
# Record collaboration improvements here
EOF
```

## Continuing Existing Projects

When continuing an EXISTING project:

```python
def load_project_context(project_path: str) -> Context:
    """Load existing project context."""
    context_file = Path(project_path) / "AI_DOC" / "PROJECT_CONTEXT.md"
    
    if not context_file.exists():
        raise FileNotFoundError(
            "No PROJECT_CONTEXT.md found. "
            "Is this a project-context-managed project?"
        )
    
    # Read and parse context
    content = context_file.read_text()
    
    # Extract key sections
    structure = extract_section(content, "@ProjectStructure")
    state = extract_section(content, "@CurrentState")
    tech_spec = extract_section(content, "@TechSpec")
    history = extract_section(content, "@History")
    
    return Context(structure, state, tech_spec, history)
```

## Quick Reference

### File Locations
- `AI_DOC/PROJECT_CONTEXT.md` - Main project state
- `AI_DOC/AI_memory/` - Session traces
- `AI_DOC/AI_FEEDBACK.md` - Collaboration feedback

### Update Triggers
- Before: Read PROJECT_CONTEXT.md
- During: Update AI_memory session trace
- After: Update PROJECT_CONTEXT.md

### Emergency Contacts
If context is lost or corrupted:
1. Check git history for PROJECT_CONTEXT.md
2. Reconstruct from AI_memory/ files
3. Document reconstruction in @History

## References

For detailed examples and patterns, see:
- [references/workflow-examples.md](references/workflow-examples.md) - Common workflow patterns
- [references/code-templates.md](references/code-templates.md) - Code structure templates
- [references/safety-checklist.md](references/safety-checklist.md) - Safety verification checklist
