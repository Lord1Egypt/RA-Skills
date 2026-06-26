## Description: <br>
Harness Engineering provides a Generator/Evaluator coding workflow for planning, implementation, independent review, quality gates, and change audit records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure coding work into planning, implementation, independent evaluation, revision, and delivery stages. It is intended for programming tasks that benefit from explicit quality gates and auditable change records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can direct agents to commit and push code without a clear approval checkpoint. <br>
Mitigation: Require manual approval before any git commit or git push, and review the diff, commit message, target branch, and remote before delivery. <br>
Risk: Generated harness records can persist sensitive project details if secrets are included in planning, review, or summary files. <br>
Mitigation: Keep secrets out of generated harness files and review generated records before committing or sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cindypapa/openclaw-harness-engineering) <br>
- [Publisher profile](https://clawhub.ai/user/cindypapa) <br>
- [Harness Engineering skill source](artifact/SKILL.md) <br>
- [Quality gates template](artifact/templates/quality-gates.md) <br>
- [Evaluator SOP](artifact/skills/evaluator.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, templates, review reports, code changes, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent .harness planning, review, and summary records when used as directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
