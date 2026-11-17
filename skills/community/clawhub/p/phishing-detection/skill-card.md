## Description:

Analyzes URLs using heuristic algorithms to detect and identify phishing threats in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, developers, email filtering systems, browser extensions, and web applications use this skill to submit URLs for phishing risk assessment before users interact with suspicious links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to the provider's external analysis API.

Mitigation: Avoid submitting private, internal, or token-bearing URLs unless the provider's privacy and retention practices meet your needs.

Risk: Heuristic phishing assessments can affect decisions about whether a link is blocked, allowed, or escalated.

Mitigation: Use the returned risk score, indicators, and confidence as decision support within a reviewed security workflow rather than as the only control for high-impact actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/phishing-detection)
- [ToolWeb](https://toolweb.in)
- [API Docs](https://api.mkkpro.com:8005/docs)
- [API Route](https://api.mkkpro.com/security/phishing-detection)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns URL phishing assessment fields such as risk score, threat indicators, confidence, and analysis timestamp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
