## Description:

AI image and video generation via Vydra.ai API. Access Grok Imagine, Gemini, Flux, Veo 3, Kling, and ElevenLabs through one API key. Agents can self-register and generate images automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoafsystems](https://clawhub.ai/user/shoafsystems)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call the Vydra API for image generation, video generation, image editing, voice synthesis, credit checks, and billing-related workflows. It is intended for users who already have or can obtain a Vydra API key and are comfortable sending prompts, media URLs, and account details to Vydra.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, media URLs, account details, and billing email addresses to Vydra.

Mitigation: Review requests before sending them and avoid including confidential, regulated, or unnecessary personal data.

Risk: Documented workflows can create accounts, initiate billing, buy credits, or spend paid credits with a Vydra API key.

Mitigation: Require explicit human approval for registration, billing, credit purchase, and high-cost generation actions.

Risk: The artifact documents storing a paid API key in a plaintext credentials file.

Mitigation: Prefer the VYDRA_API_KEY environment variable or a managed secret store, and restrict access to any local credential files.

Risk: The artifact suggests fetching a live remote skill.md that can change after review.

Mitigation: Do not treat live remote skill content as trusted instructions unless it has been separately reviewed for the intended release.

## Reference(s):

- [Vydra API Documentation](references/api-docs.md)
- [Vydra Homepage](https://vydra.ai)
- [ClawHub Skill Page](https://clawhub.ai/shoafsystems/skills/image-and-video-generation-vydra)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown with inline bash, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce prompts and API request examples that spend Vydra credits or initiate account and billing flows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
