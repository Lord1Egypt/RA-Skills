## Description:

Create product demo videos with voiceover, text overlays, and real browser interactions using Puppeteer, edge-tts, Pillow, and FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiazai77](https://clawhub.ai/user/xiazai77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and product teams use this skill to plan and generate short product walkthrough or launch demo videos for web applications, including browser-recorded scenes, narration, overlays, and FFmpeg-encoded output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer adds global npm and Python packages and may download FFmpeg binaries or system fonts.

Mitigation: Review dependencies first, pin versions and checksums where possible, and install in a disposable container or VM without root privileges.

Risk: Browser recording can visit arbitrary URLs and capture visible page content.

Mitigation: Record only trusted sites and avoid entering secrets, credentials, customer data, or unreleased product information during capture.

Risk: Custom scene content is passed into shell-string subprocess calls during audio and video generation.

Mitigation: Replace shell-string execSync usage with argument-array subprocess calls or strictly sanitize scene text before using generated or third-party scenes.

Risk: Voiceover generation uses edge-tts and sends narration text to an external TTS service.

Mitigation: Confirm external service use is acceptable and keep sensitive or private content out of narration text.

## Reference(s):

- [Demo Planning Guide](references/demo-planning.md)
- [Recording Template](scripts/record-demo.mjs)
- [Dependency Installer](scripts/install-deps.sh)
- [ClawHub Skill Page](https://clawhub.ai/xiazai77/skills/product-demo-video)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets; generated MP4 video files when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses customizable scene definitions; generated media depends on local browser, TTS, fonts, and FFmpeg availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
