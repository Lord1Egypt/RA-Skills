## Description:

Helps app teams triage customer reviews, draft and post approved public replies, identify product and keyword themes, and turn selected praise into screenshot slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iderasyh](https://clawhub.ai/user/iderasyh)

### License/Terms of Use:

MIT-0

## Use Case:

App teams use this skill to prioritize and respond to customer reviews, discover recurring feedback and search terms, and optionally showcase positive reviews in screenshot slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public review replies or deletions could expose an app team to reputational harm if applied incorrectly.

Mitigation: Show the exact review and proposed action, then obtain explicit approval for each reply or deletion before applying it.

Risk: Granting MetaRun access to review workflows and installing its CLI may exceed an organization's trust or supply-chain requirements.

Mitigation: Confirm MetaRun is trusted and access is appropriate before connecting it; use a pinned or preinstalled CLI where stricter supply-chain controls apply.

## Reference(s):

- [MetaRun review inbox skill release](https://clawhub.ai/iderasyh/skills/metarun-review-inbox)
- [MetaRun agents](https://metarun.dev/agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Screenshot slides]

**Output Format:** [Review triage and reply drafts in text or Markdown; optional screenshot slide updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public replies require explicit approval for each review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
