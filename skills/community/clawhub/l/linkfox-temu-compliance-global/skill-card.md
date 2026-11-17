## Description:

Provides agent guidance and scripts for Temu Global product-compliance workflows through LinkFox-forwarded Partner Global OpenAPI endpoints, including compliance metadata, compliance labels, certification requirements, real-image upload, qualification upload, and compliance edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce operators use this skill to call LinkFox-mediated Temu Global compliance APIs for product compliance metadata, labels, certification requirements, certificate upload, real-image upload, and compliance updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox and Temu commerce credentials, including locally stored Temu access tokens.

Mitigation: Install only in trusted environments, use dedicated least-privilege Temu tokens, and keep token-store files out of logs and shared workspaces.

Risk: Full API responses may be persisted locally and can contain commerce or compliance data.

Mitigation: Review generated files under linkfox session data directories before sharing the workspace or command output.

Risk: Gateway endpoint override environment variables can redirect requests away from the default LinkFox gateway.

Mitigation: Use custom gateway environment variables only when you control and trust the endpoint.

Risk: The skill can initiate user-directed commerce compliance workflows through external APIs.

Mitigation: Review parameters and expected cost or account impact before executing scripts against production stores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-compliance-global)
- [API reference](references/api.md)
- [Partner Global Compliance interface catalog](references/partner-global-catalog.md)
- [Compliance API documentation index](references/apis/README.md)
- [Access token authorization guide](references/access-token.md)
- [Onboarding and authentication recovery](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large API responses may be summarized in stdout while full JSON responses are persisted under linkfox session data directories.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
