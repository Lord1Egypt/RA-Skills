## Description:

IMAP bulk email triage for pattern-based delete and archive workflows with dry-run preview, YAML/JSON configuration, STARTTLS support, and UID-based bulk operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview and apply reproducible IMAP inbox cleanup rules for large backlogs, moving or deleting messages by sender domain, subject keyword, or configured pattern. It is best suited for bulk triage where the user can review dry-run counts before any live mailbox changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can permanently delete mailbox messages or expunge archived messages from the inbox.

Mitigation: Run dry-run first, review counts and sample subjects, and prefer archive rules over delete rules when retention is uncertain.

Risk: Broad or mismatched sender-domain and subject patterns can affect important messages.

Mitigation: Populate leave_domains for banks, authentication, receipts, legal, account, and payment services before running live.

Risk: IMAP credentials and certificate-verification bypass can expose sensitive mailbox access.

Mitigation: Use revocable account-specific credentials and only bypass certificate verification for a trusted local bridge such as 127.0.0.1.

Risk: Concurrent mail clients or server-side deleted flags can make live mailbox state harder to reason about.

Mitigation: Avoid running live cleanup while other mail clients may have messages marked deleted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/inbox-cleanup)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [SKILL.md](artifact/SKILL.md)
- [inbox_cleanup.py](artifact/scripts/inbox_cleanup.py)
- [config_example.yaml](artifact/scripts/config_example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML/JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can print dry-run or live execution summaries and can optionally write a JSON report.]

## Skill Version(s):

1.0.5 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
