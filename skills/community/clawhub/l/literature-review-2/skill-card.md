## Description: <br>
Conduct comprehensive, systematic literature reviews using multiple academic databases, then produce professionally formatted Markdown documents and PDFs with verified citations in styles such as APA, Nature, and Vancouver. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxr191202](https://clawhub.ai/user/yxr191202) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, students, and technical writers use this skill to plan, search, screen, synthesize, and document systematic, scoping, narrative, or meta-analysis literature reviews across biomedical, scientific, and technical domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that this skill can contact external DOI and CrossRef services during citation verification. <br>
Mitigation: Use it only when sending citation metadata to those services is acceptable, and disable or manually approve citation-verification steps for confidential, unpublished, or regulated research. <br>
Risk: The security review reports that the skill forces an external AI schematic workflow for figures. <br>
Mitigation: Review and approve any external figure-generation step before use, especially when source material contains sensitive research details. <br>
Risk: The security review verdict is suspicious because external services are used without clear per-use consent in the artifact behavior. <br>
Mitigation: Run the skill in an environment where outbound calls and generated files can be reviewed, and require operator approval before networked citation or figure-generation steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxr191202/literature-review-2) <br>
- [Literature Database Search Strategies](references/database_strategies.md) <br>
- [Citation Styles Reference](references/citation_styles.md) <br>
- [Literature Review Template](assets/review_template.md) <br>
- [PRISMA](http://www.prisma-statement.org/) <br>
- [Cochrane Handbook](https://training.cochrane.org/handbook) <br>
- [AMSTAR 2](https://amstar.ca/) <br>
- [MeSH Browser](https://meshb.nlm.nih.gov/search) <br>
- [PubMed Advanced Search](https://pubmed.ncbi.nlm.nih.gov/advanced/) <br>
- [NLM Boolean Search Guide](https://www.ncbi.nlm.nih.gov/books/NBK3827/) <br>
- [APA Style](https://apastyle.apa.org/) <br>
- [Nature Portfolio Reporting Standards](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards) <br>
- [NLM/Vancouver](https://www.nlm.nih.gov/bsd/uniform_requirements.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown review documents, PDF files, citation verification reports, search result summaries, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local scripts for citation verification, search-result processing, and PDF generation; generated reviews should be checked for citation accuracy and methodological fit before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
