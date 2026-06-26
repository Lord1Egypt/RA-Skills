# Team Design Document Template

**Project:** {{project_name}}  
**Workflow:** {{workflow_type}}  
**Creation Date:** {{creation_date}}  
**Version:** {{version}}  

---

## 1. Project/Workflow Summary

### 1.1 Core Objectives
{{primary_goals}}

### 1.2 Workflow Description
```
{{workflow_description}}
```

### 1.3 Inputs & Outputs
| Type | Content | Format |
|------|------|------|
| Input | {{input_description}} | {{input_format}} |
| Output | {{output_description}} | {{output_format}} |

### 1.4 Current State
- **Existing Tools/Systems:** {{current_tools}}
- **Team Size:** {{team_size}}
- **Execution Frequency:** {{execution_frequency}}

---

## 2. Identified Pain Points

### 2.1 Primary Pain Points
| Priority | Description | Impact Level | Frequency |
|--------|----------|----------|------|
| P0 | {{pain_point_1}} | High/Medium/Low | {{frequency_1}} |
| P1 | {{pain_point_2}} | High/Medium/Low | {{frequency_2}} |
| P2 | {{pain_point_3}} | High/Medium/Low | {{frequency_3}} |

### 2.2 Detailed Pain Point Analysis

#### Pain Point 1: {{pain_point_1_title}}
**Symptoms:** {{symptoms_1}}  
**Root Cause:** {{root_cause_1}}  
**Desired Improvement:** {{desired_improvement_1}}

#### Pain Point 2: {{pain_point_2_title}}
**Symptoms:** {{symptoms_2}}  
**Root Cause:** {{root_cause_2}}  
**Desired Improvement:** {{desired_improvement_2}}

#### Pain Point 3: {{pain_point_3_title}}
**Symptoms:** {{symptoms_3}}  
**Root Cause:** {{root_cause_3}}  
**Desired Improvement:** {{desired_improvement_3}}

---

## 3. Recommended Team Configuration

### 3.1 Three-Tier Architecture Design

```
┌─────────────────────────────────────────────────────────────┐
│                            User                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                         Main Agent                          │
│                Role: Pure Relay                             │
│                Duties: Communication, Dispatch, Reporting   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                       Manager Agent                         │
│                Role: Planning & Orchestration               │
│                Duties: Task Decomposition, QA, Worker Mgmt  │
└───────────┬───────────┬───────────┬─────────────────────────┘
            │           │           │
            ▼           ▼           ▼
┌───────────────┐ ┌───────────┐ ┌───────────────┐
│  Worker 1     │ │ Worker 2  │ │  Worker 3     │
│  {{role_1}}   │ │ {{role_2}}│ │  {{role_3}}   │
└───────────────┘ └───────────┘ └───────────────┘
```

### 3.2 Agent Detailed Configuration

#### Main Agent
| Attribute | Configuration |
|------|------|
| Agent ID | `main` |
| Persona Prototype | {{main_persona}} |
| Task Category | {{main_task_category}} |
| Core Duties | User Communication, Intelligent Dispatch, Status Aggregation |
| Reports To | User |

#### Manager Agent
| Attribute | Configuration |
|------|------|
| Agent ID | `manager` |
| Persona Prototype | {{manager_persona}} (Suggested: Drucker Upgraded / Project Manager) |
| Task Category | {{manager_task_category}} |
| Core Duties | Planning, Coordination, Verification, Quality Control |
| Reports To | Main Agent (High-level status) |
| Manages | Worker Agents |

#### Worker Agents

| Agent ID | Persona Prototype | Role | Task Category | Core Duties | Signature Characteristic |
|----------|----------|----------|----------|----------|------------|
| {{worker_1_id}} | {{worker_1_persona}} | {{worker_1_role}} | {{worker_1_category}} | {{worker_1_duties}} | {{worker_1_quote}} |
| {{worker_2_id}} | {{worker_2_persona}} | {{worker_2_role}} | {{worker_2_category}} | {{worker_2_duties}} | {{worker_2_quote}} |
| {{worker_3_id}} | {{worker_3_persona}} | {{worker_3_role}} | {{worker_3_category}} | {{worker_3_duties}} | {{worker_3_quote}} |
| {{worker_4_id}} | {{worker_4_persona}} | {{worker_4_role}} | {{worker_4_category}} | {{worker_4_duties}} | {{worker_4_quote}} |

