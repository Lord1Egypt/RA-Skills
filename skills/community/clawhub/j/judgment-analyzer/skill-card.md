## Description: <br>
Analyzes judgment documents, extracts key case information, and generates structured analysis reports for single PDF or Word files and folders of cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzzcode](https://clawhub.ai/user/szzzcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, compliance, and research users use this skill to extract text from local judgment PDFs or Word documents and turn the content into structured case summaries or batch comparison reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted text and generated summaries may contain sensitive legal or personal information. <br>
Mitigation: Process only judgment files intended for analysis, keep the generated 摘要 folder in an appropriate protected location, and delete it when no longer needed. <br>
Risk: Untrusted PDF or Word files and unpinned parsing dependencies can introduce document-processing risk. <br>
Mitigation: Install dependencies in a virtual environment and consider pinning or auditing dependency versions before processing untrusted files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/szzzcode/judgment-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/szzzcode) <br>
- [Project Homepage](https://github.com/szzzcode/judgment-analyzer) <br>
- [Output Template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text extraction files and Markdown analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an 摘要 folder with extracted .txt files, per-case summaries, and for batch runs a 综合分析报告.md file.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
