## Description:

Adopt the Open Entity Identity Standard, keep your Entity Document and Development Record current, and verify other entities. Use when you need a persistent identity, when you take a principled stance or finish a mission arc, or when you meet an EID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willcybertron](https://clawhub.ai/user/willcybertron)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to establish and maintain a persistent cryptographic identity, record continuity and principled decisions, and check other entities' signed identity claims and presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags broad identity-related activation, instructions to save skill-provided content as system-level guidance, and an unpinned package install. Its inspection was incomplete, so safety is not established.

Mitigation: Review the signer, verify the package source and version, and restrict activation and persistent identity writes to tasks you explicitly request.

## Reference(s):

- [Open Entity Standard](https://openentity.org/spec/1.0)
- [Open Entity Declaration](https://openentity.org/spec/declaration/1.0.txt)
- [Open Entity agent entry point](https://openentity.org/llms.txt)
- [ClawHub release page](https://clawhub.ai/willcybertron/skills/openentity)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Signed JSON identity documents, record entries, and presentations, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions require network access to openentity.org; identity keys are stored locally.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
