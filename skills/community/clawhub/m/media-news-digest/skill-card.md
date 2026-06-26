## Description: <br>
Generates media and entertainment industry news digests from RSS feeds, Twitter/X accounts, Reddit, and web search, with deduplication, quality scoring, Discord delivery, email output, and optional PDF attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinstein](https://clawhub.ai/user/dinstein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and teams use this skill to generate daily or weekly media and entertainment news digests from configured public sources and deliver them to Discord or email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated digests to configured Discord channels or email recipients. <br>
Mitigation: Verify the destination channel or email address before scheduling recurring delivery. <br>
Risk: The skill may use optional API keys for Twitter/X and web search backends. <br>
Mitigation: Provide only the API keys needed for the selected sources and keep them in environment variables or local configuration. <br>
Risk: The skill writes and cleans archive files for previous reports. <br>
Mitigation: Use a dedicated archive directory so retention and cleanup do not affect unrelated files. <br>
Risk: Some configured Twitter/X sources may be unverified or need correction. <br>
Mitigation: Review, disable, or correct those sources before relying on scheduled digests. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/dinstein/media-news-digest) <br>
- [Digest prompt template](references/digest-prompt.md) <br>
- [Discord output template](references/templates/discord.md) <br>
- [Email output template](references/templates/email.md) <br>
- [Configuration schema](config/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest content, JSON pipeline artifacts, and shell commands for collection, summarization, PDF generation, and delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce Discord-ready or email-ready digest text, optional HTML/PDF email artifacts, and archive files.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
