## Description:

VATlayer (vatlayer.com). Use this skill for ANY VATlayer request — searching and reading data. Whenever a task involves VATlayer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve VAT rates, calculate VAT inclusive or exclusive prices, list reduced rate types, and validate VAT numbers through their connected VATlayer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions direct users to run remote CLI installers without integrity checks or a separate approval step.

Mitigation: Install a verified CLI release yourself and require approval before any downloaded installer runs.

Risk: OOMOL brokers VATlayer requests and manages the connected credential.

Mitigation: Review whether you trust OOMOL to handle the connection and its credential.

## Reference(s):

- [VATlayer](https://vatlayer.com)
- [VATlayer API documentation](https://docs.apilayer.com/vatlayer/docs/api-documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [VATlayer ClawHub release](https://clawhub.ai/oomol/skills/oo-vatlayer)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text or JSON results from VAT lookup, validation, and price calculation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected VATlayer action and the connected account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
