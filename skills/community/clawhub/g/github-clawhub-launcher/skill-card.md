## Description:

Review GitHub and ClawHub release plans, metadata, tags, release notes, and final publish order before a human runs any commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to review GitHub and ClawHub release metadata, public wording, release notes, tests, audit checks, and the final human-run publishing order before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release-review guidance could be mistaken for authorization to publish or modify release assets.

Mitigation: Use the skill for checklist review and release-note drafting only; a human should inspect status, tests, scans, credentials boundaries, and publish commands before taking action.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown release review with a verdict, fixes, release-note draft, checklist, and publish order]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces review guidance only and keeps publishing actions under human control.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
