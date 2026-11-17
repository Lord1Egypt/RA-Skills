## Description:

从小宇宙下载播客音频与节目说明，并指导代理下载音频、转换为 MP3、保存 show notes。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically comfortable podcast listeners use this skill to have an agent download Xiaoyuzhou episode audio, convert it to MP3, and save episode notes in a structured podcast directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to run shell tools that download audio, invoke ffmpeg, and write files to a podcast directory.

Mitigation: Review proposed commands before execution, use trusted episode URLs, and run in a workspace with appropriate file permissions.

Risk: The artifact references a download script that is not present in the submitted artifact.

Mitigation: Review the actual script implementation before relying on automated downloads.

Risk: The workflow deletes the original m4a file by default after conversion.

Mitigation: Set KEEP_M4A=true when the original download should be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/podcast-downloader-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with shell commands and generated audio or notes files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of curl, jq, and ffmpeg; output files are organized under the configured podcast directory.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
