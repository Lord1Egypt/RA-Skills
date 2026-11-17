## Description:

SMS verification and virtual phone numbers via Grizzly SMS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grizzlysms-git](https://clawhub.ai/user/grizzlysms-git)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Grizzly SMS for balance checks, virtual phone number rentals, SMS verification-code retrieval, activation management, and setup guidance for OpenClaw or MCP clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be collected in chat or exposed through loosely configured agent environments.

Mitigation: Prefer protected configuration or secret storage for GRIZZLY_SMS_API_KEY and avoid pasting long-lived credentials into chat when a secure configuration path is available.

Risk: The skill can rent phone numbers, retrieve verification codes, and support automated third-party account signups.

Mitigation: Install and enable it only for intended SMS-verification workflows, review account-registration use against applicable service terms, and keep browser automation disabled unless it is explicitly needed.

Risk: Broad exec permissions could allow commands beyond the intended Grizzly SMS CLI flow.

Mitigation: Restrict exec permissions to the documented grizzly-cli.mjs commands and avoid full exec configurations with approval disabled.

Risk: Exposing the MCP HTTP port without authentication could make Grizzly SMS actions available to unintended callers.

Mitigation: Do not expose the MCP HTTP port publicly unless access control and authentication are in place.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/grizzlysms-git/skills/grizzly-sms-mcp)
- [Grizzly SMS documentation](https://grizzlysms.com/docs)
- [Grizzly SMS service](https://grizzlysms.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON snippets, and copy-friendly values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include phone numbers, activation IDs, SMS codes, account balance text, service and country listings, and setup configuration snippets.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
