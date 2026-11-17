## Description:

Nano Banana 2 \u2014 Pro Pack on RunComfy helps agents generate text-to-image outputs with Google's Nano Banana 2 model through the RunComfy CLI, including batch variants, in-image typography, configurable resolution, aspect ratio, output format, seeds, and optional web-grounded context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for Nano Banana 2 image-generation commands, prompt guidance, and RunComfy input settings for marketing drafts, social thumbnails, batch variants, typography-heavy images, and web-grounded current-event imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated-image requests are sent to RunComfy.

Mitigation: Avoid submitting sensitive prompts or confidential creative briefs unless the user is comfortable with RunComfy processing them.

Risk: The skill requires a RunComfy token stored locally or supplied through RUNCOMFY_TOKEN.

Mitigation: Store the token only in controlled environments, protect local configuration files, and rotate the token if it may have been exposed.

Risk: Higher resolutions, larger batches, and optional web-grounded generation can increase cost and latency.

Mitigation: Use default or lower-cost settings for drafts, limit batch sizes intentionally, and enable web search only when current context is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/nano-banana-2-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy)
- [Nano Banana 2 model page](https://www.runcomfy.com/models/google/nano-banana-2?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [RunComfy CLI invocations can produce generated image files in a caller-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
