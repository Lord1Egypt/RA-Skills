## Description:

Publishes GEO-optimized, AI-citable news, changelogs, and announcements to the public Manto news network and helps agents verify whether published items are indexed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tans](https://clawhub.ai/user/tans)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to format factual, citable announcements and publish them to Manto through HTTP, CLI, or MCP workflows. They can also search, inspect account status, delete their own content, and configure client integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published content becomes public on Manto and may be indexed or cited by other agents.

Mitigation: Use the skill only for content intended for public release and verify factual claims before publishing.

Risk: A Manto API key can authorize publishing, account access, deletion, and promotion-budget actions.

Mitigation: Store the API key securely, avoid committing it to files or logs, and require human confirmation before destructive or spending-related actions.

Risk: Changing MANTO_BASE_URL can redirect credentials and submitted content away from the production Manto service.

Mitigation: Keep MANTO_BASE_URL unset except when testing with non-production credentials.

## Reference(s):

- [Manto homepage](https://manto.xin)
- [Manto MCP endpoint](https://manto.xin/mcp)
- [Server-resolved GitHub source](https://github.com/tans/manto/tree/main/skills/manto-geo)
- [GitHub repository](https://github.com/tans/manto)
- [ClawHub skill page](https://clawhub.ai/tans/skills/manto-geo)
- [Manto API reference](references/api.md)
- [Manto client integrations](references/clients.md)
- [GEO writing guide](references/geo-writing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, shell, TOML, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public Manto endpoints and credential-protected publishing, deletion, account, and promotion endpoints when configured with a Manto API key.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
