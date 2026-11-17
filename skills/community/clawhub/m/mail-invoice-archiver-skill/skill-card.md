## Description:

Read supported mailbox providers such as 126, 163, and Gmail, identify invoice attachments or invoice download links, archive invoices by month, deduplicate by invoice number and amount, and prepare monthly reports plus delivery bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure mailbox access, sync likely invoice mail, archive invoice files by month, and summarize totals, duplicates, conflicts, high-value invoices, and failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires mailbox access and writes invoice archives locally.

Mitigation: Use the narrowest mailbox and archive location practical, and prefer system credential storage or prompt mode over plaintext config and command-line secrets.

Risk: Sync can follow invoice links from email, and the security summary flags weak URL scoping and unsafe download limits.

Mitigation: Run sync with link-following disabled or configure a narrowly trusted link policy until URL validation and download-size limits are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amortalsodyssey/skills/mail-invoice-archiver-skill)
- [Compatibility Notes](references/compatibility-notes.md)
- [Feishu Example Config](config/feishu/config.example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command output, local archive files, summary files, and delivery zip bundles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces month-scoped invoice archives, SQLite-backed metadata, report summaries, and chat-delivery package paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
