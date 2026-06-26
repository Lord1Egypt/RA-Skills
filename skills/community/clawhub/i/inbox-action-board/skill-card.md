## Description: <br>
Organizes emails or messages into reply, waiting, follow-up, and archive action views for inbox triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and productivity-focused users use this skill to turn email summaries, chat snippets, and pending replies into a reviewable Markdown action board with next steps and confirmation gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inbox and message inputs may contain private or sensitive information. <br>
Mitigation: Treat message contents as private data and consider redaction before processing or sharing generated boards. <br>
Risk: The generated action board may be incomplete or may misclassify reply, waiting, follow-up, or archive items. <br>
Mitigation: Review the board and confirmation gaps before sending messages, deleting content, or making external-system changes. <br>
Risk: The helper script can create or overwrite the specified output file. <br>
Mitigation: Run it only on intended input files and choose an output path that is acceptable to create or overwrite. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/inbox-action-board) <br>
- [Skill README](artifact/README.md) <br>
- [Output template](artifact/resources/template.md) <br>
- [Structured specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown action board, or JSON containing the generated report when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local output file when the helper script is run with an explicit output path; otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
