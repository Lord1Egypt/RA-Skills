## Description:

Share a live preview of a website under development via an AiTun tunnel, with hot-reload support so users can see changes in real time as an agent edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to share an in-progress local website through an AiTun tunnel so users can review live changes during iterative development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands can execute downloaded shell or PowerShell code during setup.

Mitigation: Prefer the pip or uv package path in an isolated environment before using the skill.

Risk: A public preview tunnel can expose sensitive local routes, secrets, private repositories, or production data.

Mitigation: Tunnel only non-sensitive local previews, avoid admin and debug routes, and stop the development server and tunnel when the session ends.

## Reference(s):

- [AiTun homepage](https://aitun.cc)
- [ClawHub listing](https://clawhub.ai/ctz168/live-preview)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/live-preview)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands to install AiTun, start a local development server, open a public tunnel, share the preview URL, and clean up running processes.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
