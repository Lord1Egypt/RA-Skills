## Description:

Conduct comprehensive, systematic literature reviews using multiple academic databases such as PubMed, arXiv, bioRxiv, and Semantic Scholar, then create professionally formatted markdown documents and PDFs with verified citations in multiple citation styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxr191202](https://clawhub.ai/user/yxr191202)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, analysts, and technical teams use this skill to plan, execute, synthesize, and document systematic literature reviews, scoping reviews, meta-analyses, and research summaries across biomedical, scientific, and technical domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad local file and command execution authority.

Mitigation: Use it in a dedicated workspace or container and install it only when local file and command execution authority is acceptable.

Risk: PDF generation includes a path that evidence.security identifies as unsafe before review.

Mitigation: Review PDF generation before installation, avoid untrusted filenames or documents, and pin dependencies.

Risk: English- and prestige-based review guidance may be mistaken for systematic-review policy.

Mitigation: Treat that guidance as optional and align review methods with the user's applicable systematic-review protocol.

## Reference(s):

- [Review Template](assets/review_template.md)
- [Citation Styles Reference](references/citation_styles.md)
- [Literature Database Search Strategies](references/database_strategies.md)
- [PRISMA](http://www.prisma-statement.org/)
- [Cochrane Handbook](https://training.cochrane.org/handbook)
- [AMSTAR 2](https://amstar.ca/)
- [MeSH Browser](https://meshb.nlm.nih.gov/search)
- [PubMed Advanced Search](https://pubmed.ncbi.nlm.nih.gov/advanced/)
- [APA Style](https://apastyle.apa.org/)
- [Nature Portfolio Reporting Standards](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards)
- [NLM/Vancouver Style](https://www.nlm.nih.gov/bsd/uniform_requirements.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown, JSON, BibTeX, and PDF files with inline shell commands and structured review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate literature search result summaries, citation verification reports, formatted references, markdown review documents, and PDFs when required dependencies are available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
