## Description:

灵犀Note录音文件查询 helps an agent query sales and meeting recording lists and details from the Lingxi API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubf1215](https://clawhub.ai/user/liubf1215)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure a Lingxi API key, query sales or meeting recordings, and inspect returned recording details without inventing IDs or responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a live Lingxi API key that can access recording metadata, audio URLs, transcripts, and analysis.

Mitigation: Use only an API key intended for this access level, keep the OpenClaw config file permission-restricted, redact the key in chat and terminal output, and rotate any exposed key.

Risk: Recording content can include private customer, sales, or meeting information.

Mitigation: Return only the information the user requested, avoid posting full recording contents in shared channels, and confirm authorization before exposing audio URLs or transcript details.

Risk: The artifact includes guidance for viewing configuration that could reveal secrets if followed literally.

Mitigation: Use masked checks for configuration validation and never display the full `LYK_API_KEY` value.

## Reference(s):

- [Recording list and detail query reference](artifact/references/list.md)
- [Lingxi API configuration reference](artifact/references/config.md)
- [Lingxi API base URL](https://aiapi.szyldata.com/api)
- [ClawHub skill page](https://clawhub.ai/liubf1215/skills/lingxiai-note-recording)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and structured recording data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-derived recording metadata, audio URLs, transcripts, summaries, and analysis fields when authorized.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
