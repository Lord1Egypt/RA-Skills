## Description:

Knowledge Base Collector - save YouTube, URLs, text to Obsidian with AI summarization. Auto-transcribes videos, fetches pages, supports weekly/monthly digest emails and nightly research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbiger](https://clawhub.ai/user/arbiger)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to collect YouTube videos, web pages, and plain text into an Obsidian knowledge base, with optional transcription, summarization, digest generation, and nightly research automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can email local note metadata to a hard-coded external recipient.

Mitigation: Do not use email features until the recipient is changed to an address you control and the message body has been previewed.

Risk: The nightly research workflow can repeatedly run searches and send email in the background when scheduled with cron.

Mitigation: Review cron configuration before enabling it, and run save-only mode first to inspect generated results.

Risk: Running the collectors on private vaults or untrusted URLs can expose sensitive local notes or process untrusted web content.

Mitigation: Avoid private vaults and untrusted URLs unless URL validation, private temporary files, and dependency pinning are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbiger/skills/kb-collector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, digest text, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Markdown files to a local Obsidian vault and send digest email when send flags are used.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
