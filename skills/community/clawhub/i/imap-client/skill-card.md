## Description: <br>
Read, search, and download email over IMAP from the command line using the `myl` CLI client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggrrrh](https://clawhub.ai/user/aggrrrh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to let an agent inspect a configured mailbox, search messages, read selected email, and save raw messages or attachments through a read-only IMAP workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox credentials and can read sensitive email content. <br>
Mitigation: Use an app-specific password, prefer OpenClaw SecretRef or per-run environment injection, and avoid storing credentials in plaintext files where possible. <br>
Risk: The IMAP password may briefly be visible in process arguments while the wrapped `myl` command runs. <br>
Mitigation: Avoid shared multi-user machines for this workflow and run the skill only in an environment where local process visibility is acceptable. <br>
Risk: Email operations may expose more mailbox content than the user intended or mark messages read when requested. <br>
Mitigation: Use small result sets by default, summarize long messages instead of dumping full bodies, and pass `--mark-seen` only when the user explicitly asks to mark messages read. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aggrrrh/imap-client) <br>
- [Authentication & Connection](references/authentication.md) <br>
- [Installation](references/installation.md) <br>
- [Operations Reference](references/operations.md) <br>
- [Recipes](references/recipes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [myl CLI](https://github.com/pschmitt/myl) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown summaries with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save email bodies, raw .eml messages, HTML, or attachments to local files when requested.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
