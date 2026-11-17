## Description:

Instagram caption writer with hashtags, Story scripts, Reels scripts, bio optimization, and content calendar support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media managers, and marketing teams use this skill to draft and organize Instagram captions, hashtags, Story and Reels scripts, hooks, CTAs, translations, schedules, and related content notes in local logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram drafts, schedules, hashtags, and related notes are stored in plaintext local files and can be exported on command.

Mitigation: Avoid storing secrets or confidential campaign data; restrict or delete ~/.local/share/instagram-caption when the logs are no longer needed.

Risk: CSV exports may be opened in spreadsheet applications that interpret cell content.

Mitigation: Review CSV exports before sharing or opening them in spreadsheet tools, especially when entries contain leading formula characters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/instagram-caption)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text command output with optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores Instagram drafts, schedules, hashtags, and related notes locally under ~/.local/share/instagram-caption.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
