## Description:

Universal video downloader supporting multiple platforms (Douyin, Bilibili, YouTube, TikTok, etc.). Can download videos by URL or search by keyword (Douyin supported). Use when users need to download videos from video platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwkgit](https://clawhub.ai/user/wwkgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to download single or batched videos from supported platforms, search Douyin by keyword, and save local media files with JSON metadata. Users should only download content they are authorized to use and should review platform terms before running it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser mode may use authenticated browser cookies while visiting remote video pages.

Mitigation: Run the skill in a disposable container or VM with no sensitive browser profile and avoid browser mode for untrusted URLs.

Risk: The browser automation path disables Chromium sandboxing.

Mitigation: Use strict isolation, pinned dependencies, and minimal mounted folders before executing downloads.

Risk: The skill contacts third-party video platforms and writes media and metadata locally.

Mitigation: Review platform terms, download only authorized content, and limit output directories to non-sensitive locations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wwkgit/skills/multi-platform-video-downloader)
- [Docker usage guide](artifact/DOCKER_README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime output includes downloaded media files and JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to local download directories and may include per-video metadata JSON and batch summary JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
