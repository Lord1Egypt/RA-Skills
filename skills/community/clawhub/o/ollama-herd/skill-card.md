## Description:

Ollama Herd helps agents inspect and operate a local Ollama fleet by routing LLM, image generation, speech-to-text, and embedding requests across macOS, Linux, and Windows devices with fleet health monitoring, queue management, and dashboard guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage self-hosted Ollama fleets, inspect node and model health, query routing analytics, and issue guarded curl commands for model and router operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to pull or delete Ollama models, which may consume substantial disk space or remove local assets.

Mitigation: Require explicit user confirmation before pulling or deleting models, and verify the target model and node before executing the command.

Risk: Router traces, prompts, and local fleet telemetry may be visible through documented local APIs and logs.

Mitigation: Treat the router and nodes as trusted local services, avoid exposing them to untrusted networks, and inspect traces only when the user intends it.

Risk: Installation and runtime commands depend on package and local-service behavior outside the artifact itself.

Mitigation: Use a virtual environment where practical and pin ollama-herd to the reviewed version 1.5.3 for reproducible use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ollama-herd)
- [PyPI project](https://pypi.org/project/ollama-herd/)
- [Project homepage](https://github.com/geeks-accelerator/ollama-herd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, curl examples, JSON endpoint descriptions, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Ollama Herd endpoints, local trace databases, and fleet configuration paths.]

## Skill Version(s):

1.5.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
