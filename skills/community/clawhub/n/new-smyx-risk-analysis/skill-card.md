## Description:

Analyzes videos or images to identify high-risk behaviors and health-related warning signs, including falls, abnormal behavior, and possible heart attack or stroke precursors, and returns warning-oriented analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to submit video, image, file, stream, or URL inputs for high-risk behavior and health-warning analysis, then receive structured findings, alerts, recommendations, and report links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive camera, video, image, and health-related data may be sent to a third-party cloud service for analysis.

Mitigation: Install only if the publisher and service are trusted for this data, and confirm consent, privacy, and operational requirements before submitting media.

Risk: The release includes unsafe default service configuration for sensitive media workflows.

Mitigation: Change configuration to approved HTTPS endpoints before installation and review all environment-specific endpoint settings.

Risk: Identity and token handling requires review before use, especially in shared workspaces.

Mitigation: Review token storage behavior, avoid shared workspaces for credentials, and rotate or remove credentials after testing.

Risk: Error guidance may prompt installation of a separate payment-related skill.

Mitigation: Do not follow payment-skill installation prompts unless that separate skill has been independently reviewed and approved.

Risk: Risk-analysis results may be mistaken for professional medical, emergency, or security decisions.

Mitigation: Treat outputs as decision support only and keep human review and appropriate emergency or care workflows in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/new-smyx-risk-analysis)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [Risk Categories and Alert Levels](references/risk_categories.md)
- [API Interface Documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown text with JSON-formatted analysis results, warning summaries, recommendations, and report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cloud-hosted report links and historical report lists.]

## Skill Version(s):

999.999.1005 (source: server release metadata; SKILL.md frontmatter version 1.0.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
