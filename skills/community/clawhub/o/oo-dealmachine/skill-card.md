## Description:

Provides DealMachine search and read actions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search DealMachine property data, inspect account and field information, and retrieve selected property details through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified installer code with broad effects on the agent environment; the remote installers and hosted connector were not verified.

Mitigation: Review and install a verified CLI release manually before use, rather than allowing automatic installer execution.

Risk: Searches and enrichment may consume credits.

Mitigation: Use the credit-free count action or estimate search cost before requesting results, and consider the cost before enrichment.

## Reference(s):

- [DealMachine Homepage](https://dealmachine.com)
- [DealMachine API Documentation](https://api.docs.dealmachine.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data, API Calls, Guidance]

**Output Format:** [DealMachine action results as JSON, with natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the requested read action; searches or enrichment may consume credits.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
