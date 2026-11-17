## Description:

Provides real-time verified news briefs, search, trending news, and topic-focused intelligence reports from The Polaris Report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnytarrr](https://clawhub.ai/user/johnnytarrr)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to retrieve current news briefs, search verified news, inspect trending topics, and generate topic-focused intelligence summaries with confidence and bias indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News searches and brief topics are sent to The Polaris Report API by default.

Mitigation: Avoid sensitive queries unless the backend is trusted, or configure POLARIS_API_URL to an approved service.

Risk: Generated news briefs and intelligence summaries may be incomplete, time-sensitive, or misleading if treated as definitive.

Mitigation: Review confidence scores, bias ratings, source links, and the underlying brief before using results for decisions.

## Reference(s):

- [The Polaris Report](https://thepolarisreport.com)
- [API Documentation](https://thepolarisreport.com/docs)
- [Agent Integration Guide](https://thepolarisreport.com/agents)
- [Privacy Policy](https://thepolarisreport.com/privacy)
- [Publisher Profile](https://clawhub.ai/user/johnnytarrr)
- [Skill Page](https://clawhub.ai/johnnytarrr/skills/polaris-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text and Markdown-style summaries with links, confidence scores, bias ratings, and command error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is generated from The Polaris Report API responses and may include brief URLs, category labels, summaries, counter-arguments, confidence scores, and bias ratings.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
