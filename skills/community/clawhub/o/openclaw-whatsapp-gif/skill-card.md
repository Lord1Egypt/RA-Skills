## Description:

Source and send relevant reaction GIFs in WhatsApp chats using safe filters and deterministic ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[witty-quotes25](https://clawhub.ai/user/witty-quotes25)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to choose one context-appropriate reaction GIF and prepare it for a WhatsApp chat. It is intended for lightweight social responses such as celebration, humor, acknowledgment, empathy, or agreement, while avoiding serious or sensitive contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare or send WhatsApp messages to external recipients without an explicit confirmation step.

Mitigation: Require user confirmation and recipient verification before sending any GIF payload.

Risk: The skill downloads remote media and writes cached files to temporary storage.

Mitigation: Use the configured host allowlist and media size/type checks, and harden or isolate the temp cache before shared or higher-risk use.

Risk: Optional web scraping, remote URL fallback, and telemetry logging increase sourcing, delivery, or privacy exposure if enabled.

Mitigation: Keep these policy options disabled unless the deployment explicitly accepts those risks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/witty-quotes25/skills/openclaw-whatsapp-gif)
- [Provider notes](references/providers.md)
- [Runtime policy](references/policy.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON message payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a WhatsApp send payload, a ranked GIF candidate list, a local cached media file path, or concise fallback text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
