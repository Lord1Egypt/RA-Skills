---
name: opencode-acp
description: Collaborate with OpenCode via ACP protocol for code modifications, refactoring, and feature implementation.
metadata:
  {
    "openclaw": { "emoji": "🔧", "requires": { "anyBins": ["opencode"] } },
  }
---

# OpenCode ACP Collaboration

Use OpenCode via ACP (Agent Client Protocol) for code modifications, refactoring, and feature implementation.

## Quick Start

### Automated Workflow (Recommended)

Use the provided Python script for automated OpenCode collaboration:

> On first run, the skill auto-creates a local `.venv` (Python 3.9+) in this skill directory and re-runs inside that environment.
> If the current interpreter is below 3.9, it auto-discovers a local Python 3.9+ executable (`python3.12`/`python3.11`/`python3.10`/`python3.9`/`python3`/`python`; on Windows also `py -3.x`).

```bash
# Run from this repository root
# Simple task
python opencode_acp_client.py \
  --project /path/to/project \
  --task "Add --version flag to CLI"

# With verbose logging
python opencode_acp_client.py \
  --project /path/to/project \
  --task "Refactor authentication module" \
  --verbose

# With custom timeout (default: 600 seconds)
python opencode_acp_client.py \
  --project /path/to/project \
  --task "Build REST API for todos" \
  --timeout 1200
```

**What it does:**
1. Starts OpenCode ACP server
2. Initializes ACP connection
3. Creates session
4. Sends task
5. Monitors progress and displays output
6. Stops OpenCode when done

**Output:**
- Real-time progress updates
- Tool calls and status
- Agent messages
- Completion status

### Manual Workflow (Advanced)

For fine-grained control, use manual JSON-RPC messages:

```bash
# Start OpenCode ACP server in background
exec pty:true workdir:/path/to/project background:true command:"opencode acp"
# Returns sessionId (e.g., "neat-zephyr")

# Initialize connection
process action:write sessionId:neat-zephyr data:'{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{"fs":{"readTextFile":true,"writeTextFile":true},"terminal":true},"clientInfo":{"name":"Claw","title":"Claw AI Assistant","version":"1.0.0"}}}\n'

# Wait for response
process action:log sessionId:neat-zephyr

# Create session
process action:write sessionId:neat-zephyr data:'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/path/to/project","mcpServers":[]}}\n'

# Wait for session ID
process action:log sessionId:neat-zephyr

# Send task
process action:write sessionId:neat-zephyr data:'{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"ses_xxx","prompt":[{"type":"text","text":"Your task here"}]}}\n'

# Monitor progress
process action:log sessionId:neat-zephyr

# Kill when done
process action:kill sessionId:neat-zephyr
```

## The Pattern: Plan → Execute → Verify

### Step 1: Analyze Requirements

**Your job (as planner):**
- Understand user needs
- Identify technical constraints
- Assess impact and risks

**Output:**
- Clear, specific requirements
- Technical constraints
- Risk assessment

### Step 2: Create Plan

**Your job (as planner):**
- Break down into executable steps
- Define acceptance criteria
- Provide implementation guidance

**Format:**
```markdown
# Task: [Task Name]

## Objective
[Goal description]

## Requirements
1. [Requirement 1]
2. [Requirement 2]
...

## Acceptance Criteria
- ✅ [Criterion 1]
- ✅ [Criterion 2]
...

## Implementation Guidance
1. [Step 1]
2. [Step 2]
...

## Verification
[How to verify]
```

### Step 3: Execute with OpenCode

**Start OpenCode ACP server:**
```bash
exec pty:true workdir:/path/to/project background:true command:"opencode acp"
```

**Initialize connection:**
```json
{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{"fs":{"readTextFile":true,"writeTextFile":true},"terminal":true},"clientInfo":{"name":"Claw","title":"Claw AI Assistant","version":"1.0.0"}}}
```

**Create session:**
```json
{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/path/to/project","mcpServers":[]}}
```

**Send task:**
```json
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"ses_xxx","prompt":[{"type":"text","text":"[Your plan from Step 2]"}]}}
```

### Step 4: Monitor Progress

**Poll for updates:**
```bash
process action:log sessionId:neat-zephyr
```

**Key update types:**
- `agent_thought_chunk` - OpenCode's thinking process
- `tool_call` - Tool invocations (search, analyze, edit)
- `plan` - Task plan updates
- `stopReason` - Task completion signal

