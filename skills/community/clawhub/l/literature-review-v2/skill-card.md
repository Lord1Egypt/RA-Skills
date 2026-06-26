## Description: <br>
Conducts comprehensive, systematic literature reviews across biomedical, scientific, and technical domains using multiple academic databases, citation verification, and markdown or PDF document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diekunstderfug](https://clawhub.ai/user/diekunstderfug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, students, and technical writers use this skill to plan, search, screen, synthesize, and format literature reviews, systematic reviews, scoping reviews, and meta-analyses. It helps document search strategies, deduplicate results, verify citations, and produce structured markdown or PDF review outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries external academic databases and citation services, which may expose confidential research plans, unpublished references, or sensitive search terms. <br>
Mitigation: Use non-sensitive queries when possible, avoid unpublished confidential materials, and confirm that third-party database and API exposure is acceptable before running searches. <br>
Risk: The scanner reported that the skill mandates an external AI schematic workflow that is under-scoped and references a missing helper script. <br>
Mitigation: Review the schematic requirement before use, confirm the expected scientific-schematics workflow is available, and do not rely on the missing helper command without separately validating it. <br>
Risk: PDF generation runs local pandoc and xelatex processing, which may fail or behave unexpectedly if dependencies or input markdown are not reviewed. <br>
Mitigation: Check dependencies with the provided script option, review generated commands and input markdown, and inspect PDF output before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diekunstderfug/literature-review-v2) <br>
- [Database search strategies](references/database_strategies.md) <br>
- [Citation styles reference](references/citation_styles.md) <br>
- [Review template](assets/review_template.md) <br>
- [PRISMA statement](http://www.prisma-statement.org/) <br>
- [Cochrane Handbook](https://training.cochrane.org/handbook) <br>
- [AMSTAR](https://amstar.ca/) <br>
- [PubMed Advanced Search Builder](https://pubmed.ncbi.nlm.nih.gov/advanced/) <br>
- [MeSH Browser](https://meshb.nlm.nih.gov/search) <br>
- [NLM Citing Medicine](https://www.ncbi.nlm.nih.gov/books/NBK3827/) <br>
- [APA Style](https://apastyle.apa.org/) <br>
- [Nature Portfolio reporting standards](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards) <br>
- [NLM uniform requirements](https://www.nlm.nih.gov/bsd/uniform_requirements.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, citation reports, JSON search result files, BibTeX-style entries, shell commands, and PDFs generated from markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query external academic databases and APIs; PDF generation depends on local pandoc and xelatex availability.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
