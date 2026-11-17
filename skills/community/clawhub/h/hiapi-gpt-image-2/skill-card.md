## Description:

Generate or edit images with HiAPI's GPT Image 2 family through the HiAPI unified async task API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiapiai](https://clawhub.ai/user/hiapiai)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to generate or edit images with HiAPI's GPT Image 2 model family from natural-language prompts and optional reference image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and update workflows can run code from unpinned GitHub sources or place files in custom agent skill directories.

Mitigation: Review before installing, prefer a pinned commit or signed release, and avoid untrusted custom target paths or AGENT_SKILLS_DIR values.

Risk: A configurable API host can expose the HiAPI API key to an endpoint outside the normal service path.

Mitigation: Keep HIAPI_BASE_URL at https://api.hiapi.ai unless the alternate endpoint is fully controlled and trusted.

Risk: Printed update commands may ask the user to run additional package installation commands.

Mitigation: Treat printed update commands as untrusted until independently verified.

## Reference(s):

- [HiAPI GPT Image 2 API](references/api.md)
- [Output Handling](references/output.md)
- [HiAPI Docs](https://docs.hiapi.ai)
- [Awesome GPT Image 2 Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts)
- [ClawHub Skill Page](https://clawhub.ai/hiapiai/skills/hiapi-gpt-image-2)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [JSON containing task metadata and generated image file paths or remote URLs; failures return concise text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HIAPI_API_KEY; local data URI outputs are saved under outputs/ unless saving is disabled.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
