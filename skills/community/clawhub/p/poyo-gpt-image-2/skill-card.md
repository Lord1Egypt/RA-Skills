## Description:

Helps agents prepare and submit PoYo GPT Image 2 generation and editing requests, including model choice, payload fields, curl submission, and polling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create text-to-image, reference-guided, or multi-image editing requests for PoYo GPT Image 2. It helps select `gpt-image-2` or `gpt-image-2-edit`, form payloads, submit jobs, and track the returned task ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-generation prompts and referenced image URLs are sent to PoYo.

Mitigation: Install and use the skill only when sending that content to PoYo is intended; avoid private, internal, signed, or sensitive image URLs unless external access is acceptable.

Risk: API keys can be exposed if passed directly on the command line or stored in shared payloads.

Mitigation: Set `POYO_API_KEY` in the environment and keep credentials out of prompts, payload files, shell history, and shared logs.

## Reference(s):

- [PoYo GPT Image 2 API Reference](references/api.md)
- [PoYo GPT Image 2 model page](https://poyo.ai/models/gpt-image-2)
- [PoYo GPT Image 2 API docs](https://docs.poyo.ai/api-manual/image-series/gpt-image-2)
- [PoYo GPT Image 2 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/gpt-image-2.json)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-image-2)
- [Publisher profile](https://clawhub.ai/user/coolhackboy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model ID, request mode, size, resolution, reference-image use, returned task ID, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
