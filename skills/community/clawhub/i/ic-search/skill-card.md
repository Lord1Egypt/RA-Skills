## Description:

Searches electronic component prices, inventory, quotes, and spot purchase availability through the documented IC Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wordgao](https://clawhub.ai/user/wordgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sourcing teams, and procurement agents use this skill to query electronic component part numbers, quantities, brands, pricing, inventory, and spot availability from a supplier API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms can include component part numbers, quantities, brands, and sourcing intent sent to a third-party API over plaintext HTTP.

Mitigation: Avoid confidential BOMs, sensitive procurement plans, or private demand signals unless the service is moved to HTTPS and data handling is approved.

Risk: The skill has broad auto-trigger rules for inventory, quote, purchase, spot-stock, and PCS-related requests.

Mitigation: Confirm user intent before sending ambiguous or sensitive procurement queries to the external service.

Risk: The documented request uses a fixed supply token in the URL query string.

Mitigation: Treat the token and generated request URLs as sensitive operational data and avoid logging or sharing them unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wordgao/skills/ic-search)
- [IC Search API documentation](references/api.md)
- [IC Search usage examples](references/examples.md)
- [IC Search error codes](references/errors.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and plain-text supplier search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the API data field to the user; examples include curl commands and fixed supply parameter usage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
