## Description:

Generates videos with MiniMax Hailuo using text prompts, image-to-video, start/end frames, or subject-reference inputs, with MINIMAX_API_KEY supplied by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to ask an agent for MiniMax Hailuo video-generation commands and configuration guidance across text, image, start/end-frame, and subject-reference workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and face-reference URLs may be sent to MiniMax during video generation.

Mitigation: Avoid sensitive prompts or images, and use subject-reference or face images only with appropriate permission.

Risk: API-key documentation is inconsistent about embedded credentials versus user-provided credentials.

Mitigation: Set your own MINIMAX_API_KEY environment variable and do not rely on an embedded key.

Risk: Running dependency installation in a shared environment can affect other Python projects.

Mitigation: Install requests and run the script in an isolated Python environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skydream9527-ctrl/skills/hailuo-gyh)
- [MiniMax platform](https://platform.minimax.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated video file paths when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, requests, and a user-provided MINIMAX_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
