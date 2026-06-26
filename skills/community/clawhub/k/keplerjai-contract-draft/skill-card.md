## Description: <br>
基于 Word 模板和结构化业务信息生成合同草稿。适用于 AI 总助根据现有 .docx 模板起草合同、填充甲乙方与合作信息、识别缺失字段并输出可审阅草稿的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renjicode](https://clawhub.ai/user/renjicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to draft reviewable contract documents from existing Word templates and structured business terms. It helps prepare a JSON job spec, generate an editable .docx draft, identify unresolved fields, and produce run and validation summaries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may write contract artifacts and diagnostic summaries to disk and may save or reuse sensitive business-contract context more broadly than users expect. <br>
Mitigation: Use redacted inputs where possible, confirm where outputs and memory are stored before processing confidential agreements, review generated reports, and clean up generated files or saved memory that should not persist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renjicode/keplerjai-contract-draft) <br>
- [README](README.md) <br>
- [Generic Requirements](references/generic-requirements.md) <br>
- [Input Contracting Rules](references/input-contracting-rules.md) <br>
- [Runtime Output Contract](references/runtime-output-contract.md) <br>
- [Template Analysis](references/template-analysis.md) <br>
- [Word Plugin Setup](references/word-plugin-setup.md) <br>
- [Iteration Notes](references/iteration-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [JSON job specs, Markdown summaries, shell commands, editable .docx files, unresolved item lists, run summaries, and validation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft contract artifacts for business and legal review; generated documents should not be treated as final legal advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
