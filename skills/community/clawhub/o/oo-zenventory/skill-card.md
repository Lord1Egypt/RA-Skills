## Description:

Use Zenventory through an OOMOL-connected account to read, create, and update inventory data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage Zenventory inventory through an OOMOL-connected account. It supports listing and retrieving items, creating items, and updating existing items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup instructs users to execute downloaded installer software without a separate approval step.

Mitigation: Install a verified oo CLI release yourself, review its automatic skill installation, and prevent automatic execution of the fallback installer.

Risk: Connecting an account grants the skill access to Zenventory, and some actions modify inventory data.

Mitigation: Connect only the intended Zenventory account and keep the documented user approvals for write and destructive actions.

## Reference(s):

- [Zenventory](https://www.zenventory.com)
- [Zenventory API documentation](https://docs.zenventory.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Zenventory skill on ClawHub](https://clawhub.ai/oomol/skills/oo-zenventory)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON request payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Zenventory data; create and update actions change inventory state and require user approval.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
