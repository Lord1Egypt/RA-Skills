## Description:

YouTube transcripts, 4K downloads, and video exploration. Onnex-owned fork of youtube-ultimate. Security reviewed before install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrtlearns](https://clawhub.ai/user/mrtlearns)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve YouTube transcripts, inspect video and channel metadata, search YouTube, and save media for local analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broader Google and YouTube OAuth authority than its read-style features require.

Mitigation: Use a Google/YouTube account suitable for this exposure and prefer a release that narrows OAuth scopes to read-only.

Risk: Reusable OAuth tokens are stored in a risky format.

Mitigation: Review token storage before installation and prefer a release that replaces pickle token storage with a safer documented format.

Risk: The artifact includes an unrelated gogcli credential fallback.

Mitigation: Remove or disable the fallback before use unless it is intentionally required and documented.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Pin dependencies and review updates before installing or running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrtlearns/skills/onnex-youtube)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands]

**Output Format:** [Plain text or JSON CLI output, with downloaded media files for download commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+. YouTube Data API commands require Google OAuth, and download commands require yt-dlp.]

## Skill Version(s):

4.2.2 (source: frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
