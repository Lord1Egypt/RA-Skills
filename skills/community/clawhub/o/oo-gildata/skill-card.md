## Description:

Search and read Gildata Data Map data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to search, read, and analyze financial data in Gildata Data Map, including company information, securities, funds, and market indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When the oo CLI is missing, setup instructions run a remote installer, creating a risk of uncontrolled software installation.

Mitigation: Review and explicitly approve CLI installation separately. Prefer a verified, pinned release and check whether it installs additional agent skills.

Risk: Using the connector entrusts OOMOL with access to the connected Gildata account.

Mitigation: Review the connected account and the access granted to OOMOL before using the connector.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Gildata Data Map](https://www.gildata.com/products/datamap)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Structured financial data and natural-language findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by requested data, comparison, or screening task.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
