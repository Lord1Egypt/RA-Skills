## Description:

Generate images with an OpenAI-compatible image provider such as happy/gpt-image-2, with retries and bounded batch concurrency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate single or batched image files through a locally configured OpenAI-compatible image provider, with bounded retries and per-task result records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generator logs are saved locally in generated run directories.

Mitigation: Avoid entering secrets or sensitive business data in prompts, and review or clean generated run directories after use.

Risk: The skill can fetch provider-supplied image URLs that are not independently validated by the release evidence.

Mitigation: Use trusted image providers and prefer bounded inline image data until URL validation controls are added.

Risk: Image generation depends on the configured external provider and its handling of prompts and outputs.

Mitigation: Install only with providers whose access, retention, and content policies are acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/happy-img2-direct)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration]

**Output Format:** [PNG image files with JSON status and batch result records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to local run directories; batch mode records one result per task and continues when individual tasks fail.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
