## Description: <br>
Write 40-100+ page academic reports such as FYPs, theses, and dissertations with a 3-wave parallel agent pipeline that extracts data from a research repository, writes chapters in parallel, and compiles LaTeX with cross-reference auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, and developers use this skill to turn a research repository with code and experiment results into a long-form LaTeX academic report. It supports data preparation, chapter drafting, figure planning, citation verification, cross-reference auditing, and compilation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation checking sends bibliography metadata such as titles and DOIs to CrossRef, Semantic Scholar, and OpenAlex. <br>
Mitigation: Do not run citation checking on embargoed, unpublished, or sensitive bibliographies unless sharing that metadata with public academic APIs is acceptable. <br>
Risk: The skill analyzes the chosen research repository and can surface confidential logs, data, or experiment details during report generation. <br>
Mitigation: Remove secrets, confidential logs, and sensitive files before using the skill on a repository. <br>
Risk: Generated academic reports can contain incorrect claims, citations, figures, or cross-references if source data is incomplete or unreviewed. <br>
Mitigation: Validate source artifacts, run citation_checker.py and cross_ref_audit.py, compile the LaTeX output, and manually review the report before submission. <br>


## Reference(s): <br>
- [Phy Write Academic Report on ClawHub](https://clawhub.ai/PHY041/phy-write-academic-report) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [Citation Verification Workflow](references/citation-workflow.md) <br>
- [LaTeX Compilation Reference](references/compilation-guide.md) <br>
- [Parallel Agent Pipeline Reference](references/parallel-pipeline.md) <br>
- [Writing Guide: Thesis-Length Academic Documents](references/writing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with LaTeX, BibTeX, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local LaTeX compilation, cross-reference audits, and citation checks against public academic APIs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
