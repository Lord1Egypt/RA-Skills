## Description: <br>
Turn a day of memory into a clear owner brief with highlights, decisions, open loops, and next-step recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asistent-alex](https://clawhub.ai/user/asistent-alex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to convert daily memory files and lossless-claw SQLite messages into structured owner briefs with highlights, decisions, open loops, and next-step recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes broad GraQle agent instructions that are unrelated to normal Mindkeeper brief generation. <br>
Mitigation: Review the bundled agent instructions before installation and disable or ignore them unless GraQle behavior is explicitly desired. <br>
Risk: Generated briefs can contain sensitive memory-derived content. <br>
Mitigation: Use local text, HTML, or .eml output first and inspect the full content before sharing or sending it. <br>
Risk: Optional email delivery can send brief content through sendmail or NexLink. <br>
Mitigation: Verify the recipient, subject, body, and delivery mode before enabling live email delivery. <br>


## Reference(s): <br>
- [Openclaw Mindkeeper ClawHub Release](https://clawhub.ai/asistent-alex/openclaw-mindkeeper) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text or HTML briefs, optional .eml email messages, and CLI diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local output files and can optionally deliver email through file output, sendmail, or NexLink when email flags are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
