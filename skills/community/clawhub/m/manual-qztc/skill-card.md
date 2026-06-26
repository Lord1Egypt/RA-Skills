## Description: <br>
仅供QZTC内部使用。教学工作手册生成工具 v5.3。Generator+Reviewer双模式，支持Pipeline一键生成+审查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alukardo](https://clawhub.ai/user/alukardo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QZTC teaching staff use this skill to generate teaching work manuals from course spreadsheets and review the resulting Word documents for placeholder replacement and table structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local student and course spreadsheets and writes generated docx files beside input spreadsheets. <br>
Mitigation: Use trusted Excel and template paths, keep student data in approved local storage, and review generated documents before sharing. <br>
Risk: Template directory settings can change which Word templates are used for generation. <br>
Mitigation: Review the optional config.env template directory setting and point it only to trusted QZTC templates. <br>


## Reference(s): <br>
- [Teaching Work Manual Generation Rules](references/grading-formula.md) <br>
- [ClawHub skill page](https://clawhub.ai/alukardo/manual-qztc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts are Word documents and review reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Excel spreadsheets and Word templates; pipeline mode can generate and then review a document.] <br>

## Skill Version(s): <br>
5.3.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
