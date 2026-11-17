## Description:

Analyzes Yandex.Metrika API data when a user asks about traffic, conversions, visitor behavior, or site reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimblemarketingapex-netizen](https://clawhub.ai/user/nimblemarketingapex-netizen)

### License/Terms of Use:


## Use Case:

External users, site owners, marketers, and analysts use this skill to summarize Yandex.Metrika traffic, conversions, visitor behavior, high-bounce pages, and conversion-funnel issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Yandex.Metrika token and counter ID could allow the agent to read analytics for a site the user did not intend to analyze.

Mitigation: Confirm the selected counter and use an appropriately scoped token before allowing the agent to read metrics.

Risk: Traffic, conversion, and visitor-behavior reports may contain sensitive business analytics.

Mitigation: Review generated findings and recommendations before sharing them outside the intended audience.

## Reference(s):

- [Metrika Analysis on ClawHub](https://clawhub.ai/nimblemarketingapex-netizen/skills/metrika-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis with concise findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on user-provided METRIKA_TOKEN and COUNTER_ID to read analytics for the selected site.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
