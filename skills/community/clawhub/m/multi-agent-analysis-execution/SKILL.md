---
name: multi agent analysis and execution
description: Orchestrate complex multi-agent workflows with explicit coordinator planning, execution governance, and *automatic output management*. Each skill run creates its own isolated output namespace to prevent file accumulation and confusion from repeated executions.
version: 1.0.0
---

# multi_agent_coordinator - SKILL.md (Lean + Debug Mode)

## Description
Orchestrate complex multi-agent workflows with an explicit **coordinator-driven process** that plans, sequences, and governs execution across multiple agents.

This version keeps the system **lean by default** while preserving the **full coordination logic, guardrails, and execution discipline** required for reliable multi-agent workflows.

**Critical Rule:** When this skill is invoked, the coordinator process **MUST execute fully across all phases**. No phases may be skipped or partially executed.

---

## Core Principles

1. **Lean by default** — minimal files, fast execution
2. **Debug on demand** — full traceability when needed
3. **Run isolation always** — every run gets its own directory

---

## Run Directory (Always Created)

Each execution creates a unique directory:

```
Coordinator_runs/
└── run_YYYYMMDD_HHMMSS/
```

- No absolute paths
- Prevents collisions
- Keeps runs isolated

---

## Modes

```
mode = lean (default) | debug
```

### Lean Mode (default)
- Minimal output
- No intermediate files

### Debug Mode
- Full artifact generation
- Complete traceability

---

# The Five-Phase Coordinator Process

**MANDATORY EXECUTION CONTRACT**
- You MUST start at PHASE 0
- You MUST execute phases sequentially (0 → 4)
- You MUST NOT skip phases
- You MUST NOT perform ad-hoc reasoning outside the coordinator structure
- You MUST follow the planned execution (no improvisation during execution)

---

## PHASE 0: COORDINATOR PLANNING

This phase defines the **core intelligence of the skill** and MUST be executed carefully.

### Mandatory Planning Steps

1. **Task Plan Creation**
   - Analyze the problem
   - Answer: *"What steps are required to solve this?"*
   - Decompose into clear, atomic tasks
   - Limit the number of tasks to 15 for any given problem.

2. **Dependency Analysis**
   - Answer: *"What depends on what?"*
   - Identify ordering constraints
   - Identify parallelizable tasks

3. **Execution Group Formation**
   - Group independent tasks
   - Define strict execution order between groups

4. **Agent Specification (CRITICAL GUARDRAIL)**
   For each task (max 15 ):
   - Define a **single-purpose agent**
   - Assign a **clear responsibility**
   - Define:
     - Inputs
     - Outputs
     - Constraints (read/write, safety, isolation)
       - Work and scanning only limited to the workspace unless explicit approval of user
     - Agent prompt 
   - Each task MUST map to exactly one agent
   - No credentials, tokens etc should be passed or to be found in the generated prompt.
   - If the sub agent requires credentials they should be available via ENV or other tools.

5. **Coordinator Execution Strategy**
   The coordinator MUST:
   - Maintain full control of execution
   - Enforce group sequencing
   - Ensure all agents complete before proceeding
   - Handle failures explicitly (no silent failures)

### Lean Mode
- All planning done in memory

### Debug Mode
Persist planning artifacts

---

## PHASE 1: EXECUTION

This phase executes the previously defined plan with **strict governance**.

### Execution Rules (MANDATORY)

For each execution group in order:

1. Spawn all agents with the generated prompt of phase 0 in the group (parallel allowed)
2. Ensure agents only operate within their defined scope
3. Wait for ALL agents in the group to complete
4. Verify successful completion of each agent
5. ONLY THEN proceed to next group

### Failure Handling (GUARDRAIL)
- If an agent fails:
  - Coordinator MUST detect it
  - MUST stop progression OR handle explicitly
  - MUST report failure in final output

### Lean Mode
- In-memory execution

### Debug Mode
- Persist prompts and outputs

---

## PHASE 2: OUTPUT MANAGEMENT

### Core Rule
All outputs MUST remain scoped to the current run directory.

### Lean Mode
Only create:

```
runs/run_YYYYMMDD_HHMMSS/
└── REPORT.final
```

Optional:
```
└── run.log
```

### Debug Mode
Full structure:

```
runs/run_YYYYMMDD_HHMMSS/
├── TASK_PLAN.md
├── DEPENDENCY_GRAPH.md
├── EXECUTION_GROUPS.md
├── AGENT_REQUIREMENTS.md
├── prompts/
├── outputs/
└── REPORT.final
```

---

## PHASE 3: REPORTING

The coordinator MUST consolidate all results.

### Requirements
- Include results from ALL agents
- Verify execution order was respected
- Report any failures or inconsistencies

Output:
```
REPORT.final
```

---

## PHASE 4: CLEANUP

### Lean Mode
- Minimal footprint
- No additional cleanup required

### Debug Mode
Optional retention policy:

```
keep_last = N
```

---

# Guardrails Summary

- MUST execute all phases sequentially
- MUST NOT skip planning
- MUST NOT bypass coordinator
- MUST enforce task → agent mapping (1:1)
- MUST enforce execution group sequencing
- MUST detect and report failures
- MUST isolate each run in its own directory

---

# Summary

- Lean by default, debug when needed
- Full coordinator logic preserved
- Strong execution guarantees via guardrails
- Every run isolated

