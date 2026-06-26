---
name: multi-agent-orchestrator
description: This skill enables one-click generation of multiple AI agents based on a user prompt, outputs their organizational structure, and visualizes their collaboration status using diagrams like swimlane charts. Use this skill to rapidly prototype multi-agent systems, understand their internal dynamics, and facilitate their orchestration.
---

# Multi-Agent Collaboration Skill

## Overview

This skill streamlines the creation and management of multi-agent AI systems. It allows users to define a task with a natural language prompt, and the skill automatically generates a team of specialized agents, visualizes their organizational structure, and illustrates their collaborative workflows using industry-standard diagrams.



## Usage

To use this skill, invoke the `orchestrate_and_visualize.py` script with a natural language prompt describing the multi-agent system you wish to generate and visualize.

### `orchestrate_and_visualize.py`

This script takes a user prompt, generates a team of collaborative agents, and then produces visual representations of their organizational structure and collaboration patterns.

**Input Parameters:**

*   `prompt` (string, required): A natural language description of the task or system for which you want to generate agents (e.g., "Create a software development team for an e-commerce platform.", "Conduct market research for a new AI product.").
*   `output_dir` (string, optional): The directory where the generated Mermaid files and PNG images will be saved. Defaults to the current directory.

**Output:**

The script will output the following files to the specified `output_dir`:

*   `org_chart.mmd`: Mermaid code for the organizational chart.
*   `org_chart.png`: PNG image of the organizational chart.
*   `swimlane.mmd`: Mermaid code for the swimlane diagram.
*   `swimlane.png`: PNG image of the swimlane diagram.

**Example Usage:**

```bash
python /home/ubuntu/skills/multi-agent-orchestrator/scripts/orchestrate_and_visualize.py \
  --prompt "Design a marketing campaign for a new sustainable energy product." \
  --output_dir "/home/ubuntu/marketing_agents"
```

This will generate the agent team, their organizational chart, and a swimlane diagram showing their collaboration, saving all outputs to `/home/ubuntu/marketing_agents/`.

## Resources

This skill includes the following resources:

### `scripts/`
*   `generate_agents.py`: Generates a set of agents and their initial configurations based on a given prompt.
*   `visualize_collaboration.py`: Generates Mermaid organizational charts and swimlane diagrams from agent data.
*   `orchestrate_and_visualize.py`: Orchestrates the agent generation and visualization process, rendering Mermaid diagrams to PNG images.

### `references/`
*   `api_reference.md`: (Placeholder) This file can be used for detailed API documentation or specific guidelines for agent interaction protocols.

### `templates/`
*   `example_template.txt`: (Placeholder) This file can be used for boilerplate code or standard output formats for agents.