**Stop conditions:**
- `stopReason: "end_turn"` - Normal completion
- `stopReason: "cancelled"` - Task cancelled
- Timeout (suggest: 5-10 minutes)

### Step 5: Verify Results

**Verification checklist:**
- ✅ Code changes match requirements
- ✅ Acceptance criteria met
- ✅ Code style consistent
- ✅ Tests pass
- ✅ No regressions

**Verification methods:**
1. Review OpenCode's change summary
2. Run relevant tests
3. Manual verification of key features
4. Code quality check

### Step 6: Cleanup

**Stop OpenCode:**
```bash
process action:kill sessionId:neat-zephyr
```

**Record results:**
- Update memory/YYYY-MM-DD.md
- Record success/failure reasons
- Document lessons learned

## ⚠️ First-Time Project Setup

If this is OpenCode's first time working on a project, initialize the knowledge base first:

1. **Start OpenCode TUI** (not acp mode):
   ```bash
   cd /path/to/project
   opencode
   ```

2. **Run initialization**:
   ```
   /init-deep
   ```

3. **Wait for completion**:
   - OpenCode creates hierarchical AGENTS.md knowledge base
   - Analyzes project structure and code
   - Builds project context

4. **Exit and restart in acp mode**:
   - After initialization, exit TUI
   - Restart with `opencode acp` for collaboration

**Why init-deep?**
- Helps OpenCode understand project structure
- Builds code knowledge graph
- Improves execution efficiency and accuracy
- Reduces unnecessary exploration and trial-and-error

## OpenCode Configuration

**Location:** `/root/.opencode/opencode.json`

**Recommended mode:** `sisyphus` (AI orchestrator)

## ACP Protocol Details

**Protocol version:** 1

**Transport format:** JSON-RPC 2.0

**Message delimiter:** Newline (\n)

**Communication:** stdin/stdout

## Available OpenCode Modes

- **sisyphus** (recommended): Powerful AI orchestrator, excels at planning and delegation
- **hephaestus**: Autonomous deep worker, end-to-end task completion
- **prometheus**: Planning agent
- **atlas**: Task orchestrator

## Best Practices

### 1. Clear Requirements

**Good:**
```markdown
# Task: Add Version Command

## Objective
Add --version flag to display project version from package.json

## Requirements
1. Support both --version and -v
2. Display format: "QMD Memory v1.0.0\nOpenClaw memory plugin"
3. Exit after displaying version

## Acceptance Criteria
- ✅ `bun src/qmd.ts --version` works
- ✅ Version matches package.json
- ✅ No impact on existing commands
```

**Bad:**
```markdown
Add version command
```

### 2. Acceptance Criteria

**Good criteria:**
- Specific, measurable, verifiable
- Include positive and negative tests
- Consider edge cases

**Example:**
- ✅ Run `command --version` displays correct version
- ✅ Run `command -v` displays same result
- ✅ Version matches package.json
- ✅ Exit code is 0
- ✅ No impact on other commands

### 3. Progress Monitoring

**Key metrics:**
- Task breakdown count (typically 3-7 subtasks)
- Background agents count (typically 2-4)
- Tool call count (search, analyze, edit)
- Execution time (typically 2-10 minutes)

**Warning signs:**
- Long silence (> 2 minutes)
- Repeated error messages
- Tool call failures
- Timeout

### 4. Error Handling

**Common errors:**
1. **GLIBC version issues**: Some tools (like ast_grep) may be incompatible
   - Solution: OpenCode auto-switches to other tools
2. **Agent not found**: e.g., "librarian" agent unavailable
   - Solution: OpenCode uses other agents
3. **Timeout**: Task execution too long
   - Solution: Break into smaller tasks or increase timeout

## Collaboration Principles

### Planner's Responsibilities

1. **Clear requirements**:
   - Specific, measurable, verifiable
   - Include context and constraints
   - Provide examples and references

2. **Reasonable plan**:
   - Break into small steps
   - Consider technical feasibility
   - Estimate workload

3. **Effective verification**:
   - Clear acceptance criteria
   - Executable verification methods
   - Timely feedback

### Executor's Characteristics (OpenCode)

1. **Automatic planning**:
   - Break requirements into subtasks
   - Auto-select tools and methods
   - Parallel execution of multiple tasks

2. **Intelligent execution**:
   - Use sisyphus mode (AI orchestrator)
   - Launch background explore agents
   - Auto-search and analyze code

3. **Continuous feedback**:
   - Real-time progress reports
   - Show thinking process
   - Provide execution summary

