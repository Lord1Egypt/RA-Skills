## Description: <br>
IMAP bulk email triage - pattern-based delete/archive with dry-run mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People with IMAP mailboxes use this skill to prepare repeatable bulk cleanup workflows for deleting or archiving messages by sender domain, subject keyword, or regex after reviewing a dry run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live runs can permanently delete or archive mailbox messages. <br>
Mitigation: Run dry-run first, review matched counts and subjects, and populate leave_domains for banks, payment processors, auth, legal, receipts, and other important senders before applying changes. <br>
Risk: The script requires IMAP credentials and mailbox access. <br>
Mitigation: Use a controlled local environment, provide credentials through environment variables or a password manager, and avoid disabling TLS verification except for a trusted local bridge or equivalent controlled setup. <br>


## Reference(s): <br>
- [Inbox Cleanup on ClawHub](https://clawhub.ai/nissan/inbox-cleanup) <br>
- [Skill instructions](SKILL.md) <br>
- [Configuration example](scripts/config_example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML/JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce a dry-run summary and optional JSON report when the script is executed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
