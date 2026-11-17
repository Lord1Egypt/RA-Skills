## Description:

Resolves and downloads Douyin and Bilibili video links, including short links, by selecting high-quality streams, falling back across supported methods, and saving MP4 output locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to process supported Douyin or Bilibili URLs, resolve video streams, and save downloaded MP4 files to a local downloads directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs dependencies and browser components, which can modify the host environment.

Mitigation: Review before installing and run only in a contained environment with dependencies preinstalled and pinned where possible.

Risk: Weak URL and file-path controls could allow unexpected requests or writes outside the intended download workflow.

Mitigation: Validate exact Bilibili and Douyin hosts before requests, avoid arbitrary custom paths or filenames, and confine downloads to a dedicated directory without overwriting existing files.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [ClawHub Skill Page](https://clawhub.ai/wangminrui2022/skills/link-resolver-engine)
- [Publisher Profile](https://clawhub.ai/user/wangminrui2022)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command invocations and local MP4 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are intended for Bilibili and Douyin links only and default to a local downloads directory.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
