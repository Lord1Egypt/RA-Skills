## Description: <br>
Converts FAQs, chats, and scattered notes into reviewable SOP or playbook drafts with exception branches and rollback steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, support, training, and knowledge-management teams use this skill to turn raw FAQs, chat logs, and procedural notes into structured Markdown SOPs, playbooks, checklists, and review drafts before real-world use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input materials may contain sensitive chat logs, personal data, or operational details. <br>
Mitigation: Redact sensitive content before processing and use the skill only on files intentionally selected for local analysis. <br>
Risk: Generated SOPs or playbooks may be incomplete or unsuitable for a real procedure. <br>
Mitigation: Treat outputs as review drafts and require human approval before execution, publication, or system changes. <br>
Risk: Writing output to an unintended path could expose or overwrite local draft material. <br>
Mitigation: Choose output paths deliberately, prefer dry-run or stdout while reviewing, and inspect generated files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/knowledge-to-playbook) <br>
- [Skill README](artifact/README.md) <br>
- [Skill specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown SOP/playbook drafts or JSON reports generated from local input files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional local Python script reads chosen inputs and can write a chosen output path; no network, credential, persistence, or destructive behavior is indicated by server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