### 3.3 Persona Selection Reasoning

#### {{worker_1_persona}}
**Reasoning:** {{persona_1_reasoning}}  
**Applicable Scenarios:** {{persona_1_scenarios}}

#### {{worker_2_persona}}
**Reasoning:** {{persona_2_reasoning}}  
**Applicable Scenarios:** {{persona_2_scenarios}}

#### {{worker_3_persona}}
**Reasoning:** {{persona_3_reasoning}}  
**Applicable Scenarios:** {{persona_3_scenarios}}

---

## 4. Communication Workflow

### 4.1 Message Flow Diagram

```
User Request
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│  Main Agent                                                 │
│  ├─ Parse User Intent                                        │
│  ├─ Decide if Manager is needed                              │
│  └─ Forward to Manager or Respond Directly                   │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Manager Agent                                              │
│  ├─ Receive Task                                            │
│  ├─ Decompose Sub-tasks                                     │
│  ├─ Dispatch to Workers (sessions_send)                     │
│  ├─ Collect Results                                         │
│  ├─ Quality Verification (QA)                               │
│  └─ Aggregate Report to Main Agent                          │
└──────────┬─────────┬─────────┬──────────────────────────────┘
           │         │         │
           ▼         ▼         ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Worker 1 │ │ Worker 2 │ │ Worker 3 │
    │ (async)  │ │ (async)  │ │ (async)  │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         └────────────┼────────────┘
                      │
                      ▼
        Result Aggregation & Verification
                      │
                      ▼
              Return to Main Agent
                      │
                      ▼
                    User
```

### 4.2 Communication Protocol

#### Main Agent → Manager
```
sessions_send(
  sessionKey="agent:manager:main",
  message="Task description + Context + Constraints + Lessons",
  timeoutSeconds=0  // Async, non-blocking
)
```

#### Manager → Workers
```
sessions_send(
  sessionKey="agent:<worker_id>:manager",
  message="Sub-task + Dependencies + Acceptance Criteria + Lessons",
  timeoutSeconds=0  // Async, parallel execution
)
```

### 4.3 Status Reporting Mechanism

| Level | Content | Frequency | Format |
|------|----------|------|------|
| Worker → Manager | Done / Blocked / Failed | Immediate | Structured JSON |
| Manager → Main | Milestone Summary, Key Decisions | Milestones | Summary + Detail Links |
| Main → User | High-level Status, Final Result | On Demand | Natural Language |

---

## 5. Task Category Mapping

### 5.1 Task Category Allocation

| Agent | Primary Task Category | Fallback Chain | Description |
|-------|--------------|----------------|------|
| Main | {{main_category}} | {{main_fallback}} | Intelligent dispatch, no direct processing |
| Manager | {{manager_category}} | {{manager_fallback}} | Planning & Coordination, QA |
| Worker 1 | {{worker1_category}} | {{worker1_fallback}} | {{worker1_note}} |
| Worker 2 | {{worker2_category}} | {{worker2_fallback}} | {{worker2_note}} |
| Worker 3 | {{worker3_category}} | {{worker3_fallback}} | {{worker3_note}} |

### 5.2 Task Category Reference Definitions

| Category | Model Type | Applicable Scenarios |
|------|----------|----------|
| `ultrabrain` | GPT/Gemini Pro | Strategic Planning, Complex Reasoning |
| `deep` | GPT Codex | Deep Code Exploration, Autonomous Development |
| `visual-engineering` | Gemini Pro | Visual Engineering, UI/UX |
| `unspecified-high` | Claude Opus | Strict Instruction Following, Quality Review |
| `quick` | Grok/Haiku/Flash | Rapid Response, Simple Tasks |

---

## 6. Knowledge Transfer Strategy

### 6.1 Experience Sharing Mechanism

```
Worker A Completes Task
    │
    ▼
Extract Key Learnings
    │
    ▼
Write to notepads/<plan>/learnings.md
    │
    ▼
Manager attaches lessons when dispatching
    │
    ▼
Worker B receives Task + History Lessons
```

### 6.2 Experience Record Format

```markdown
## {{learning_title}}
**Source:** {{source_agent}}  
**Scenario:** {{scenario}}  
**Problem:** {{problem}}  
**Solution:** {{solution}}  
**Key Snippet:** {{key_snippet}}  
**Reuse Advice:** {{reuse_advice}}
```

