## Description:

Routes local mflux image-generation requests across Apple Silicon devices so agents can generate PNG images with Z-Image-Turbo, Flux Dev, or Flux Schnell while balancing fleet load.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to install and call a local fleet router for mflux image generation, choose generation parameters, monitor image-generation activity, and save generated PNG outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches broader fleet API use beyond its stated image-generation purpose.

Mitigation: Review non-image API examples before use and avoid sending sensitive text, audio, or prompts through those APIs unless that broader use is intended.

Risk: The workflow starts a local fleet router and exposes documented local HTTP APIs on port 11435.

Mitigation: Run the router only in a trusted local environment and review network exposure before allowing other devices to connect.

Risk: The workflow installs and uses current releases of ollama-herd and mflux.

Mitigation: Install only from trusted package sources and pin or review package versions when deployment reproducibility matters.

Risk: mflux model operations can involve large downloads and generated image files.

Mitigation: Require explicit confirmation before pulling or deleting models and before deleting or modifying generated image files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/mflux-image-router)
- [ollama-herd Package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, JavaScript, curl examples, and API parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, starting a local router on port 11435, calling local HTTP APIs, and writing PNG image outputs.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
