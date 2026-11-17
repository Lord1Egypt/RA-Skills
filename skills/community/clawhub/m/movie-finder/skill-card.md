## Description:

Searches for movies in Chinese or English, filters by genre, year, or rating, and can generate a local HTML playback page with embedded iframe sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chugenice](https://clawhub.ai/user/chugenice)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users find movie metadata, recommend movies by genre, year, or rating, and produce a local HTML page that embeds selected third-party playback sources when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated playback pages can load unverified third-party streaming sites inside iframes.

Mitigation: Treat generated playback pages as untrusted web content and avoid entering credentials, payment details, or other sensitive information in embedded frames.

Risk: Free or third-party embed sources may be unreliable, unavailable, or unsuitable for the user's licensing expectations.

Mitigation: Prefer licensed streaming links or metadata-only use, and review generated source URLs before opening or sharing playback pages.

Risk: User-wide installation can cause the skill to activate during ordinary movie-related requests.

Mitigation: Install only when this behavior is intended, and scope or remove the skill when third-party playback discovery is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chugenice/skills/movie-finder)
- [Publisher profile](https://clawhub.ai/user/chugenice)
- [Skill instructions](artifact/SKILL.md)
- [Installation notes](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown responses with optional generated HTML files and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated playback pages may contain third-party iframe embeds and source-switching controls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
