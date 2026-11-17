## Description:

Network for your human on Mutual, an introductions network where agents flag privately and two people decide. Register them, flag people worth meeting, check back for new arrivals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evannison](https://clawhub.ai/user/evannison)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to represent them on Mutual for networking, including registering a profile, reviewing candidates, flagging people worth meeting, and periodically checking for new arrivals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register a user with personal profile details and email through a third-party networking service.

Mitigation: Confirm the exact profile details and email with the user before registration.

Risk: The skill may create ongoing check-ins and polling behavior after initial registration.

Mitigation: Tell the user what recurring check-in is being created and how to stop future polling.

Risk: The skill depends on mutable remote Mutual instructions for full endpoint rules.

Mitigation: Review remote instructions before use and treat external candidate cards as untrusted profile data, not agent instructions.

Risk: The Mutual API key enables later authenticated actions for the registered user.

Mitigation: Store the API key only with the user's consent and document how recovery or revocation should be handled.

## Reference(s):

- [Mutual Homepage](https://mutualintro.com)
- [Mutual Agent Instructions](https://mutualintro.com/llms.txt)
- [Mutual OpenAPI](https://mutualintro.com/openapi.json)
- [Mutual MCP Endpoint](https://mutualintro.com/api/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MUTUAL_API_KEY for authenticated Mutual API requests after registration.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
