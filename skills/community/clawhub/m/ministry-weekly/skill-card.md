## Description: <br>
Ministry Weekly helps church staff turn a weekly Sunday briefing into a ready-to-review content package with bulletin copy, scripture context, platform-specific social posts, a weekly email, image prompts, sermon-series recap, and optional confirmation-gated Telegram delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Church staff and ministry communicators use this skill to produce weekly Sunday communications from a concise sermon and announcement brief. It supports recurring church profile context, sermon-series continuity, draft publishing copy, graphics prompts, and optional Telegram delivery after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps church profile and weekly ministry context in a local ministry-data.json file. <br>
Mitigation: Review the stored church profile and weekly brief data periodically, avoid congregant personal information, and remove local data that is no longer needed. <br>
Risk: Generated bulletin, social, email, image-prompt, or Telegram content may contain incorrect scripture framing, unsuitable announcements, or congregation-specific details that should not be published. <br>
Mitigation: Review all generated content before publishing or sending, with special attention to scripture interpretation, public announcements, and congregation privacy. <br>
Risk: Telegram delivery can post externally through the user's configured integration. <br>
Mitigation: Use the built-in confirmation gate: inspect the assembled Telegram message and approve posting only when the destination channel and content are correct. <br>


## Reference(s): <br>
- [Ministry Weekly on ClawHub](https://clawhub.ai/chris-openclaw/ministry-weekly) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown-style content package with structured sections, draft copy, prompts, and optional Telegram-formatted message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local ministry-data.json for church profile, sermon series, and confirmed weekly briefs; Telegram posting is optional and requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
