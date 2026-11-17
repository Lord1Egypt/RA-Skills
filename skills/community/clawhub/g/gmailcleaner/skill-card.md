## Description:

Reads and searches Gmail folders and labels through the gog CLI so an agent can check inboxes, unread messages, spam, custom labels, threads, and message content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coorops25](https://clawhub.ai/user/coorops25)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to read, search, summarize, and navigate Gmail messages after configuring gog CLI access. It is suited to inbox checks, unread-message review, folder or label searches, and follow-up workflows that need message IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Gmail content and may require broad mailbox authorization.

Mitigation: Review before installing when Gmail contains sensitive personal, work, legal, financial, or authentication messages, and prefer Gmail-only authorization unless Sheets or Docs export is explicitly needed.

Risk: Analyzer and responder workflows may send selected email content to Anthropic.

Mitigation: Use those workflows only after confirming the user is comfortable with external AI processing of selected email content.

Risk: Related organizer, responder, scheduler, reporter, export, and logging workflows can modify mailbox state or persist email-derived information.

Mitigation: Require explicit confirmation before sending, deleting, bulk moves, scheduled jobs, exports, and persistent logs.

Risk: Installation through an unverified package path could introduce supply-chain risk.

Mitigation: Use the reviewed brew installation path when possible and avoid the npm install path unless it has been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coorops25/skills/gmailcleaner)
- [gog CLI homepage](https://gogcli.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized email lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses gog CLI JSON results as input, presents concise summaries instead of raw JSON, and preserves message IDs for follow-up actions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
