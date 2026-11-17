## Description:

Produces specific, prioritized action plans based on Meta Ads campaign analysis data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and Meta Ads operators use this skill after campaign analysis to convert performance findings into one to three prioritized, data-backed actions in Meta Ads Manager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Meta Ads campaign analysis context from the current session.

Mitigation: Review what campaign data is available in the session before invoking the skill.

Risk: Recommendations may include pauses, budget changes, or other campaign actions that affect ad delivery.

Mitigation: Review each recommendation before applying changes manually in Meta Ads Manager.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendations with concise context, prioritized action steps, data-backed reasons, and optional observations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires existing campaign analysis context; if analysis data is missing, asks which time period to analyze first.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
