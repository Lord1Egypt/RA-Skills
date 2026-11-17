# Multi-Agent Governance

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-blue.svg)](https://clawhub.ai/skills/multi-agent-governance)

A comprehensive governance system for managing agent roles, responsibilities, handoff policies, and conflict resolution in multi-agent environments.

## Overview

This Skill provides a complete framework for coordinating multiple AI agents in collaborative workflows. It defines clear role boundaries, enforces handoff policies, and resolves conflicts to ensure smooth multi-agent collaboration.

## Key Features

- **9 predefined agent roles** — Standard template includes orchestrator, requirement, design, implementation, code review, test planner, verification, reflection, and documentation agents
- **Flexible templates** — Choose from standard (9 agents), simplified (5 agents), or minimal (3 agents) templates
- **Custom roles** — Register your own agent roles with specific responsibilities and constraints
- **Handoff validation** — Ensure all required fields are present when agents hand off work
- **Conflict resolution** — Multiple strategies for resolving agent disagreements (orchestrator-first, user-first, voting)
- **Configuration persistence** — Save and load governance configurations to YAML or JSON
- **Multi-framework support** — Works with OpenClaw, LangChain, AutoGen, CrewAI

## Installation

```bash
# Install from ClawHub
openclaw skills install multi-agent-governance

# Or clone from GitHub
git clone https://github.com/Terr123123/openclaw-skills.git
cd openclaw-skills/core-stack/multi-agent-governance
pip install -e .
```

## Quick Start

```python
from multi_agent_governance import MultiAgentGovernance

# Initialize governance system
governance = MultiAgentGovernance(template="standard")

# List registered agents
print(governance.list_roles())
# ['orchestrator_agent', 'requirement_agent', 'design_agent', ...]

# Validate handoff
result = governance.validate_handoff(
    from_agent="requirement_agent",
    to_agent="design_agent",
    handoff_data={
        "from": "requirement_agent",
        "to": "design_agent",
        "change_id": "change-123",
        "inputs": {"proposal.md": "..."},
        "required_outputs": ["design.md"]
    }
)

# Resolve conflict
resolution = governance.resolve_conflict(
    agents=["design_agent", "implementation_agent"],
    disagreement_type="workflow_selection_disputed",
    context={"proposal": "..."}
)
```

## Templates

### Standard Template (9 Agents)

Best for complex projects with full development lifecycle:

- **orchestrator_agent** — Coordinates workflow and agent assignments
- **requirement_agent** — Analyzes and validates requirements
- **design_agent** — Creates technical design
- **implementation_agent** — Implements code changes
- **code_review_agent** — Reviews code quality
- **test_planner_agent** — Plans test strategy
- **verification_agent** — Verifies implementation
- **reflection_agent** — Analyzes process and improvements
- **documentation_agent** — Updates documentation

### Simplified Template (5 Agents)

Best for medium complexity projects:

- orchestrator_agent, requirement_agent, implementation_agent, code_review_agent, verification_agent

### Minimal Template (3 Agents)

Best for simple projects:

- orchestrator_agent, implementation_agent, verification_agent

## Documentation

- [Usage Guide](docs/usage-guide.md) — Complete usage instructions
- [API Reference](docs/api-reference.md) — Detailed API documentation
- [Examples](examples/) — Practical code examples

## Use Cases

- Multi-agent workflow coordination
- Quality assurance through role boundaries
- Automated conflict resolution
- Configuration management for agent teams
- Governance reporting and monitoring

## Configuration

Save and load governance configurations:

```python
# Save configuration
governance.save_configuration("config.yaml")

# Load configuration
governance2 = MultiAgentGovernance(template="minimal")
governance2.load_configuration("config.yaml")
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License — See [LICENSE](LICENSE) for details

## Author

Terr123123

## Links

- **ClawHub**: https://clawhub.ai/skills/multi-agent-governance
- **GitHub**: https://github.com/Terr123123/openclaw-skills
- **OpenClaw**: https://openclaw.ai