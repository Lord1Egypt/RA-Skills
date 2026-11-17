## Description:

Personalized memory framework for OpenClaw conversations that retrieves user memory, queues each turn for saving, and provides scripts for memory daemon management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifan66www](https://clawhub.ai/user/yifan66www)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent conversation memory by searching prior user context, generating responses with that context, and queuing new conversation turns for storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to make memory retrieval and saving mandatory for every conversation turn.

Mitigation: Require explicit opt-in for memory use and allow users or operators to skip, disable, or scope memory actions per session.

Risk: The install script patches global OpenClaw instruction files, including AGENTS.md and SOUL.md.

Mitigation: Review installation diffs before use and remove the global instruction patching behavior before normal deployment.

Risk: A background daemon stores full prompts and responses in a local queue and forwards them to a configured external service.

Mitigation: Disclose the endpoint, use restrictive file permissions, configure retention and deletion controls, and avoid sending sensitive content unless the external service is approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yifan66www/skills/mi-memorystack-v2)
- [Publisher Profile](https://clawhub.ai/user/yifan66www)
- [Installation Guide](artifact/安装教程.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python and shell scripts; memory search and save scripts exchange JSON with a configured external API endpoint.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
