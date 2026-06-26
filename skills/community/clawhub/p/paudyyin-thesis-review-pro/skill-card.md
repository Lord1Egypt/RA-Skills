## Description: <br>
高校硕士/博士学位论文智能评审技能，基于13篇真实论文评审经验总结的结构化评审框架，支持学硕、专硕和博士论文评审，并生成Word格式评审意见。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic reviewers, thesis supervisors, and graduate program staff use this skill to extract thesis information, assess methodology, experiments, writing quality, and novelty, and produce structured review feedback for master’s or doctoral theses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Thesis PDFs and generated review files may contain confidential student, institutional, or unpublished research information. <br>
Mitigation: Use the skill only in environments authorized to process thesis material and store generated review files in access-controlled locations. <br>
Risk: Search queries based on thesis details may expose identifying or unpublished research information. <br>
Mitigation: Avoid web searches with identifying or novel unpublished details unless the reviewer has explicit authorization. <br>
Risk: The skill reads thesis files and may generate Word review artifacts. <br>
Mitigation: Confirm which files will be read before use and review generated outputs before sharing or archiving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/paudyyin-thesis-review-pro) <br>
- [Publisher profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review content with optional Python examples for PDF extraction and Word document generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured thesis review sections, reviewer questions, revision recommendations, batch comparison summaries, and .docx generation guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
