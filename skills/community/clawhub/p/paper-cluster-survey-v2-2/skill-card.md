## Description: <br>
Extract structured paper records from one or more local PDFs, arXiv links, DOI links, or general paper URLs, then classify the papers and write an academic survey review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huang888596](https://clawhub.ai/user/huang888596) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to turn mixed paper sources into structured records, defensible classifications, and an integrated literature review. It is suited to URL-first literature collection, PDF-based review drafting, taxonomy building, and formal academic survey preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read supplied PDFs or local paths and fetch paper URLs, which may expose confidential documents or private-network resources if the user provides them. <br>
Mitigation: Use only intended public or approved research sources, avoid confidential files and localhost/private-network URLs, and review the source list before extraction. <br>
Risk: Extracted metadata and generated survey claims may be incomplete or inaccurate when source text is weak, missing, or recovered through fallback methods. <br>
Mitigation: Check important claims, classifications, and citations against the original papers, especially when extraction notes indicate low-confidence methods. <br>


## Reference(s): <br>
- [Extraction Pipeline](references/extraction-pipeline.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Review Paper Style](references/review-paper-style.md) <br>
- [Taxonomy Guidelines](references/taxonomy-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, and command-line examples for generated literature review workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write requested manifest, paper-record, and review files; default review output includes corpus summary, classification scheme, classification table, formal review article, and references.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
