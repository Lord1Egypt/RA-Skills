## Description:

Guides an agent to generate curl commands for downloading Douyin video files with a Referer header and configured local save paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnview](https://clawhub.ai/user/gnview)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to have an agent compose curl-based download commands for Douyin video URLs, including output paths and filenames. Use should be limited to content the user owns or has explicit permission to download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches use of a Referer header to bypass Douyin anti-hotlink access controls.

Mitigation: Use only authorized platform features or content the user has explicit permission to download, and review legal, copyright, terms-of-service, and account consequences before use.

Risk: Generated download commands may fail when Douyin playback URLs expire or when the target directory does not exist.

Mitigation: Refresh authorized playback URLs before running commands and create the configured download directory in advance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gnview/skills/gnview-douyin-video-download)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curl command guidance using a Referer header, a video URL, and a local output path; it does not download files by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
