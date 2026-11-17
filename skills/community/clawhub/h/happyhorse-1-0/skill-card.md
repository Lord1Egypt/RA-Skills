## Description:

HappyHorse 1.0 on RunComfy helps an agent guide text-to-video generation through the RunComfy CLI, including prompt shaping, supported parameters, invocation examples, and operational limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate short HappyHorse 1.0 text-to-video clips through RunComfy, with guidance for prompts, aspect ratios, duration, resolution, watermark settings, and reproducible seeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunComfy authentication tokens are required for normal use.

Mitigation: Use a narrowly scoped RunComfy token and prefer environment-based credentials in CI or containers.

Risk: Prompts and generated results are sent to and retrieved from RunComfy.

Mitigation: Avoid submitting sensitive content unless RunComfy account terms and data-handling expectations fit the use case.

Risk: The skill depends on the RunComfy CLI package and network service availability.

Mitigation: Consider using a pinned or project-local @runcomfy/cli version and verify the package source before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/happyhorse-1-0)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0)
- [HappyHorse 1.0 text-to-video](https://www.runcomfy.com/models/happyhorse/happyhorse-1-0/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers RunComfy CLI inputs, prompt patterns, operational limits, and generated video output handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
