## Description:

Find influencers and creators across TikTok, Instagram, and YouTube by keyword; expand similar creators, enrich profiles, and build outreach-ready lead lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, partnerships, and growth teams use this skill to discover, enrich, and rank creator candidates across TikTok, Instagram, and YouTube for campaign outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign queries and API credentials can be sent to a configured gateway.

Mitigation: Use only a trusted HTTPS gateway and a trusted environment file for skill configuration.

Risk: The skill creates a persistent local install identifier that the gateway can use to correlate requests over time.

Mitigation: Review this behavior before installation and clear the local install identifier if the deployment requires reset or reduced correlation.

Risk: Creator profile, engagement, and brand-collaboration data may have gaps or quality caveats.

Mitigation: Require returned shortlists to include data gaps, selection rationale, and next-step validation before outreach.

## Reference(s):

- [API Index](artifact/references/api-index.md)
- [Request and Response Guide](artifact/references/request-response.md)
- [Operation Manifest](artifact/references/operations.json)
- [ClawHub Skill Page](https://clawhub.ai/chengyu-xixihaha/skills/influencer-lead-discovery)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with optional inline shell commands and JSON API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ordered top candidates, selection rationale, data-gap risks, and recommended next actions.]

## Skill Version(s):

1.0.5 (source: server release evidence and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
