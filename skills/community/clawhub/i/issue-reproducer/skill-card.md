## Description: <br>
Organizes bug descriptions into reproducible steps, environment details, expected and actual results, and minimum reproduction criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and support teams use this skill to turn bug reports and reproduction clues into structured, reviewable Markdown issue-reproduction drafts and checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional script can write or overwrite a report file when an output path is provided. <br>
Mitigation: Choose the output path deliberately, use dry-run or stdout when reviewing behavior, and pass only the specific bug material intended for processing. <br>
Risk: Bug reports can contain sensitive environment details or personal information. <br>
Mitigation: Review and redact sensitive inputs before processing whenever possible. <br>
Risk: Incomplete inputs may lead to overconfident reproduction drafts. <br>
Mitigation: Keep missing facts explicit as pending confirmation items and do not fabricate logs, root causes, or results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/issue-reproducer) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Output Template](artifact/resources/template.md) <br>
- [Structured Specification](artifact/resources/spec.json) <br>
- [Smoke Test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON, with optional local shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a user-directed report file when the optional Python script is run with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
