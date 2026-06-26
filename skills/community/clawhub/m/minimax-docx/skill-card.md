## Description: <br>
Minimax Docx creates validated Word .docx files with professional formatting, visual hierarchy, and cross-application compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrisLiu16](https://clawhub.ai/user/KrisLiu16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-production agents use this skill to create new Word documents or apply user-provided templates, then validate formatting, schema health, residual placeholders, and cross-application compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ordinary commands can automatically download and run .NET installer scripts and modify the user's home-level .NET installation. <br>
Mitigation: Install .NET 9 manually before using the skill, and avoid running doctor, render, audit, or map-apply on systems where ~/.dotnet contains important existing runtimes. <br>
Risk: Generated filler content or template edits may be unsuitable for reliance without review. <br>
Mitigation: Review generated document content, template replacements, audit output, and residual-placeholder checks before relying on or distributing the document. <br>


## Reference(s): <br>
- [Minimax Docx ClawHub page](https://clawhub.ai/KrisLiu16/minimax-docx) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Create workflow guide](artifact/guides/create-workflow.md) <br>
- [Template-apply workflow guide](artifact/guides/template-apply-workflow.md) <br>
- [DOC input normalization protocol](artifact/guides/doc-input-normalization.md) <br>
- [C# OpenXML coding guide](artifact/guides/development.md) <br>
- [Troubleshooting guide](artifact/guides/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [DOCX files with validation output, Markdown guidance, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated documents are expected to pass audit checks, schema validation, and residual-placeholder checks before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
