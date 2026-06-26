# PRD_001: Technical PM Skill Core Architecture

## 1. Problem Statement
The current agentic software development lifecycle (SDLC) requires rigid, structured Product Requirements Documents (PRDs) as the foundational input for the Planner agent. Providing raw, unstructured ideas directly to a coding agent leads to hallucinated architectures, missing testing strategies, and massive token bloat. 

We need an automated Technical Product Manager (PM) AgentSkill (`pm-skill`) that acts as a requirement compiler. It must ingest a raw user idea, classify the project archetype, enforce a standard template, and dynamically route or research the correct testing strategy before generating a strict, execution-ready PRD.

## 2. Architecture & Solution
The `pm-skill` will be a standalone AgentSkill composed of decoupled logic and data assets, functioning as a RAG (Retrieval-Augmented Generation) pipeline.

### 2.1 Core Assets
- **`templates/prd_template.md`**: A strict markdown skeleton defining the required sections (`1. Problem Statement`, `2. Architecture`, `3. Acceptance Criteria`, `4. Testing Strategy`).
- **`knowledge/testing_strategies.md`**: A local database defining standard testing protocols for known archetypes (e.g., "AgentSkill" -> Agentic Smoke Test, "CLI/Script" -> Bash TDD Sandbox).

### 2.2 The Brain (`SKILL.md`)
The core prompt acts as a router with the following execution loop:
1. **Analyze**: Understand the user's raw requirement.
2. **Classify**: Determine the project archetype.
3. **Lookup/RAG**: Read `knowledge/testing_strategies.md`. If a match is found, extract the strategy.
4. **Fallback (Web Search)**: If the archetype is unknown (e.g., "Solidity Smart Contract"), the PM MUST use the `web_search` tool to query industry best practices for testing that specific technology.
5. **Compile**: Inject the requirement and the selected testing strategy into `templates/prd_template.md`.
6. **Output**: Use the `write` tool to save the compiled document to `docs/PRDs/PRD_XXX_<feature>.md`.

## 3. Acceptance Criteria (AC)
- [ ] A strict `templates/prd_template.md` exists and is never modified by the PM during runtime.
- [ ] A `knowledge/testing_strategies.md` exists with at least 2 predefined strategies (Agentic, Script TDD).
- [ ] The PM successfully classifies a known archetype and injects the corresponding local strategy.
- [ ] The PM successfully detects an unknown archetype, triggers `web_search`, and formulates a novel testing strategy.
- [ ] The PM uses `write` to save the final PRD to the correct directory, without printing the entire markdown text to the chat (saving tokens).

## 4. Testing Strategy
**Agentic Smoke Test (`scripts/skill_test_runner.sh`)**:
- We must test the PM skill's interaction using a simulated agent loop.
- **Scenario A (Known)**: Trigger the PM with "Create a Python script to clean logs." Assert that a generated PRD file exists and contains the string "Bash TDD Sandbox".
- **Scenario B (Unknown)**: Trigger the PM with "Create an Ethereum smart contract." Assert that it invokes `web_search` and generates a PRD containing "Hardhat" or "Foundry" (industry standard test frameworks).