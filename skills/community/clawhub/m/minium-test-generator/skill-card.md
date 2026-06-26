## Description: <br>
Minium recorded-script to test-case tool that parses recorded scripts and generates project-aligned test cases and page objects while preserving step completeness and logical consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiziria](https://clawhub.ai/user/yiziria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to turn Minium recorded scripts into page objects, executable tests, and step-comparison materials for WeChat mini-program automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recorded Minium scripts may contain sensitive test data, identifiers, or environment details. <br>
Mitigation: Redact sensitive values before providing recorded scripts to the skill. <br>
Risk: Generated files or modifications may affect files outside the intended test scope if the target directory is too broad. <br>
Mitigation: Provide only the intended test directory and review generated diffs before running or committing changes. <br>
Risk: The artifact includes IDE assistant configuration that may not match the user's approval expectations. <br>
Mitigation: Remove or ignore the bundled .idea Sweep auto-approval file if that IDE assistant is used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yiziria/minium-test-generator) <br>
- [Quick start guide](快速开始.md) <br>
- [Avoid missing steps](core-skills/避免漏掉步骤.md) <br>
- [Code generation quality control flow](docs/代码生成质量控制流程.md) <br>
- [Code review checklist](docs/代码审查清单.md) <br>
- [Code style guide](docs/代码规范.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code, generated files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or propose page-object files, test-case files, step checklists, and validation reports in the user-specified test directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 11.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
