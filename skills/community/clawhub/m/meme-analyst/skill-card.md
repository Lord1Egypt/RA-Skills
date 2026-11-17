## Description:

Analyzes memes, screenshots, and Telegram media by decomposing visual and textual elements, researching cultural references in the original language, and explaining humor mechanisms and irony depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antibagr](https://clawhub.ai/user/antibagr)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to explain image memes, screenshots, jokes, and Telegram-channel meme media. It helps identify cultural references, especially Russian-language references, and produce concise human-facing humor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private screenshots, sensitive chats, or Telegram channel media may be sent through external search or analysis flows.

Mitigation: Use only with sources where that processing is acceptable, and add consent, redaction, or source restrictions before handling sensitive content.

Risk: User or channel-derived meme content may be persisted in meme-analysis memory without clear retention limits.

Mitigation: Review and limit what is saved under memory/memes, and define retention or deletion practices before deployment.

Risk: Automated Telegram media ingestion can broaden collection beyond an interactive user request.

Mitigation: Enable cron ingestion only for approved channels and review channel configuration, media scope, and batch outputs.

## Reference(s):

- [Meme Analyst ClawHub Skill Page](https://clawhub.ai/antibagr/skills/meme-analyst)
- [antibagr Publisher Profile](https://clawhub.ai/user/antibagr)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown analysis with reference, twist, humor, irony, and context details when appropriate.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update meme-analysis memory files for templates, references, humor patterns, channels, and daily summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
