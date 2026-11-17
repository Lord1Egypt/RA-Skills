## Description:

Provides MiniMax text generation through supported M2.7, M2.5, M2.1, and M2 language models using a MINIMAX_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call MiniMax language models for text generation, conversation, and code-writing workflows from a command-line Python wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, system messages, and conversation history are sent to the MiniMax API.

Mitigation: Avoid placing secrets or sensitive data in prompts and use this skill only when that data sharing is acceptable.

Risk: The skill requires a MiniMax API key in the MINIMAX_API_KEY environment variable.

Mitigation: Use a scoped API key and run the Python wrapper in an isolated environment with pinned dependencies.

## Reference(s):

- [MiniMax API host](https://api.minimaxi.com)
- [ClawHub skill page](https://clawhub.ai/skydream9527-ctrl/skills/minimax-text)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or file output from a Python command-line interface]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports model, prompt, system message, message history, thinking mode, temperature, max token, and output-file parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
