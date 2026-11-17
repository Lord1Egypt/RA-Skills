## Description:

Provides real-time geopolitical intelligence for Iran crisis monitoring, Trump Truth Social posts, prediction markets, and tracked-source briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dachein](https://clawhub.ai/user/dachein)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, journalists, and operators use this skill to request concise Iran crisis briefings, check Trump policy signals, investigate event evidence chains, and compare news and social feeds with prediction markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fast-moving geopolitical briefings and AI-generated assessments can be wrong, stale, or weakly sourced.

Mitigation: Frame briefing claims as assessments, check source counts and confidence, and cross-reference events with posts, news, and prediction-market endpoints before relying on conclusions.

Risk: Using the skill sends topic and feed requests to Capduck remote intelligence feeds.

Mitigation: Install and invoke it only when remote queries to those public feeds are acceptable for the user's workflow.

Risk: Responses may include bilingual English and Chinese content when translations are available.

Mitigation: Ask the agent to answer in a preferred language when bilingual output is not desired.

## Reference(s):

- [Iran Briefing on ClawHub](https://clawhub.ai/dachein/skills/iran-briefing)
- [dachein ClawHub profile](https://clawhub.ai/user/dachein)
- [Capduck skill API](https://skill.capduck.com)
- [Iran briefing endpoint](https://skill.capduck.com/iran)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with source confidence labels and optional bilingual English and Chinese excerpts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default responses are concise, usually 200-400 words unless the user asks for detail.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
