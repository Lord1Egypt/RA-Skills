## Description:

AutoSkills CLI detects project types such as web, Python, academic, finance, marketing, and media projects, then recommends and installs matching AgentSkills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamwgp](https://clawhub.ai/user/adamwgp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use AutoSkills CLI to inspect a project, identify its likely domain or stack, and get recommended AgentSkills with commands for detection, installation, listing, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run an unpinned remote npm package that may change the user's agent setup.

Mitigation: Use detection or listing modes first, prefer a pinned exact package version in an isolated environment, and allow installs or integration activation only after review.

Risk: Global installation can keep the CLI available across future sessions.

Mitigation: Avoid global installation unless persistent availability is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adamwgp/skills/our-autoskills)
- [Project homepage](https://github.com/adamwgp/our-autoskills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run npm and ClawHub commands that change the user's local agent skill setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
