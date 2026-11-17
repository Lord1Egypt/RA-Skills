## Description:

Search Facebook Marketplace listings near a specified location with filters for radius, price range, limit, and pickup-only through a user-provided Marketplace-compatible service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexanderhe88](https://clawhub.ai/user/alexanderhe88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query a trusted local or configured Marketplace-compatible service and receive normalized listing results for nearby Facebook Marketplace searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Marketplace-compatible service receives the user's query, location, and filters.

Mitigation: Keep MARKETPLACE_API_BASE_URL pointed at a local service or a trusted HTTPS endpoint.

Risk: Dependencies are not pinned in the artifact requirements.

Mitigation: Install in a virtual environment and pin dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexanderhe88/skills/marketplace-local-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns query, location, count, and normalized listing fields when the configured service responds successfully.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
