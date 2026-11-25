## Description:

Runs parallel prose and craft review agents against a voice profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and content teams can use the skill to review generated text against a voice profile before publishing. It returns prose and craft findings, with suggested corrections for hard failures and advisory findings for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A possible “review” trigger conflict could affect when the skill activates.

Mitigation: Check how the review trigger behaves in your agent setup before relying on it.

Risk: Security analysis was partial because referenced local files were unavailable for review.

Mitigation: Review the referenced components and confirm they are available and expected in your installation.

## Reference(s):

- [Scribe plugin reference](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review tables with findings and suggested corrections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are advisory except for documented hard failures, which may be auto-corrected.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
