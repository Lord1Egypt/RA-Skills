## Description: <br>
Download PhotoPlus / 谱时图片直播 albums from a URL or activity ID; use to inspect metadata, filter date tabs, save JSON, or write caption/GPS metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloene](https://clawhub.ai/user/helloene) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive PhotoPlus live album images they are authorized to download, inspect album metadata, select date tabs, and save JSON or photo metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can fetch and run mutable third-party code from the upstream downloader. <br>
Mitigation: Use a pinned, reviewed local copy of the upstream downloader with --repo-dir when possible instead of fetching the live main branch. <br>
Risk: The wrapper can install Python packages without pinning or verification when --install-deps is used. <br>
Mitigation: Run --dry-run first and avoid --install-deps unless the execution environment permits package installation and the dependencies have been reviewed. <br>
Risk: Album downloads may contain photos or metadata the user is not authorized to store. <br>
Mitigation: Use the skill only for albums the user owns or has permission to archive, and inspect metadata or run a small --count test before large downloads. <br>


## Reference(s): <br>
- [Upstream Project Notes](references/upstream-project.md) <br>
- [helloene/live-album-downloader](https://github.com/helloene/live-album-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and file output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can download image files, write JSON sidecars, and write EXIF/IPTC metadata through the upstream PhotoPlus downloader.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
