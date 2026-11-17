## Description:

Uses the MakeMidas CLI to generate images and short videos from prompts or reference images and save the results locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypercube67-formal](https://clawhub.ai/user/hypercube67-formal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to generate images or short video clips through MakeMidas and save the resulting files locally. The CLI uses the user's MakeMidas credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI download instruction is unpinned, and the scan does not identify which package version would run.

Mitigation: Review the package source and select a specific version before installing; use an already installed CLI where practical.

Risk: Image and video generations spend the user's MakeMidas credits.

Mitigation: Check available credits and expected costs before requesting generation, especially for video, 4K, or multiple outputs.

## Reference(s):

- [MakeMidas developer documentation](https://makemidas.com/developers)
- [MakeMidas pricing](https://makemidas.com/pricing)
- [MakeMidas skill release on ClawHub](https://clawhub.ai/hypercube67-formal/skills/makemidas)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may result in generated image or video files saved locally.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
