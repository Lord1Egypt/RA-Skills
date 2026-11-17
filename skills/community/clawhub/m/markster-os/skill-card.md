## Description:

This skill explains Markster OS, routes users to setup guidance, and asks for explicit approval before full installation or Git-backed workspace operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atiti](https://clawhub.ai/user/atiti)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this bootstrap skill to understand Markster OS, review setup steps, and initialize a Git-backed company workspace only after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to clone an upstream repository and run install.sh locally, giving an external installer broad local authority.

Mitigation: Trust and inspect the upstream repository and installer first, prefer a pinned reviewed commit or signed release, avoid sudo, and run setup in a constrained or disposable workspace.

Risk: Workspace remote attachment and first push can affect a company repository if approved without review.

Mitigation: Require explicit approval before remote or push commands and run markster-os validate . before treating the workspace as ready.

## Reference(s):

- [Markster OS repository](https://github.com/markster-public/markster-os)
- [Markster OS OpenClaw guide](https://github.com/markster-public/markster-os/blob/master/setup-prompts/openclaw.md)
- [Markster OS ClawHub listing](https://clawhub.ai/atiti/skills/markster-os)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before install, remote, or push commands.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
