## Description:

Search and read VTEX catalog data, including products, brands, categories, and product/SKU IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce operators use this skill to retrieve catalog and storefront data from a VTEX store connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute changing remote code without a clear user checkpoint, and remote installer behavior is unverified.

Mitigation: Review and install a verified CLI release before enabling the skill; require approval for later installation changes and review or disable automatic skill synchronization.

Risk: The integration uses the connected OOMOL account and VTEX connection.

Mitigation: Confirm the intended OOMOL account and VTEX connection before use.

## Reference(s):

- [VTEX API documentation](https://developers.vtex.com/docs/api-reference)
- [VTEX](https://vtex.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON data returned from VTEX product, brand, category, and storefront search reads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only catalog data; query fields depend on the selected VTEX action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
