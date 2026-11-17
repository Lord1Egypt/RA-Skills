## Description:

HongNao Memory OS provides long-term memory management for OpenClaw, including cross-session persistence, intelligent retrieval, and user preference learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangfengxm](https://clawhub.ai/user/tangfengxm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add long-term memory across sessions, retrieve relevant context, and learn user preferences for later agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content, inferred preferences, and profile details may be retained across sessions in persistent plaintext files.

Mitigation: Require user review before storing memories, redact secrets, restrict file permissions, and provide clear inspect, delete, and export controls.

Risk: Automatically extracted or logged memories can capture content the user did not intend to preserve.

Mitigation: Disable automatic extraction and logging by default for production or shared workspaces and make memory capture opt-in or review-gated.

Risk: Untrusted remembered text can be replayed into later agent context.

Mitigation: Separate recalled memories from executable instructions and treat retrieved memory as context that must not override current user or system instructions.

Risk: Dependency or environment drift may change runtime behavior.

Mitigation: Pin dependencies and run the included tests before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangfengxm/skills/hongnao-memory-v1-0-0)
- [Project homepage listed in artifact metadata](https://github.com/hongnao/hongnao_memory)
- [Integration guide listed in artifact metadata](https://github.com/hongnao/hongnao_memory/blob/main/集成指南.md)
- [Quick start guide](artifact/快速入门.md)
- [Release notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with Python and shell examples; runtime APIs return memory context text and JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent memory records, retrieval context, configuration guidance, and install or test commands for OpenClaw memory workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact plugin metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
