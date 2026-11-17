## Description:

Generate HappyHorse 1.0 text-to-video clips through HiAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiapiai](https://clawhub.ai/user/hiapiai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to generate short HappyHorse 1.0 text-to-video clips via HiAPI, returning a downloaded video file when available or a remote URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and update flows may execute code during installation or upgrade.

Mitigation: Review the skill before installing, prefer a pinned commit or trusted OpenClaw installation path, and manually verify printed update commands before running them.

Risk: A custom HIAPI_BASE_URL can redirect API requests and credentials to an untrusted endpoint.

Mitigation: Leave HIAPI_BASE_URL unset unless the endpoint is fully trusted, so requests use the default HiAPI endpoint.

Risk: Video generation can fail, time out, or return only a remote URL.

Mitigation: Return only the CLI-reported saved file path or remote URL, and provide the reported status, compact error message, and next action when generation fails.

## Reference(s):

- [HiAPI HappyHorse 1.0 Video API](artifact/references/api.md)
- [Output Handling](artifact/references/output.md)
- [HiAPI Docs](https://docs.hiapi.ai)
- [HiAPI Skill Page](https://clawhub.ai/hiapiai/skills/hiapi-happyhorse-1-0-video)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and CLI JSON output; generated videos are saved as MP4 files or returned as remote URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HIAPI_API_KEY; supports 3 to 15 second videos, 720p or 1080p resolution, common aspect ratios, and optional seed values.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; package.json reports 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
