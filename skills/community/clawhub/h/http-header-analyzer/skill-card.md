## Description:

Analyze HTTP security headers and TLS configuration. Find missing headers, weak ciphers, and misconfigurations in web applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan web application URLs for missing HTTP security headers, exposed server technology headers, and optional TLS connection details. The results are advisory and should be reviewed before relying on them for security decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS scans are performed without certificate validation, which can make scan results misleading.

Mitigation: Treat scan output as advisory unless certificate verification is enabled by default or intentionally insecure scans are clearly marked.

Risk: The TLS analysis is weaker than the skill description may imply.

Mitigation: Review TLS findings with a dedicated TLS assessment tool before using them for security decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hostilespider/skills/http-header-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown-style terminal output or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports present and missing headers, exposed technology headers, score, risk level, and optional TLS connection details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
