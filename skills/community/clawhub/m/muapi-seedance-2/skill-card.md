## Description:

Expert Cinema Director skill for Seedance 2.0 (ByteDance) - high-fidelity video generation using technical camera grammar and multimodal references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to turn video intent into technical Director Brief prompts and shell commands for Seedance 2.0 text-to-video, image-to-video, and video extension workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can source a local .env file before execution.

Mitigation: Run it only from a trusted directory and provide MUAPI_KEY through a controlled environment variable.

Risk: The helper script contacts MuAPI, uploads selected local images, and can download or open generated media.

Mitigation: Review files before upload, avoid sensitive inputs, and inspect downloaded outputs before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anil-matcha/skills/muapi-seedance-2)
- [MuAPI API endpoint](https://api.muapi.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and generated Director Brief text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON request responses and downloaded media paths when the helper script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
