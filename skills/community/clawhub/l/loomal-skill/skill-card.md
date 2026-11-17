## Description:

Loomal capabilities: agent inbox at mailgent.dev, encrypted credential vault with 2FA, calendar, and USDC payments, with actions user-directed and scope-gated by a Loomal API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masteratwork](https://clawhub.ai/user/masteratwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent work with Loomal-provided mail, credential vault, calendar, identity signing, and USDC payment workflows under the scopes granted to the user's Loomal API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Loomal API key can delegate access to sensitive mail, vault, calendar, signing, and payment capabilities depending on granted scopes.

Mitigation: Use narrow per-task API keys, avoid combining broad scopes unless needed, and rotate keys when a task ends or a key is no longer needed.

Risk: Public calendar sharing and USDC payment actions can expose information or move real value.

Mitigation: Require explicit user confirmation for public calendar changes and payment redemption, including amount, destination, and visibility impact.

Risk: Installing the skill relies on trust in Loomal and the @loomal/mcp package used by the MCP server.

Mitigation: Install only when the user trusts Loomal and the package source, and keep the MCP package version pinned or updated intentionally.

## Reference(s):

- [Loomal homepage](https://loomal.ai)
- [Loomal documentation](https://docs.loomal.ai)
- [Loomal OpenClaw integration documentation](https://docs.loomal.ai/integrations/openclaw)
- [Loomal API reference](https://docs.loomal.ai/api-reference)
- [@loomal/mcp npm package](https://www.npmjs.com/package/@loomal/mcp)
- [ClawHub skill page](https://clawhub.ai/masteratwork/skills/loomal-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and tool-selection instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOOMAL_API_KEY; available actions depend on the scopes granted to that key.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
