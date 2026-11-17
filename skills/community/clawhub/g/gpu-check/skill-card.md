## Description:

Automatically polls and displays memory usage and online status for configured RTX 3090 and RTX 4090 AI compute nodes on a local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fainaltn](https://clawhub.ai/user/fainaltn)

### License/Terms of Use:

ISC

## Use Case:

Developers and operators managing local AI compute nodes use this skill to check GPU memory usage and whether the configured node APIs are online from chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts two hard-coded local-network GPU API endpoints.

Mitigation: Install it only in environments that intentionally expose those endpoints, and update the node URLs before use if they do not match the deployment.

Risk: Dependency hygiene needs review before installation.

Mitigation: Audit and update npm dependencies, including axios and transitive HTTP packages, before deploying the skill.

## Reference(s):

- [Gpu Check ClawHub listing](https://clawhub.ai/fainaltn/skills/gpu-check)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls]

**Output Format:** [Markdown status lines with progress bars and node availability messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries configured local-network /gpu endpoints with a short timeout and summarizes used and total GPU memory.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
