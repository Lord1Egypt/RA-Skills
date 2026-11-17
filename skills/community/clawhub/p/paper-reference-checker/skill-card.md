## Description:

This skill helps agents verify academic references against Google Scholar, CNKI, arXiv, DOI resolvers, and other academic databases to detect fabricated, broken, uncertain, or unverifiable citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benchen4395](https://clawhub.ai/user/benchen4395)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, editors, and academic reviewers use this skill to extract and verify references from PDFs, arXiv pages, Overleaf projects, BibTeX files, or pasted bibliographies. It helps identify citations that are verified, uncertain, not found, fabricated, or broken.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Citation titles, DOIs, arXiv IDs, or bibliography details may be sent to external academic search services during verification.

Mitigation: Avoid using the skill on confidential manuscripts unless those external lookups are acceptable for the user's use case.

Risk: Academic database searches can produce partial matches or missing results that lead to uncertain citation judgments.

Mitigation: Use DOI and arXiv identifiers first, cross-check multiple databases when needed, and preserve UNCERTAIN status when evidence is incomplete.

## Reference(s):

- [Citation Extraction and Parsing Rules](references/citation-extraction.md)
- [Database Query Strategies](references/search-strategies.md)
- [Authenticity Judgment Criteria](references/verification-criteria.md)
- [Reference Extraction Decision Tree](scripts/extract_references.md)
- [Sample Citation Verification Report](examples/sample-report.md)
- [BibTeX Example](examples/bibtex-example.bib)
- [DOI Resolver](https://doi.org/{DOI})
- [arXiv Abstract Lookup](https://arxiv.org/abs/{ID})
- [ClawHub Skill Page](https://clawhub.ai/benchen4395/skills/paper-reference-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown citation verification report with status labels and supporting lookup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include citation status categories such as VERIFIED, UNCERTAIN, NOT FOUND, FABRICATED, and BROKEN CITATION.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
