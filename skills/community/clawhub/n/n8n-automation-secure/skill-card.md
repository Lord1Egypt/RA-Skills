## Description:

Secure n8n workflow automation guidance for agents that use n8n APIs with environment-based credentials, setup validation, and security-oriented workflow operation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelmaz](https://clawhub.ai/user/nelmaz)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to inspect, execute, and maintain n8n workflows from an agent while following documented setup, credential, and review practices for API-driven workflow changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose powerful n8n workflow API actions, including workflow execution or modification.

Mitigation: Use narrowly scoped n8n API keys, verify commands before execution, and keep workflow changes under explicit human review.

Risk: Advertised permission modes, confirmations, audit logs, and rate limits may be examples rather than enforced client controls.

Mitigation: Do not rely on those controls unless they are separately implemented and tested in the deployment environment.

Risk: Credentials may be exposed if API keys or URLs are stored in persistent shell startup files or agent configuration files.

Mitigation: Provide N8N_API_KEY and N8N_URL through a secret manager or short-lived process environment, and avoid storing secrets in bashrc or config files.

## Reference(s):

- [Security guide](references/security.md)
- [Setup validation script](scripts/validate-setup.sh)
- [n8n API documentation](https://docs.n8n.io/api/)
- [ClawHub skill page](https://clawhub.ai/nelmaz/skills/n8n-automation-secure)
- [Publisher profile](https://clawhub.ai/user/nelmaz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, YAML, JavaScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires N8N_URL and N8N_API_KEY environment variables; normal use should validate setup before API actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, artifact metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
