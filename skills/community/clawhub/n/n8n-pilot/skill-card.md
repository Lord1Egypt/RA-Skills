## Description:

Design, build, deploy, test, and secure advanced n8n workflows with architecture patterns, flow logic, dangerous pattern detection, self-hosting, credential management, and workflow recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, build, deploy, test, and secure n8n workflow automations, including webhook flows, credential setup, self-hosting patterns, and production safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community-node installation can run third-party npm code inside the n8n container.

Mitigation: Install only trusted, pinned, reviewed packages in staging before promoting them to production.

Risk: n8n API and encryption keys protect workflow access and stored credentials.

Mitigation: Store N8N_API_KEY and N8N_ENCRYPTION_KEY in a secret manager or protected environment, avoid plaintext secret backups, and verify backups include the encryption key.

Risk: Automated workflows can perform destructive email or business-data actions.

Mitigation: Prefer quarantine or labels over automatic deletion, require explicit confirmation for destructive changes, and test workflows inactive before activation.

Risk: Unauthenticated or unvalidated webhooks can be triggered externally.

Mitigation: Use header, basic, or JWT authentication, validate inputs at the first workflow node, and rate limit public endpoints.

## Reference(s):

- [n8n built-in integrations documentation](https://docs.n8n.io/integrations/builtin/)
- [ClawHub skill page](https://clawhub.ai/wahajahmed010/skills/n8n-pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, JavaScript, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires N8N_API_KEY and N8N_BASE_URL for API-driven workflows; some OAuth2 credential setup requires browser interaction.]

## Skill Version(s):

0.1.0 (source: frontmatter, artifact/_meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
