## Description:

Coordinates local multi-agent workflows using a shared blackboard, advisory permission scoring, token-budget checks, and persistent project context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jovancoding](https://clawhub.ai/user/jovancoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use it to coordinate agents in a trusted workspace through a shared blackboard and to track task budgets, advisory permission scores, and persistent project context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory manipulation could redirect writes to persistent context, permission, audit, or coordination data.

Mitigation: Install and run it in a trusted workspace with protected directory permissions, and review the scan guidance before use.

## Reference(s):

- [Network AI homepage](https://network-ai.org)
- [Network AI on ClawHub](https://clawhub.ai/jovancoding/skills/network-ai)
- [Network AI project documentation](https://github.com/Jovancoding/Network-AI)
- [ClawHub skill scan findings](https://github.com/Jovancoding/Network-AI/blob/main/SECURITY.md#clawhub-skill-scan-findings)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands]

**Output Format:** [JSON state files and Markdown coordination/context files, with status text on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent local state is stored under the project root and data/ (or data/<env>/).]

## Skill Version(s):

6.0.1 (source: server-resolved release, artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
