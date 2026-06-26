# SKILL: LoR (Loop of Resilience)

## Metadata
- **Name**: LoR (Loop of Resilience)
- **Category**: Engineering, Verification, Chain of Thought (CoT), Agent Reliability
- **Description**: A modular 5-step engineering verification loop for complex tasks. It implements a sophisticated Chain of Thought (CoT) paradigm, automating the Raw Reply -> Verification Planning -> Forced Execution -> Result Checking -> Final Output flow.
- **Repository**: https://github.com/lumi77-mac/lor-skill

## Usage
- Auto-triggered on complex tasks (coding, architecture, complex planning).
- Explicit trigger via `/lor [task]` or `@[AgentName] /lor [task]`.

## Requirements
- Node.js (v16.0.0 or higher)
- OpenClaw execution environment

## Auto-Registration
- The system outputs a registration hook `[REGISTER_LOR_SKILL]` upon installation.
- **Agent Memory**: Agents should detect this hook and register the skill in their `MEMORY.md`.

## Safety Constraints
- Require user confirmation for destructive operations (`exec`, `write`, `edit`).
- Read-only operations (`read`, `search`) execute automatically.
- Max 3 retries in Step 4.
