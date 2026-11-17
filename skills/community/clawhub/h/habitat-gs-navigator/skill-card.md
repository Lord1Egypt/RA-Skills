## Description:

Habitat-GS Navigator helps agents navigate and interact with photo-realistic 3D Gaussian Splatting environments through the Habitat-GS Bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the0xka1](https://clawhub.ai/user/the0xka1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to drive Habitat-GS navigation episodes, inspect observations, choose movement actions, and interact with a local Habitat-GS Bridge server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable third-party bridge code before use.

Mitigation: Use a virtual environment or container and pin and inspect a trusted habitat-gs-bridge commit before installation.

Risk: The bridge can be configured to non-local endpoints.

Mitigation: Keep the bridge bound to local trusted endpoints unless a reviewer explicitly approves another endpoint.

Risk: Episode logs and generated lessons could be used to update shared memory or skills.

Mitigation: Require explicit human review before logs or lessons update shared memory or create or modify skills.

## Reference(s):

- [Habitat-GS Bridge API Reference](references/api-reference.md)
- [Habitat-GS Bridge Setup](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/the0xka1/skills/habitat-gs-navigator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline bash code blocks and navigation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands for hab-cli, bridge server configuration, and episode logging notes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
