## Description:

Build Instacart recipe pages, shopping lists, and retailer lookups with MCP, REST, secure auth, and launch-ready integration rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and integration teams use this skill to choose the correct Instacart integration surface and build recipe pages, shopping-list pages, nearby retailer lookups, MCP handoffs, troubleshooting flows, and launch-readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instacart requests can send recipe, shopping-list, retailer lookup, and MCP payload data to Instacart services.

Mitigation: Use the skill only for intended Instacart workflows, confirm the chosen surface before sending traffic, and avoid undeclared external destinations.

Risk: The required INSTACART_API_KEY could be exposed if pasted into chat, markdown, screenshots, repository files, or local notes.

Mitigation: Keep the key in environment variables or a secret manager and keep raw secrets out of ~/instacart/ memory files.

Risk: Production page creation or public messaging can fail when approval, key status, or brand guidance has not been confirmed.

Mitigation: Use development first, confirm production approval and key permissions, and review launch messaging before public release.

Risk: Malformed request payloads can produce validation errors or weak product matches.

Mitigation: Validate units, quantities, identifiers, filters, geography, and retailer context locally before retrying API calls.

## Reference(s):

- [ClawHub Instacart Skill](https://clawhub.ai/ivangdavila/skills/instacart)
- [Instacart Skill Definition](artifact/SKILL.md)
- [Auth Playbook](artifact/auth-playbook.md)
- [Endpoint Map](artifact/endpoint-map.md)
- [Request Patterns](artifact/request-patterns.md)
- [MCP Integration](artifact/mcp-integration.md)
- [Connect Boundaries](artifact/connect-boundaries.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INSTACART_API_KEY for live Instacart requests and jq for documented smoke-test examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
