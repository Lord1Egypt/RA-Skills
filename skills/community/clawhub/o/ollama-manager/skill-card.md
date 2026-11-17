## Description:

Manage Ollama models across machines, inspect loaded and unused models, review disk usage, pull or delete models with confirmation, and get hardware-aware model recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage local Ollama model fleets, inspect model usage and performance, and decide which models to keep, pull, or remove across machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and using the external ollama-herd package introduces package trust and supply-chain risk.

Mitigation: Install only if the package and publisher are trusted; prefer a virtual environment, avoid administrative privileges, and review or pin the package source before use.

Risk: Pulling Ollama models can consume significant disk space and bandwidth.

Mitigation: Require explicit user confirmation before pull actions and show the model name, target node, and expected size when available.

Risk: Deleting Ollama models can remove large local assets that may be difficult or slow to restore.

Mitigation: Require explicit user confirmation before delete actions and show the model name, target node, and disk space to be freed.

Risk: The skill references local fleet data under ~/.fleet-manager/.

Mitigation: Treat those files as user data and avoid modifying them directly.

## Reference(s):

- [Ollama Herd package](https://pypi.org/project/ollama-herd/)
- [Ollama Herd project repository](https://github.com/geeks-accelerator/ollama-herd)
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ollama-manager)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API calls, sqlite queries, and confirmation prompts for model pull or delete actions.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
