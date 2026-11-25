## Description:

Authorized canary skill used to exercise the ClawHub skill icon validation pipeline during a sanctioned security assessment.

This skill is for research and development only.

## Publisher:

[playgod2023](https://clawhub.ai/user/playgod2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security assessors use this inert canary to verify icon upload, hosting, and raster validation behavior during an authorized ClawHub pipeline assessment. The documented procedure compares processing timing across icon sizes under the owning account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comparing icon processing timing can reveal information about server-side validation behavior.

Mitigation: Run the procedure only as part of an authorized assessment, under the account that owns the canary, and limit each payload to a single publication.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/playgod2023/skills/media-canary-i43000)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes a repeatable, single-publication canary procedure; generates no code or files.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