---

## 7. Risk Assessment

### 7.1 Potential Risks

| Risk | Probability | Impact | Mitigation |
|------|--------|------|----------|
| {{risk_1}} | High/Medium/Low | High/Medium/Low | {{mitigation_1}} |
| {{risk_2}} | High/Medium/Low | High/Medium/Low | {{mitigation_2}} |
| {{risk_3}} | High/Medium/Low | High/Medium/Low | {{mitigation_3}} |

### 7.2 Fallback Strategy

| Agent | Primary Model | Fallback Option 1 | Fallback Option 2 |
|-------|--------|------------|------------|
| Manager | {{manager_primary}} | {{manager_fallback_1}} | {{manager_fallback_2}} |
| Worker 1 | {{w1_primary}} | {{w1_fallback_1}} | {{w1_fallback_2}} |
| Worker 2 | {{w2_primary}} | {{w2_fallback_1}} | {{w2_fallback_2}} |

---

## 8. Implementation Checklist

### 8.1 Pre-Implementation Check

- [ ] User has confirmed the team design
- [ ] All Agent IDs are defined
- [ ] Persona prototypes are selected and recorded
- [ ] Task categories are assigned
- [ ] Fallback chains are configured
- [ ] Working directories created
- [ ] openclaw.json backed up

### 8.2 Implementation Steps

- [ ] Step 1: Create Manager Agent Workspace
  - **Note:** `bash scripts/setup_agent.sh` may not exist in all environments.
  - **Manual Fallback:** `mkdir -p agents/manager`
  ```bash
  bash scripts/setup_agent.sh manager "{{manager_persona}}" {{manager_model}}
  ```

- [ ] Step 2: Create Worker Agent Workspaces
  - **Manual Fallback:** `mkdir -p agents/{{worker_id}}`
  ```bash
  bash scripts/setup_agent.sh {{worker_1_id}} "{{worker_1_persona}}" {{worker_1_model}}
  bash scripts/setup_agent.sh {{worker_2_id}} "{{worker_2_persona}}" {{worker_2_model}}
  bash scripts/setup_agent.sh {{worker_3_id}} "{{worker_3_persona}}" {{worker_3_model}}
  ```

- [ ] Step 3: Configure openclaw.json
  - Add agents.list entries
  - Configure fallback chains
  - Set default models

- [ ] Step 4: Create SOUL.md Files
  - Manager Agent SOUL.md
  - Each Worker Agent SOUL.md

- [ ] Step 5: Create AGENTS.md Files
  - Manager Agent AGENTS.md
  - Each Worker Agent AGENTS.md

- [ ] Step 6: Restart OpenClaw Gateway
  ```bash
  openclaw gateway restart
  ```

- [ ] Step 7: Verify Agent Registration
  ```bash
  openclaw agents list
  ```

- [ ] Step 8: End-to-End Testing
  - Send test task
  - Verify message flow
  - Check result quality

### 8.3 Post-Implementation Check

- [ ] All Agents status: OK
- [ ] Message flow: No blocks
- [ ] Task quality: High
- [ ] User acceptance: Passed
- [ ] Documentation updated

---

## 9. User Confirmation

### 9.1 Design Approval

I have reviewed the above team design and confirm the following:

- [ ] Workflow description is accurate
- [ ] Pain point analysis reflects reality
- [ ] Recommended team configuration is reasonable
- [ ] Persona prototypes are appropriate
- [ ] Task category allocation is correct
- [ ] Implementation plan is feasible

### 9.2 Modification Notes (If any)

{{modification_notes}}

### 9.3 Approval Signature

**Approver:** {{approver_name}}  
**Date:** {{approval_date}}  
**Signature:** ___________________

---

## 10. Appendix

### 10.1 Reference Documents

- [SKILL.md](../SKILL.md) - Full Usage Guide
- [references/persona-library.md](../references/persona-library.md) - Persona Prototype Library
- [docs/task_categories_and_model_matching.md](../docs/task_categories_and_model_matching.md) - Task Category System
- [docs/architecture_guide.md](../docs/architecture_guide.md) - Architecture Details

### 10.2 Change History

| Version | Date | Changes | Author |
|------|------|----------|------|
| {{version}} | {{creation_date}} | Initial version | {{author}} |

---

**Document Generation:** Multi-Agent Orchestration Skill  
**Template Version:** 1.0.0  
