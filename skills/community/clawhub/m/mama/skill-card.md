## Description:

MAMA is a multi-account IMAP/SMTP mail assistant that helps agents inspect, search, read, draft replies, forward, explicitly send, organize, download attachments from, and summarize configured mailboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hejunhui-73](https://clawhub.ai/user/hejunhui-73)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, personal users, and operators use this skill to manage one or more locally configured mailboxes, keep account context consistent across mail actions, and generate keyword- or deadline-focused mail digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores mailbox credentials locally and can access configured mailboxes.

Mitigation: Install only when mailbox access is acceptable, use dedicated app passwords where possible, and keep scripts/mail_config.json private.

Risk: Secret values can be exposed if passed through unsafe temporary files or command history.

Mitigation: Prefer interactive input, stdin, or environment variables; avoid /tmp files for secrets unless file permissions are locked down.

Risk: Send and move operations can change mailbox state or send messages externally.

Mitigation: Review send, forward-with-send, and move commands before execution and require explicit confirmation flags for direct state-changing actions.

Risk: Cleanup behavior can remove files when combined with custom output directories.

Mitigation: Avoid using custom --output-dir together with --cleanup-days unless the target directory contents have been reviewed.

Risk: Downloaded attachments can contain unsafe file types or large files.

Mitigation: Keep the default risky-extension blocking in place and use size limits for attachment downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hejunhui-73/skills/mama)
- [Configuration guide](references/config-guide.md)
- [First-run guide](references/first-run-guide.md)
- [Output format guide](references/output-format-guide.md)
- [Schedule guide](references/schedule-guide.md)
- [Keyword guide](references/keyword-guide.md)
- [Deadline detection guide](references/deadline-detection-guide.md)
- [Channel routing guide](references/channel-routing-guide.md)
- [Troubleshooting guide](references/troubleshooting-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and optional JSON command output, with local .eml drafts, downloaded attachments, summaries, cache files, and configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mail operations depend on local IMAP/SMTP account configuration and explicit confirmation for direct send or move actions.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
