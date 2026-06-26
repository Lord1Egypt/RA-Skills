## Description: <br>
Project Brief Writer turns scattered requirements, chat notes, and meeting content into a structured project brief with scope, acceptance criteria, risks, and milestones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and project leads use this skill to convert raw requirements, goals, constraints, and related conversations into a reviewable project brief. It is intended for drafting objectives, scope, requirements, acceptance criteria, dependencies, risks, milestones, and clarification items before formal approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper can read the input path selected by the user and can write to the selected output path. <br>
Mitigation: Run it only on intended project materials, avoid broad sensitive directories, and inspect the chosen output path before writing. <br>
Risk: Generated briefs may reflect incomplete, ambiguous, or sensitive source material. <br>
Mitigation: Review the draft before using it for decisions, approvals, external sharing, or execution planning; redact sensitive inputs where appropriate. <br>
Risk: The skill is not suitable for legal contracts or replacing formal requirements approval. <br>
Mitigation: Use the output as a reviewable draft and route legal, compliance, or final approval decisions through the appropriate formal process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/project-brief-writer) <br>
- [Skill specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>
- [Example output](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown brief, or JSON containing the generated report when the local helper is run with JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated brief to a user-selected output file when the local Python helper is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
