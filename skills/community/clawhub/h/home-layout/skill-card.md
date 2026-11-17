## Description:

Provides home-layout guidance such as space-use planning, furnishing inspiration, and movement-flow optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for home space planning, furnishing ideas, and layout-flow guidance. Reviewers should note that the artifact body also describes venue discovery fields such as queues, reservations, parking, and navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill identity and artifact instructions are inconsistent: the title and description indicate home-layout assistance, while the body describes venue discovery, queues, parking, navigation, and store visits.

Mitigation: Review before installing; either constrain use to the intended home-layout scope or correct the artifact instructions before release.

Risk: Venue, queue, hours, parking, and navigation details can be outdated or misleading if an agent treats the artifact body as operational guidance.

Mitigation: Require users or downstream agents to verify time-sensitive venue information with trusted live sources before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/home-layout)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise natural-language or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; output may include home-layout suggestions or, if the inconsistent artifact instructions are followed, venue-related information.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
