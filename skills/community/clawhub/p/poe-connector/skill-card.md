## Description:

Connects an agent to Poe.com models for text chat, multimodal file input, media generation, and model discovery through Poe's OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzwalker](https://clawhub.ai/user/dzwalker)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to route chat, image, video, audio, and model-discovery requests through Poe from an OpenClaw environment. It is useful when an agent needs Poe-hosted models through shell commands and an existing Poe API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and explicitly attached files are sent to Poe and downstream model providers.

Mitigation: Do not attach secrets, private documents, or regulated data unless approved for Poe and the selected provider.

Risk: Generated media handling automatically downloads model-supplied URLs and writes them locally without sufficient limits or validation.

Mitigation: Run in a constrained environment and require explicit confirmation, trusted host allowlists, and strict size and content limits before downloading media.

Risk: The release depends on the openai Python package at a broad version range.

Mitigation: Pin and review the openai dependency before deployment.

## Reference(s):

- [ClawHub Poe Connector Skill Page](https://clawhub.ai/dzwalker/skills/poe-connector)
- [Poe](https://poe.com)
- [Poe API Keys](https://poe.com/api/keys)
- [Poe OpenAI-Compatible API Endpoint](https://api.poe.com/v1)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Configuration guidance]

**Output Format:** [CLI text output, streamed text responses, JSON model listings, and local media files with handoff hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, bash, the openai Python package, and a configured POE_API_KEY. Generated media may be saved locally for delivery through the agent's message tool.]

## Skill Version(s):

1.1.0 (source: server release evidence, SKILL.md frontmatter, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
