## Description:

Use the OpenClaw `infer` CLI for provider-backed model, image, audio transcription, TTS, video, web-search, and embedding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[takhoffman](https://clawhub.ai/user/takhoffman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and run OpenClaw `infer` CLI commands for provider-backed model, image, audio transcription, TTS, video, web-search, and embedding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or invoking the wrong OpenClaw CLI package or provider configuration could run unintended tooling or send requests to unintended providers.

Mitigation: Confirm the npm package, `openclaw` binary on PATH, and configured provider before running commands.

Risk: Prompts, local files, audio, video, images, and search queries may be sent to configured inference providers.

Mitigation: Avoid secrets or regulated data unless the provider's data handling rules have been reviewed and approved.

## Reference(s):

- [OpenClaw Infer documentation](https://docs.openclaw.ai/cli/infer)
- [OpenClaw Infer ClawHub release](https://clawhub.ai/takhoffman/skills/openclaw-infer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill encourages `--json` for machine-readable results and requires the `openclaw` binary on PATH.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
