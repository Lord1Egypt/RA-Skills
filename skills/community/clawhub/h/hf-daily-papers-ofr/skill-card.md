## Description:

Generates Chinese OFR-focused daily paper digests by collecting Hugging Face Daily Papers and arXiv CS.CV metadata, classifying papers into six vision-related categories, and producing Markdown or Telegram-ready reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscffaa](https://clawhub.ai/user/wscffaa)

### License/Terms of Use:


## Use Case:

Developers and research teams use this skill to monitor daily OFR-related computer vision papers and receive categorized paper recommendations as Markdown files or Telegram-formatted text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Hugging Face and arXiv to fetch public paper metadata.

Mitigation: Install and run it only in environments where outbound access to those services is expected.

Risk: Telegram automation can send generated report content to the configured target without an interactive confirmation.

Mitigation: Set TELEGRAM_TARGET deliberately, review cron configuration before enabling it, and use a test target before production posting.

Risk: arXiv metadata is fetched over HTTP and paper titles are rendered into Markdown links without escaping.

Mitigation: Review generated Markdown before redistribution when report integrity matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wscffaa/skills/hf-daily-papers-ofr)
- [Hugging Face Daily Papers](https://huggingface.co/papers)
- [arXiv API](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown reports and Telegram-ready plain text, with CLI and cron usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated report files under recommendations/ and can optionally send a generated digest to a configured Telegram target.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