## Real-World Example

### Case: Add Version Command to QMD

**Requirement:** Add `--version` command-line option

**Planner's work:**
1. Analyze requirement: Need to read package.json version, display project info
2. Create plan:
   - Locate CLI argument parsing logic
   - Add version flag handling
   - Implement version info output
   - Add tests
3. Set acceptance criteria:
   - `bun src/qmd.ts --version` displays correct version
   - `-v` alias works
   - Version matches package.json
   - No impact on existing features

**OpenCode's work:**
1. Auto-break into 5 subtasks
2. Launch 3 explore agents in parallel
3. Search code structure (parseCLI, version info, tests)
4. Implement code changes
5. Run tests for verification

**Result:**
- ✅ Collaboration mode verified successfully
- ✅ OpenCode auto-plans and executes
- ✅ Parallel processing improves efficiency
- ✅ Real-time progress feedback

## Common Questions

### Q1: What to do for first-time project?

**A:**
First-time project must initialize knowledge base:

1. Start OpenCode TUI:
   ```bash
   cd /path/to/project
   opencode
   ```

2. Run initialization:
   ```
   /init-deep
   ```

3. Exit after completion, then use acp mode for collaboration

**Purpose:**
- Create hierarchical AGENTS.md knowledge base
- Analyze project structure and dependencies
- Build code context, improve execution efficiency

### Q2: How to choose OpenCode mode?

**A:**
- **sisyphus** (default): Suitable for most tasks, auto-planning and parallel execution
- **hephaestus**: Suitable for complex tasks requiring deep analysis
- **prometheus**: Suitable for planning-only scenarios, no execution needed

### Q3: How to handle OpenCode execution failure?

**A:**
1. Check error messages and logs
2. Analyze failure reason (unclear requirements? technical limitations?)
3. Adjust plan or requirements
4. Restart OpenCode
5. If multiple failures, consider manual implementation

### Q4: How to optimize collaboration efficiency?

**A:**
1. **Clear requirements**: Reduce OpenCode's guessing and trial-and-error
2. **Reasonable breakdown**: Break large tasks into small tasks
3. **Parallel execution**: OpenCode auto-parallelizes
4. **Timely feedback**: Monitor progress, adjust promptly

### Q5: How can other Agents use this workflow?

**A:**
- **Butler Agent**: When making long-term plans, can delegate code modification tasks to OpenCode
- **Challenger Agent**: When finding optimization opportunities, can use OpenCode for quick implementation
- **Main Agent**: When receiving user requirements, can coordinate OpenCode execution

All Agents follow the same workflow: analyze requirements → create plan → start OpenCode → monitor progress → verify results.

## Rules

1. **Always use pty:true** - OpenCode needs a terminal
2. **Initialize first-time projects** - Run `/init-deep` before first use
3. **Clear requirements** - Specific, measurable, verifiable
4. **Monitor progress** - Check logs regularly, don't just wait
5. **Verify results** - Always check acceptance criteria
6. **Record lessons** - Update memory with successes and failures
7. **Be patient** - Don't kill sessions prematurely
8. **Use process:log** - Check progress without interfering

## Progress Updates

When spawning OpenCode in background, keep user informed:

- Send 1 short message when starting (what's running + where)
- Update only when something changes:
  - Milestone completes (build finished, tests passed)
  - OpenCode asks a question / needs input
  - Error occurs or user action needed
  - OpenCode finishes (include what changed + where)
- If killing session, immediately say why

This prevents "Agent failed before reply" confusion.

## Auto-Notify on Completion

For long-running tasks, append wake trigger to prompt:

```
... your task here.

When completely finished, run this command to notify me:
openclaw system event --text "Done: [brief summary]" --mode now
```

**Example:**

```bash
exec pty:true workdir:~/project background:true command:"opencode acp"
# ... initialize, create session ...
# Send prompt with wake trigger:
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"ses_xxx","prompt":[{"type":"text","text":"Build a REST API for todos.\n\nWhen completely finished, run: openclaw system event --text \"Done: Built todos REST API with CRUD endpoints\" --mode now"}]}}
```

This triggers immediate wake event — you get notified in seconds, not minutes.

## Version History

- **v1.0** (2026-02-16): Initial version
  - OpenCode 1.2.1
  - ACP protocol version 1
  - sisyphus mode
  - Test project: openclaw-qmd

---

**Last updated:** 2026-02-16  
**Maintainer:** Claw 🐾  
**Status:** ✅ Verified
