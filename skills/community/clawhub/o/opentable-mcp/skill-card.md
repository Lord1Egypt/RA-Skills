## Description:

Manage OpenTable reservations via MCP: search restaurants, check slot availability, book tables, list or cancel reservations, and manage favorites while using a signed-in OpenTable browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to connect an agent to OpenTable reservation workflows through an MCP server. It helps search restaurants, inspect availability, preview booking policies, book or modify reservations, cancel upcoming reservations, and manage saved restaurants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server and browser extension operate through a signed-in OpenTable session and can access reservation and profile data.

Mitigation: Use a dedicated browser profile where possible and install only after verifying the package, extension publisher, and version.

Risk: Booking, modification, cancellation, and favorites tools can make real account changes.

Mitigation: Require explicit user confirmation before committing booking, modification, cancellation, or favorites changes.

Risk: Some reservations may include cancellation policies or payment-card holds.

Mitigation: Run booking or modification preview first when required and surface cancellation policy and payment details before asking the user to confirm.

## Reference(s):

- [OpenTable MCP package](https://www.npmjs.com/package/opentable-mcp)
- [OpenTable MCP source](https://github.com/chrischall/opentable-mcp)
- [fetchproxy extension](https://github.com/chrischall/fetchproxy)
- [OpenTable](https://www.opentable.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, MCP tool calls, markdown]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and MCP tool-call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the opentable-mcp package, the fetchproxy browser extension, and a signed-in OpenTable browser tab.]

## Skill Version(s):

0.15.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
