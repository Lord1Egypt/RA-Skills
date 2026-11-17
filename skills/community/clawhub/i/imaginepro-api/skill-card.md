## Description:

Generate AI images via ImaginePro API (Midjourney, Flux, Nano Banana, Lumi Girl, video).

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:


## Use Case:

Developers and AI coding agents use this skill to generate, edit, upscale, and track images or videos through the ImaginePro API from shell commands or JSON-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, image URLs, frame URLs, task metadata, and the ImaginePro API key to ImaginePro API endpoints.

Mitigation: Use only approved prompts and image URLs, keep IMAGINEPRO_API_KEY in the environment rather than hard-coding it, and avoid sending confidential or restricted content.

Risk: Most generation and post-processing operations consume paid ImaginePro credits.

Mitigation: Check credit balance and pricing before batch or repeated generation, and prefer low-volume test runs before larger jobs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iamzifei/skills/imaginepro-api)
- [ImaginePro AI Agent Skill Documentation](https://platform.imaginepro.ai/ai-agent-skill)
- [ImaginePro API Key Setup](https://platform.imaginepro.ai/dashboard/setup)
- [ImaginePro Pricing](https://platform.imaginepro.ai/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can return pretty-printed or compact JSON containing task IDs, status, result URLs, model data, or errors.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
