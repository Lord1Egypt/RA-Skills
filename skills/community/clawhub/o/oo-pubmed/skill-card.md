## Description:

Search PubMed and retrieve article data through the PubMed connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use the skill to search PubMed, retrieve normalized article records, match citations, and explore related or citing articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run downloaded software whose full effects are unverified.

Mitigation: Verify and install the oo CLI yourself before enabling the skill, and prevent automatic execution of its installer fallback.

Risk: The CLI can install additional agent skills, and PubMed requests pass through OOMOL and may use credits.

Mitigation: Review the CLI's installation of additional agent skills and understand that PubMed requests pass through OOMOL and may use credits.

## Reference(s):

- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [NCBI API documentation](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON responses containing normalized PubMed article data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
