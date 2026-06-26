---
name: intent-engineering
description: A meta-framework for designing, building, and orchestrating an ecosystem of strategically-aligned agent skills. This skill governs how the agent itself operates, ensuring that all created skills work together as a cohesive, transparent, and governable system aligned with your organization's goals and values.
---

# Intent Engineering: The Agent's Operating System

## Overview

This skill is more than a tool; it is the **operating system for the agent itself**. It provides a comprehensive meta-framework for building and managing an ecosystem of interconnected agent skills. When you ask the agent to build something, it uses *this very skill* to guide its own reasoning, decision-making, and implementation process.

This framework extends the principles of intent engineering to a multi-skill environment and, critically, to the agent's own behavior. It introduces a structured approach to **ecosystem architecture**, **data governance**, **skill composition**, **shared intent**, and **agent self-governance**.

## The Agent as the Orchestrator

The agent is not just a passive tool; it is the active orchestrator of this entire framework. This creates a virtuous cycle of recursive improvement.

1.  **Intent Amplification:** The agent takes your high-level, sometimes "shallow," prompts and uses this framework to translate them into well-architected, robust, and aligned skills.
2.  **Complexity Absorption:** The agent handles the intricate details of data contracts, orchestration patterns, and governance, allowing you to focus on strategic intent.
3.  **Self-Referential Governance:** The agent applies the principles of this framework to itself. Its decisions are logged, its outputs are validated against data contracts, and its actions are aligned with the shared intent. This is **meta-governance**.
4.  **Recursive Improvement:** The agent uses the `intent-engineering` skill to improve and extend the `intent-engineering` skill itself, creating a self-improving system.

## The Intent-Driven Skill Ecosystem Architecture

An aligned skill ecosystem consists of five core components that work together to ensure that individual skills are greater than the sum of their parts.

| Component | Description | Implementation |
| :--- | :--- | :--- |
| **1. Skill Registry** | A centralized, machine-readable inventory of all available skills, their capabilities, dependencies, and data contracts. | `references/skill_registry.json` |
| **2. Data Contracts** | Formal schemas (JSON Schema) defining the inputs and outputs for each skill, ensuring predictable and reliable data exchange. | `references/data_contracts/` |
| **3. Orchestration Engine** | A system for defining and executing workflows that compose multiple skills, handling data flow, and managing dependencies. | `scripts/orchestrator.py` |
| **4. Shared Intent Framework** | A global set of organizational goals, values, and decision boundaries that all skills inherit, ensuring consistent alignment. | `references/shared_intent.md` |
| **5. Agent Decision Framework** | The internal guidance system the agent uses to apply this framework, amplify user intent, and govern its own actions. | `references/agent_decision_framework.md` |

## The Enhanced 4-Phase Workflow

The agent follows this workflow when you ask it to build or modify a skill.

### Phase 1: Deconstruct Intent (Ecosystem-Aware)

**Objective:** To define a skill's strategic purpose *within the context of the broader ecosystem*.

**New Workflow Steps:**

1.  **Define Skill's Role:** In addition to its own goal, define how this skill contributes to the overall ecosystem.
2.  **Align with Shared Intent:** Consult the `references/shared_intent.md` to ensure the skill's values and boundaries are consistent with organizational-level principles.
3.  **Identify Dependencies:** Use the `references/skill_registry.json` to identify any existing skills this new skill will depend on.

### Phase 2: Map Capabilities & Define Data Contracts

**Objective:** To define the skill's tasks and formalize its data interfaces.

**New Workflow Steps:**

1.  **Design Workflow:** Decompose the skill's tasks as before.
2.  **Define Data Contracts:** For each input and output, create a formal JSON Schema in the `references/data_contracts/` directory.
3.  **Specify Data Lineage:** Document where the skill's input data comes from and where its output data goes.

### Phase 3: Build Infrastructure & Register the Skill

**Objective:** To build the skill's resources and make it discoverable by the ecosystem.

**New Workflow Steps:**

1.  **Build Resources:** Create scripts and templates as before.
2.  **Register the Skill:** Add a new entry to the `references/skill_registry.json`.

### Phase 4: Implement, Orchestrate, and Iterate

**Objective:** To implement the skill's logic, including its interactions with other skills.

**New Workflow Steps:**

1.  **Implement Logic:** Write the core logic for the skill.
2.  **Orchestrate Interactions:** Use the `scripts/orchestrator.py` to call other skills.
3.  **Validate and Deliver:** Validate the skill and its interactions within the ecosystem.

## Resources for Ecosystem Orchestration

This skill now includes a richer set of resources to manage the entire ecosystem:

*   `references/shared_intent.md`: Defines the global values and goals for the entire organization.
*   `references/skill_registry.json`: A central catalog of all skills.
*   `references/data_contracts/`: A directory containing all data contract schemas.
*   `references/agent_decision_framework.md`: The agent's internal guidance for applying this framework.
*   `references/recursive_skill_development.md`: A guide on how the agent can improve this skill itself.
*   `scripts/orchestrator.py`: A Python script for composing and executing multi-skill workflows.
*   `templates/agent_audit_log.md`: A template for auditing the agent's own actions during skill creation.
