## Description:

Submit your project to Built at GrowthX, the community builder showcase for GrowthX members, using a GrowthX API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxt-admin](https://clawhub.ai/user/gxt-admin)

### License/Terms of Use:


## Use Case:

Developers and GrowthX members use this skill to inspect a workspace project, confirm project details, and submit the reviewed summary to the Built at GrowthX showcase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit project metadata, including name, description, stack, URL, and status, to GrowthX.

Mitigation: Review the detected project details and submit only after the user confirms the final payload.

Risk: The skill requires a GrowthX API key for authenticated submission.

Mitigation: Store the API key in the configured environment or OpenClaw configuration and avoid exposing it in shared logs or prompts.

## Reference(s):

- [Built at GrowthX Skill Page](https://clawhub.ai/gxt-admin/skills/growthx-bx-submit)
- [Built at GrowthX Project Submission API](https://backend.growthx.club/api/v1/bx/projects/agent)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, git, and a GROWTHX_API_KEY.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
