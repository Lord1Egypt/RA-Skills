## Description:

Use fpx through a signed-in Chrome tab to retrieve MyAtriumHealth MyChart data, including test results, medications, allergies, immunizations, health issues, visits, goals, and messages, in shell workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MyAtriumHealth users can retrieve their own portal data, including results, medications, allergies, visits, and messages, in shell workflows using a signed-in Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill suspicious because setup permits capturing portal session cookies, which the scanner considers unnecessary for the described workflow; it did not confirm that cookies are actually captured, and its analysis was partial.

Mitigation: Before installing, review and understand the declared cookie and header capture scope and whether it is needed; proceed only if you trust the skill and bridge. Keep retrieved health information private.

## Reference(s):

- [MyAtriumHealth endpoint recipes](references/endpoints.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/myatriumhealth-mcp)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [MyChart API responses, optionally projected into concise JSON or text with jq]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain personal health information.]

## Skill Version(s):

1.5.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
