## Description:

Use Leonardo.Ai through a connected OOMOL account to create and check generations and list available models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to submit Leonardo.Ai image, video, audio, or 3D generation jobs, check their status, and review available models through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer contents could not be verified.

Mitigation: Review and approve CLI installation separately before use.

Risk: Automatic oo setup may introduce undisclosed changes to other agent skills.

Mitigation: Consider disabling automatic synchronization with OO_SKILLS_SYNC_DISABLED before running oo.

Risk: Generation requests may incur costs, and OOMOL mediates account access and requests.

Mitigation: Review generation parameters and associated cost before creating a job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-leonardo-ai)
- [Leonardo.Ai API documentation](https://docs.leonardo.ai/docs/getting-started)
- [Leonardo.Ai](https://leonardo.ai)
- [oo CLI command and environment variable controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Generated media]

**Output Format:** [JSON action requests and results, with generated media returned through Leonardo.Ai]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation jobs may produce images, video, audio, or 3D content; results include job status and media URLs.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
