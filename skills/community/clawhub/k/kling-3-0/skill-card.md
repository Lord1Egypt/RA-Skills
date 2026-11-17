## Description:

Kling 3.0 — Pro Pack on RunComfy helps agents choose and invoke RunComfy CLI endpoints for Kling 3.0 text-to-video and image-to-video generation across Standard, Pro, and 4K tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and automation agents use this skill to generate or animate cinematic video through RunComfy's Kling 3.0 endpoints. It guides tier and mode selection, input shaping, and CLI invocation for draft previews, hero 1080p clips, native 4K masters, and image-to-video animation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires RunComfy authentication through a local login or RUNCOMFY_TOKEN.

Mitigation: Use a token scoped to RunComfy, keep unrelated secrets out of the same shell, and prefer a pinned or locally installed CLI version.

Risk: Kling 3.0 generation sends prompts and image URLs to RunComfy for remote processing.

Mitigation: Avoid submitting sensitive prompts or private image URLs unless that data is appropriate for the RunComfy service boundary.

Risk: Generated videos, especially 4K outputs, can be large and are downloaded into the selected output directory.

Mitigation: Choose output directories deliberately and confirm available disk and bandwidth before batch or 4K runs.

Risk: Image-to-video mode requires a publicly fetchable HTTPS image URL.

Mitigation: Use trusted image hosts and avoid exposing private assets through public URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/kling-3-0)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI introduction](https://docs.runcomfy.com/cli/introduction)
- [RunComfy Kling 3.0 model page](https://www.runcomfy.com/models/kling/kling-3.0)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce RunComfy CLI invocations, endpoint choices, input schemas, pricing notes, and output-directory guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
