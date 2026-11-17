## Description:

Downloads videos from public LinkedIn posts as MP4 files without authentication or external dependencies, saving the best available quality to the current directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpnarchi](https://clawhub.ai/user/jpnarchi)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to build or run a Go CLI that downloads video media from public LinkedIn post URLs. It is intended for public posts that directly embed LinkedIn-hosted video content and do not require authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: README installation examples reference a placeholder GitHub path and an unpinned @latest command, creating supply-chain review risk.

Mitigation: Build only from the reviewed local source or replace installation instructions with a verified, pinned source before distribution.

Risk: URL handling can be risky if the CLI is exposed as an automated service for arbitrary submitted URLs.

Mitigation: Use only trusted public LinkedIn post URLs unless URL, redirect, response-size, and media-host validation are strengthened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpnarchi/skills/linkedin-video-dl)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands and MP4 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads an MP4 file to the current directory, shows progress, uses a temporary file during transfer, and skips existing filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
