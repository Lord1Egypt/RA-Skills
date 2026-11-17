## Description:

Guided self-reflection and introspection skill for exploring the past, clarifying core values, processing life decisions, and optionally using Wisdom Sage Mode with insights from Buffett, Duan Yongping, and Munger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slientrain-new](https://clawhub.ai/user/slientrain-new)

### License/Terms of Use:

MIT-0

## Use Case:

Users and assistants use this skill for guided personal reflection, life-story exploration, value clarification, and decision processing through patient listening and gentle mirroring. It can also produce structured Markdown session summaries and timeline notes when a conversation closes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store detailed personal life history, names, places, emotions, and session summaries in local plaintext files.

Mitigation: Use it only in protected environments and review storage, retention, deletion, encryption, and per-user isolation expectations before deployment.

Risk: Personal reflection sessions can include sensitive private information.

Mitigation: Avoid sharing passwords, tokens, private keys, or details that should not be stored or resurfaced later.

Risk: The skill presents itself as reflective support and is not a therapist or clinical tool.

Mitigation: Keep responses framed as listening and reflection, and do not rely on it for medical, mental-health, or emergency guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slientrain-new/skills/magicmirror)
- [Session stages reference](references/stages.md)
- [Conversation techniques reference](references/techniques.md)
- [Timeline schema](references/timeline-schema.json)
- [Session summary output format](references/session-output.md)
- [Success case reference](references/success-case.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text with optional Markdown session summaries and JSON timeline records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist personal timeline entries and session notes in local plaintext files]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
