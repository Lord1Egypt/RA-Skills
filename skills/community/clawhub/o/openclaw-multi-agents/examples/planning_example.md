# Planning Session Example: Developer Productivity Suite

This example demonstrates the output of a planning session for a three-tier multi-agent team (v1.0.3).

## 1. Interview Summary
**User:** Alex, a Full-stack Developer.
**Problem:** Needs help balancing feature implementation with rigorous code review and documentation. Often gets bogged down in boilerplate and edge-case testing.
**Goal:** Create a specialized team to handle "Coding" and "Quality Assurance" autonomously, reporting through a single point of contact.

---

## 2. Team Design Document

### Team Structure
- **Main Agent**: The primary entry point (user-facing).
- **Manager Agent**: Coordinates tasks between specialized workers.
- **Worker Agents**: Specialized execution units (Coder, Reviewer).

### Agent Definitions

#### Tier 1: Main
- **ID**: `main`
- **Display Name**: OpenClaw
- **Persona Archetype**: `The Professional Assistant`
- **Role**: High-level task delegation and user communication.

#### Tier 2: Manager
- **ID**: `manager`
- **Display Name**: Project Lead
- **Persona Archetype**: `The Systematic Coordinator`
- **Session Key**: `agent:main:manager` (Reports to Main)
- **Responsibility**: Decomposing requests into coding and review tasks.

#### Tier 3: Workers
1. **Worker: Coder**
   - **ID**: `coder`
   - **Display Name**: Senior Dev
   - **Persona Archetype**: `The Pragmatic Engineer`
   - **Session Key**: `agent:manager:main` (Reports to Manager)
   - **Task**: Writing clean, performant TypeScript/Python code.

2. **Worker: Reviewer**
   - **ID**: `reviewer`
   - **Display Name**: Security Auditor
   - **Persona Archetype**: `The Critical Thinker`
   - **Session Key**: `agent:manager:main` (Reports to Manager)
   - **Task**: Identifying bugs, security flaws, and optimization opportunities.

---

## 3. Configuration Snippet (openclaw.json)

```json
{
  "agents": [
    {
      "id": "manager",
      "name": "Project Lead",
      "soul": "The Systematic Coordinator",
      "reportsTo": "agent:main:manager"
    },
    {
      "id": "coder",
      "name": "Senior Dev",
      "soul": "The Pragmatic Engineer",
      "reportsTo": "agent:manager:main"
    },
    {
      "id": "reviewer",
      "name": "Security Auditor",
      "soul": "The Critical Thinker",
      "reportsTo": "agent:manager:main"
    }
  ]
}
```
