## Description:

Photo Alchemy transforms photos into surrealist AI art by using Claude to write a story and prompt, then Gemini to generate a reimagined image, with optional Apple Photos workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hbmartin](https://clawhub.ai/user/hbmartin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn local photos or Apple Photos album images into AI-generated surrealist artwork, manage style and character-mapping settings, and optionally automate album output for screensavers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The permanent installation path pipes a remote installer directly into a shell.

Mitigation: Use a pinned, verifiable package version or one-off uvx execution instead of curl-to-shell installation.

Risk: API keys may be saved in the local application database.

Mitigation: Prefer environment variables or a platform credential store, and avoid storing long-lived secrets in the app database.

Risk: Apple Photos and launchd workflows can repeatedly access photos, upload photo-derived content to AI services, and persist scheduled execution.

Mitigation: Use least-privilege source and destination albums, enable launchd scheduling only after reviewing the LaunchAgent, and monitor recurring API usage and photo uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hbmartin/skills/photo-alchemy)
- [Publisher profile](https://clawhub.ai/user/hbmartin)
- [Project homepage](https://github.com/hbmartin/imagemine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described CLI may create image files, SQLite run history, Apple Photos album entries, and optional launchd scheduling configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
