## Description:

Analyze HTTP security headers for URLs, assign A-F grades, and provide OWASP-aligned recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to check website response headers, grade security posture, and generate prioritized remediation guidance for web server and CDN configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound HTTP HEAD requests to user-provided targets, including internal or private addresses.

Mitigation: Run scans only against domains you own or are authorized to test, and avoid localhost, private/internal IP ranges, cloud metadata addresses, and URLs containing credentials or tokens.

Risk: Untrusted redirecting URLs may expose the agent's network path or reach unintended targets.

Mitigation: Use trusted target URLs and review redirect behavior before scanning URLs where network exposure is a concern.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/http-security-headers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or Markdown reports with grades, findings, and remediation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI exit codes can indicate whether results meet the configured minimum grade.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
