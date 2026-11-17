## Description:

Access historical OpenMandate mandates and matches or close retained work for an existing account while OpenMandate is in private development and unavailable for new mandates or integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsh3khar](https://clawhub.ai/user/rsh3khar)

### License/Terms of Use:

MIT-0

## Use Case:

External users with existing OpenMandate accounts use this skill to access retained mandates, matches, and contacts and to perform withdrawal actions such as closing mandates, declining matches, and deleting contacts after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform consequential account actions, including closing mandates, declining matches, and deleting contacts.

Mitigation: Require explicit human confirmation of the exact target before executing withdrawal actions.

Risk: The API bearer key may be sent to an arbitrary configured base URL.

Mitigation: Use the default OpenMandate API endpoint unless OPENMANDATE_BASE_URL is fully trusted.

Risk: OpenMandate is in private development and is not accepting new mandates, integrations, accounts, or API keys.

Mitigation: Limit use to retained access for existing accounts and do not direct users to create or reactivate work.

## Reference(s):

- [OpenMandate retained-access API reference](references/api-reference.md)
- [OpenMandate homepage](https://openmandate.ai)
- [OpenMandate hosted MCP endpoint](https://mcp.openmandate.ai/mcp)
- [OpenMandate API base URL](https://api.openmandate.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON API responses]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENMANDATE_API_KEY; OPENMANDATE_BASE_URL is optional and should only point to a trusted endpoint.]

## Skill Version(s):

0.6.2 (source: server release evidence, SKILL.md metadata, and helper script)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
