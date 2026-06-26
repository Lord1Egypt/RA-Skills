# Multi Agent Analysis and Execution Skill

This skill implements a **strict, step-by-step orchestration protocol** for executing complex tasks using multiple agents under a single coordinator. It is NOT optional guidance - it is a **deterministic execution contract** that must be followed exactly.

## 🔒 MANDATORY EXECUTION CONTRACT

When this skill is invoked, the following is **strictly required**:

→ **ALL phases MUST be executed** (Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4)
→ **ALL artifacts MUST be produced** (TASK_PLAN.md, DEPENDENCY_GRAPH.md, EXECUTION_GROUPS.md, AGENT_REQUIREMENTS.md, STATE.md, REPORT.final, agent prompts, and coordinator prompt)
→ **NO shortcuts are allowed**
→ **NO phases may be skipped**
→ **NO direct answers may be given** (the coordinator must not answer the user's question directly)
→ **NO task delegation** (the coordinator must not delegate the entire skill execution to another agent)

**Violation of any of these requirements results in an INVALID RUN.**

## How to Invoke This Skill Correctly

To properly invoke this skill for a new problem, you must:

### 1. State Your Problem Clearly
Begin by clearly describing what you want to achieve. For example:
> "I need to audit our web application's security configuration. We recently updated our authentication system and need to verify that all old API keys have been removed, check that new JWT token validation is properly implemented across all services, and ensure that rate limiting is correctly configured on all public endpoints."

### 2. Request Full Skill Execution
You must request the complete execution of the skill's mandatory protocol. Say something like:
> "Please execute the multi_agent_coordinator skill in full for this security audit problem. Generate all required planning artifacts, execute all phases, produce all required outputs, and generate the final report according to the strict execution contract."

## What Happens When You Invoke the Skill Correctly

When invoked in accordance with the mandatory execution contract, the skill will:

### Phase 0: Planning (MANDATORY)
1. Create a new timestamped directory: `workspace/coordinator_runs/multi_agent_run_YYYYMMDD_HHMMSS/`
2. Generate ALL planning documents inside that directory:
   - TASK_PLAN.md - High-level decomposition of your problem into atomic tasks
   - DEPENDENCY_GRAPH.md - Dependency analysis and sequencing logic
   - EXECUTION_GROUPS.md - Defined parallel groups and sequence order
   - AGENT_REQUIREMENTS.md - Multi-agent setup specifications
   - prompts/AGENT_1.prompt through prompts/AGENT_N.prompt - All agent prompts
   - prompts/COORDINATOR.prompt - Coordinator's ongoing governance prompt

### Phase 1: Execution (MANDATORY)
The coordinator will execute groups IN ORDER:
1. Spawn all agents in Group 1 (parallel analysis) using their prompts
2. Wait for all Group 1 agents to complete
3. Spawn Group 2 agent (waiting for specific Group 1 outputs)
4. Continue through all groups in sequence
5. Maintain coordinator session throughout
6. Apply cleanup policy after successful completion

### Phase 2: Output Verification (MANDATORY)
The coordinator MUST:
- Check that all required files exist
- Ensure no outputs are missing
- Validate that each output matches the required format
- Confirm outputs are complete

### Phase 3: Reporting (MANDATORY)
Create REPORT.final with:
- Summary of execution
- Results per agent
- Documentation of any failures
- Validation status
- Protocol compliance verification

### Phase 4: Cleanup (MANDATORY)
Apply the default cleanup policy (keep_last = 5):
- Never delete failed runs
- Never delete flagged runs
- Maintain the last 5 successful runs

## What You Provide as the User
To invoke this skill correctly for any new problem, you need to give:
1. *Clear problem statement* (what you want to achieve)
2. *Explicit request for full skill execution* (to trigger the mandatory protocol)

## What the Skill Handles Automatically
Once you've requested full skill execution, the skill manages:
- All agent spawning with their specific prompts
- Execution group sequencing and parallelization
- Session continuity maintenance
- Safety protocol enforcement
- Output namespacing and storage
- Cleanup policy application
- Final report generation
- ALL mandatory phases and artifact production

## Example Invocation Summary

You: "I need to audit our web application's security configuration..." [Problem Statement]
You: "Please execute the multi_agent_coordinator skill in full for this security audit..." [Full Execution Request]
[Skill executes ALL phases autonomously according to the mandatory contract]
You: Check results in `workspace/coordinator_runs/multi_agent_run_TIMESTAMP/REPORT.final`

## 🚫 PROTOCOL VIOLATIONS (INVALID RUN)

The skill run is INVALID if:
- Any phase is skipped
- Any required artifact is missing
- A direct answer is given instead of executing the protocol
- The coordinator delegates the entire skill execution
- STATE.md is missing or incomplete
- The execution groups are not followed in sequence

## 🔐 ENFORCEMENT PRINCIPLE

This skill is a **SYSTEM PROTOCOL**.

The coordinator has:
- ZERO discretion to skip phases
- ZERO authority to simplify the execution
- ZERO option to provide direct answers

Execution MUST be:
- explicit
- complete
- auditable
- fully compliant with the mandatory execution contract

When in doubt, request full skill execution and allow the skill to manage all phases according to its strict protocol.