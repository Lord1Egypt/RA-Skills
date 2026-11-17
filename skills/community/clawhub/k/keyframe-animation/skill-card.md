## Description:

Creates a video from two user-provided still images by using one as the start frame, one as the end frame, and guiding an Ofox video job to generate the in-between motion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user provides two still images and wants one clip that starts on the first frame, ends on the second frame, and fills in the motion between them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to Ofox for video generation.

Mitigation: Confirm the user trusts the Ofox publisher and is comfortable sending those images before generation.

Risk: Paid generation can incur costs.

Mitigation: Review the dry-run cost table and proceed with billable commands only after explicit approval.

Risk: The workflow depends on an OFOX_API_KEY.

Mitigation: Keep the API key scoped to Ofox use and avoid exposing it in prompts, logs, or shared output.

Risk: The companion ofox-video-core installer path may affect what code is installed.

Mitigation: Prefer a reviewed or pinned installer path for ofox-video-core when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/keyframe-animation)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/keyframe-animation)
- [Ofox API keys](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, brief recaps, prompts, and cost-approval tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY for paid generation and uses an explicit approval step before billable runs.]

## Skill Version(s):

2.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
