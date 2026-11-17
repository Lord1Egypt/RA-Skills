## Description:

Call a local llama.cpp server with the LLaVA model to analyze images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[447992399](https://clawhub.ai/user/447992399)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send a local image path or remote image URL to a locally running LLaVA model served by llama.cpp and receive a text description of the image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local file paths supplied to it.

Mitigation: Use trusted image files, avoid sensitive paths, and run the skill with filesystem restrictions where possible.

Risk: The skill can fetch arbitrary remote image URLs from the user's machine.

Mitigation: Use trusted URLs and run in a network-restricted environment when reviewing or deploying the skill.

Risk: The skill depends on a local llama.cpp server for image analysis.

Mitigation: Confirm the local server endpoint and model are expected before use, and treat connection failures as operational errors rather than model output.

## Reference(s):

- [Llava Vision ClawHub listing](https://clawhub.ai/447992399/skills/llava-vision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Text response with optional command-line status and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable local llama.cpp server and image input as a file path or URL.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
