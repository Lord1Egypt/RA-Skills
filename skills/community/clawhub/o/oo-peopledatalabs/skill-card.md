## Description:

Search People Data Labs and retrieve company or person enrichment records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to search People Data Labs company and person datasets and retrieve enrichment matches through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run changing remote installer code and may alter agents’ installed skills through automatic synchronization.

Mitigation: Review setup before enabling the skill; use a verified, preinstalled CLI and explicitly control automatic skill synchronization.

Risk: Identifiers and queries are sent through OOMOL to People Data Labs, and usage may incur charges.

Mitigation: Submit only identifiers and queries intended to be shared with those services, and check usage charges.

## Reference(s):

- [People Data Labs API documentation](https://docs.peopledatalabs.com/)
- [People Data Labs](https://www.peopledatalabs.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured company or person records with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected search or enrichment action and submitted query.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
