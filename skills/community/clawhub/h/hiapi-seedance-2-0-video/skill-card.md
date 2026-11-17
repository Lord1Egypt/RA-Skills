## Description:

Generate videos with HiAPI's seedance-2-0 model via the HiAPI unified async task API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiapiai](https://clawhub.ai/user/hiapiai)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent users use this skill to generate Seedance 2.0 videos from text prompts, first or last frame images, and multimodal reference material through HiAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote install or update sources may influence persistent agent files and user-run commands.

Mitigation: Prefer OpenClaw's controlled install path or a pinned commit, and review update commands before running them.

Risk: A custom HIAPI_BASE_URL can redirect requests and API keys to an untrusted endpoint.

Mitigation: Keep HIAPI_BASE_URL unset unless the endpoint is fully trusted.

Risk: Generated videos downloaded to local storage can consume disk space.

Mitigation: Use a constrained output directory with available disk space.

## Reference(s):

- [HiAPI Seedance 2.0 Video API](references/api.md)
- [Output Handling](references/output.md)
- [HiAPI Docs](https://docs.hiapi.ai)
- [HiAPI Pricing](https://www.hiapi.ai/en/pricing)
- [ClawHub Skill Page](https://clawhub.ai/hiapiai/skills/hiapi-seedance-2-0-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can return a downloaded video file path or a remote video URL when download is not possible.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
