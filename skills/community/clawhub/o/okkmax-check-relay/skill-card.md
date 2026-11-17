## Description:

Checks a specific AI API relay against OkkMax's measured data and reports only available purity, availability, latency, pricing, and review findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okkmx](https://clawhub.ai/user/okkmx)

### License/Terms of Use:

MIT-0

## Use Case:

Users evaluating a specific AI API relay can provide its name, slug, or website to review OkkMax's measured purity, availability, latency, pricing, and reviews. The skill summarizes only available measurements and their limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay name or website text submitted for lookup is shared with OkkMax.

Mitigation: Use a public relay name or clean website address and remove credentials, tokens, and private query parameters before lookup.

Risk: OkkMax measurements are dated observations and do not guarantee a relay's ongoing reliability.

Mitigation: Present findings with their data time and describe them as measurements, not guarantees.

## Reference(s):

- [OkkMax MCP server](https://www.okkmax.com/mcp)
- [OkkMax markdown data index](https://www.okkmax.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/okkmx/skills/okkmax-check-relay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response in the user's language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based relay summary with available measurements, source link, timestamp, and stated data limits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
