## Description:

Gmail triage assistant using Haiku LLM for classification, label application, and draft replies (uses gog CLI; never auto-sends).

This skill is ready for commercial/non-commercial use.

## Publisher:

[officialdelta](https://clawhub.ai/user/officialdelta)

### License/Terms of Use:

MIT-0

## Use Case:

Gmail users can use this skill to summarize recent inbox messages, classify them into practical labels, and prepare short reply drafts for human review. It is intended for mailbox triage workflows where drafts and labels are useful but automatic sending is not acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default account and keyring password handling can expose or misdirect mailbox access.

Mitigation: Replace hardcoded defaults with explicit local configuration and require the user to supply their own Gmail account and secure credential handling before use.

Risk: Mailbox-derived summaries, drafts, labels, and voice-reference content may contain sensitive personal information.

Mitigation: Delete the packaged personal voice reference, store generated cache files with restrictive permissions, and define cleanup steps for inbox summaries, triage labels, triage digests, and draft queues.

Risk: Email summaries are processed by an LLM classification step.

Mitigation: Obtain clear consent for LLM processing of mailbox content and limit summaries to the minimum content needed for triage.

Risk: Incorrect labels could be applied to Gmail threads.

Mitigation: Review the generated classification JSON before running label application and keep the no-auto-send rule in place for all replies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/officialdelta/skills/gmail-secretary)
- [Voice reference](references/voice.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown triage digests and draft queues, JSON label classifications, and shell-command workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local cache files for inbox summaries, triage labels, triage digests, and draft queues; labels may be applied to Gmail threads after review.]

## Skill Version(s):

1.0.27 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
