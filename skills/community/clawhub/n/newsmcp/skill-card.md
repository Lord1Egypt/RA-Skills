## Description:

Real-time world news briefings with AI-clustered events, topic classification, and geographic filtering. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pranciskus](https://clawhub.ai/user/pranciskus)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve concise, multi-story briefings on current events by topic, region, time window, and importance signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News topics, regions, and time windows may be visible to newsmcp.io through request URLs.

Mitigation: Use the skill only when sharing those news interests with the public API provider is acceptable.

Risk: Briefings rely on AI-generated event summaries and importance signals from the external service.

Mitigation: Review linked source articles before making consequential decisions from a briefing.

## Reference(s):

- [newsmcp homepage](https://newsmcp.io)
- [newsmcp API base](https://newsmcp.io/v1)
- [ClawHub skill page](https://clawhub.ai/pranciskus/skills/newsmcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown briefing with source links and optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the public newsmcp.io API and requires curl; no API key is requested.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
