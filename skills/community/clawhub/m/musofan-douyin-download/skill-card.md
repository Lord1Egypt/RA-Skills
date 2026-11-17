## Description:

Download Douyin (Chinese TikTok) videos to local MP4 files from shared Douyin/TikTok URLs using exported browser cookies and a local HTTP proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musofan](https://clawhub.ai/user/musofan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download Douyin or TikTok videos to local MP4 files from shared video URLs, using their own exported browser cookies and local proxy/browser setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses exported Douyin/TikTok browser cookies.

Mitigation: Use a limited, protected cookie file and refresh it only when needed; do not share or upload the cookie file.

Risk: The skill navigates to user-provided video URLs with local network-capable browser automation.

Mitigation: Use only trusted Douyin/TikTok URLs and avoid running the skill in environments where internal web services or sensitive local files are reachable.

Risk: The skill writes downloaded media to a local path.

Mitigation: Choose a dedicated download directory and review downloaded files before reuse or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/musofan/skills/musofan-douyin-download)
- [Project homepage](https://github.com/musofan/douyin-download)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash command examples; runtime output includes progress text, local file paths, and downloaded MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local MP4 downloads and status messages; no additional structured output is specified.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
