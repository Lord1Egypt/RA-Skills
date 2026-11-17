## Description:

Generate images via Krea.ai API (Flux, Imagen, Ideogram, Seedream, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fossilizedcarlos](https://clawhub.ai/user/fossilizedcarlos)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate images through Krea.ai models from an agent workflow, command line, or Python script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Krea.ai API credentials can be exposed through command-line arguments, shell history, logs, or insecure credential-file handling.

Mitigation: Prefer the credential file at ~/.openclaw/credentials/krea.json with chmod 600 permissions, avoid passing --secret in shared shells, and rotate the Krea key if it may have been exposed.

Risk: Prompts and generation parameters are sent to Krea.ai for image generation.

Mitigation: Avoid sending confidential or regulated information in prompts unless the deployment has approved Krea.ai for that data.

## Reference(s):

- [Krea.ai API keys and billing documentation](https://docs.krea.ai/developers/api-keys-and-billing)
- [Krea.ai usage statistics dashboard](https://www.krea.ai/settings/usage-statistics)
- [Krea.ai API service](https://api.krea.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, Python API guidance, and generated image URL output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill performs authenticated Krea.ai API calls and can list models, submit image-generation jobs, poll job status, and return generated image URLs.]

## Skill Version(s):

0.2.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
