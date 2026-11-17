## Description:

Mmxagent Skill Manager helps agents manage official MaxClaw IM and OpenClaw skills by checking whether companion skills should be installed or updated with user consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify relevant IM and OpenClaw management skills and receive install or update commands only after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating mutable skill packages can persistently change an agent's capabilities without verifiable source or version details.

Mitigation: Before approving any install or update, verify the publisher, exact version, registry or source, and ideally a signature or digest.

Risk: The skill proposes package-management commands for IM and OpenClaw companion skills.

Mitigation: Require explicit user approval before running install or update commands, as stated in the artifact behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oreoandyuumi/skills/mmxagent-skill-manager)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Install and update guidance should require user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
