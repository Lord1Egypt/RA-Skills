## Description: <br>
Create or update Nika platform skills with main documents and sub-documents that follow Nika constraints, including two-level structure, sub-document references, and no path or extension references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[typewrong](https://clawhub.ai/user/typewrong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create, refactor, or validate Nika platform skill drafts. It helps produce repository files and copyable Nika main-document and sub-document content with explicit input, output, and validation contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The initializer writes files into a local repository and can replace existing files when --force is used. <br>
Mitigation: Run scripts only in the intended repository and use --force only when existing files are meant to be replaced. <br>
Risk: Generated Nika skill documents may contain incomplete placeholders or unsuitable workflow assumptions. <br>
Mitigation: Review generated documents and run the included validator before using or publishing the target skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/typewrong/nika-skill-creator) <br>
- [Nika Skill constraints](references/nika-spec.md) <br>
- [Main document template](references/main-doc-template.md) <br>
- [Sub-document template](references/sub-doc-template.md) <br>
- [Validation checklist](references/validation-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, Python command examples, generated files, and validation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included initializer writes local skill files and refuses to overwrite existing files unless --force is used. The validator reports structural and reference-rule findings for target Nika skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
