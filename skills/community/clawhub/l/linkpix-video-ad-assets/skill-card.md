## Description:

Helps marketers generate single or multiple product video ads for social feeds and brand campaigns using LinkPix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and advertisers use this skill to create and deliver product video ads in batches for social feeds, paid campaigns, and brand promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing external tooling or persisting shell settings changes the user's environment.

Mitigation: Confirm the qhkit package before installation and avoid persistent PATH or shell-profile changes without user approval.

Risk: A LinkPix API token is needed to access the service.

Mitigation: Ask the user to obtain their own token and avoid exposing it in shared output or logs.

Risk: Bulk generation consumes account credits and submitted tasks cannot be cancelled.

Mitigation: Check the cost estimate and obtain user confirmation before submitting bulk work.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-video-ad-assets)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with video links and task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated video links, task IDs, and credits charged are reported to the user.]

## Skill Version(s):

0.1.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
