## Description:

Search and read data from the WHO Global Health Observatory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search WHO Global Health Observatory indicators and retrieve observations filtered by dimensions and year.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can execute downloaded code without a clear approval step.

Mitigation: Require approval for local changes and use a reviewed, version-pinned CLI distribution with verified integrity; check which additional agent skills the CLI installs.

Risk: WHO queries through OOMOL may incur charges.

Mitigation: Check applicable OOMOL charges before running queries.

## Reference(s):

- [WHO Global Health Observatory](https://www.who.int/data/gho)
- [WHO GHO OData API documentation](https://www.who.int/data/gho/info/gho-odata-api)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected indicator, dimensions, and years.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
