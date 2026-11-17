## Description:

Search and read Best Buy product, category, review, and store information through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve Best Buy product, category, review, and store information through their connected OOMOL account. The skill is intended for read-only Best Buy lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes a remote installer without a separate approval step, and the installer and hosted runtime were not verified.

Mitigation: Review and approve CLI installation separately, verify the installer or release, check which agent skills the CLI installs or updates, and disable synchronization if it is unwanted.

Risk: Best Buy queries and account authorization go through OOMOL and may use credit.

Mitigation: Review OOMOL account connection and billing requirements before use.

## Reference(s):

- [Best Buy](https://www.bestbuy.com)
- [Best Buy API documentation](https://bestbuyapis.github.io/api-documentation/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Natural language summaries based on structured Best Buy lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only product, category, review, and store information]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
