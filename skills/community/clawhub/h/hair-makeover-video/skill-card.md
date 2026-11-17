## Description:

Generate vertical short videos of hair makeover or dye transformations with scissor cuts, color gradients, and strong before/after contrast using WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn hair makeover briefs and optional public HTTPS image URLs into WeryAI video generation parameters, confirmation steps, CLI/API execution, and returned playable video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WeryAI API key and sends prompts or public image URLs to WeryAI.

Mitigation: Install and run it only when that external API use is acceptable, keep WERYAI_API_KEY secret, and use a short-lived or isolated environment for higher assurance.

Risk: Successful wait-mode generations consume WeryAI credits.

Mitigation: Review the full confirmation table before approving generation and avoid repeated runs unless the parameters are correct.

Risk: Documentation and runtime behavior should be checked for the audio setting before production use.

Mitigation: Verify the confirmed generate_audio value against the submitted JSON command and WeryAI response before relying on output behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/hair-makeover-video)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zoucdr)
- [WeryAI Video Generation API Host](https://api.weryai.com)
- [WeryAI Model Registry API Host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include confirmation tables, generated CLI commands, error explanations, and playable video URLs returned by WeryAI.]

## Skill Version(s):

0.1.4 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
