## Description:

Conducts comprehensive, systematic literature reviews using multiple academic databases, citation verification, structured synthesis, and professional markdown or PDF output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diekunstderfug](https://clawhub.ai/user/diekunstderfug)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and developers use this skill to plan, search, screen, synthesize, verify, and format literature reviews, systematic reviews, scoping reviews, and meta-analyses across scientific and technical domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature search queries and citation identifiers may be sent to public academic metadata services.

Mitigation: Avoid confidential or sensitive queries unless disclosure is acceptable, and review service terms before use.

Risk: Dependency and document-generation behavior may vary across local environments.

Mitigation: Run the skill in a virtual environment, pin dependencies where possible, and confirm required tools such as pandoc and xelatex before producing PDFs.

Risk: PDF generation on untrusted markdown or bibliography files can expose users to unsafe document-processing inputs.

Mitigation: Generate PDFs only from trusted review sources and inspect markdown, bibliography, and template inputs before running local document-generation tools.

Risk: The AI-schematic requirement depends on a separate skill or provider that may not be installed or trusted.

Mitigation: Treat schematic generation as optional unless that separate skill and provider have been installed, reviewed, and approved.

Risk: Literature synthesis can become misleading if searches are narrow, citations are stale, or study quality is not assessed.

Mitigation: Use multiple databases, document search dates and criteria, verify citations, and apply appropriate quality-assessment methods before relying on conclusions.

## Reference(s):

- [Citation Styles Reference](references/citation_styles.md)
- [Literature Database Search Strategies](references/database_strategies.md)
- [Literature Review Template](assets/review_template.md)
- [PRISMA Statement](http://www.prisma-statement.org/)
- [Cochrane Handbook](https://training.cochrane.org/handbook)
- [AMSTAR 2](https://amstar.ca/)
- [MeSH Browser](https://meshb.nlm.nih.gov/search)
- [PubMed Advanced Search](https://pubmed.ncbi.nlm.nih.gov/advanced/)
- [Boolean Search Guide](https://www.ncbi.nlm.nih.gov/books/NBK3827/)
- [APA Style](https://apastyle.apa.org/)
- [Nature Portfolio Reporting Standards](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards)
- [NLM/Vancouver Style](https://www.nlm.nih.gov/bsd/uniform_requirements.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON search and citation reports, BibTeX entries, and generated markdown or PDF review files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Citation verification and PDF generation can depend on public academic metadata services and local document-generation tools.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
