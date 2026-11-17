## Description:

Generate images through the Nano Banana REST API and help agents list models, check credits, choose request modes, poll jobs, and produce reproducible API calls or scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdhjkagbjksg](https://clawhub.ai/user/sdhjkagbjksg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate and edit images through Nano Banana, inspect available models and credits, choose sync, stream, or async execution, and poll or download generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may send prompts, reference image URLs, and generated-image requests to Nano Banana.

Mitigation: Use the skill only when sharing that content with Nano Banana is acceptable for the task and data policy.

Risk: An undocumented endpoint override can redirect API-key-authenticated requests to another server if the environment is tampered with.

Mitigation: Ensure NANO_BANANA_BASE_URL is unset or points only to a trusted endpoint before use.

Risk: API keys can be exposed if passed through command history or printed in outputs.

Mitigation: Keep the API key in NANO_BANANA_API_KEY or NB_API_KEY and do not print or restate the raw key.

Risk: Generated files may be written to an unexpected location when downloads are enabled.

Mitigation: Use --download-dir only for directories where generated image files are expected.

## Reference(s):

- [Nano Banana API Reference](references/api-reference.md)
- [Nano Banana Official Website](https://www.nananobanana.com)
- [ClawHub Skill Page](https://clawhub.ai/sdhjkagbjksg/skills/nano-banana-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON API responses, and optional downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Nano Banana API, emit JSON responses, and save generated images when a download directory is requested.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
