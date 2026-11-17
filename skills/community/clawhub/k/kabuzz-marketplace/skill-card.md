## Description:

AI-native resale marketplace for browsing, listing, buying, selling, negotiating, messaging, and managing orders through 49 MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douglashardman](https://clawhub.ai/user/douglashardman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to the Kabuzz resale marketplace for product discovery, listings, purchases, negotiations, messaging, shipping, orders, payment-method management, and onboarding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unpinned external code through npx.

Mitigation: Use a pinned, verified version of the Kabuzz MCP server before deployment.

Risk: The skill uses a financial API key and can perform off-session marketplace purchases.

Mitigation: Use a narrowly scoped, revocable API key with conservative spending limits and require human confirmation for purchases.

Risk: The skill includes payment-method management capabilities.

Mitigation: Require human confirmation for payment changes and monitor account activity after installation.

## Reference(s):

- [Kabuzz Marketplace](https://kabuzz.com)
- [Kabuzz API Docs](https://kabuzz.com/docs)
- [Kabuzz MCP Server on npm](https://www.npmjs.com/package/@kabuzz/mcp-server)
- [Kabuzz Agent Skill File](https://kabuzz.com/agent-skill.md)
- [Kabuzz llms.txt](https://kabuzz.com/llms.txt)
- [Kabuzz OpenAPI Spec](https://kabuzz.com/docs-json)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, API calls]

**Output Format:** [Markdown instructions with JSON configuration examples and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and a KABUZZ_API_KEY environment variable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
