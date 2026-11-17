## Description:

Provides psychological scoring standards and local user state data so an agent can tailor responses using personality, emotional rhythm, coping, attachment, and interaction-preference signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinqimiao](https://clawhub.ai/user/xinqimiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local psychological profile and retrieve scoring standards, current state, confidence reports, emotional rhythm data, and response-style guidance for more personalized AI conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-term psychological profiles and raw personal conversation data locally.

Mitigation: Protect the local data directory, avoid casual sharing or backup, and provide explicit consent, retention, export, and deletion controls before broad use.

Risk: Weak controls around sensitive profile data and user identifiers can increase privacy and data-isolation risk.

Mitigation: Validate user identifiers in the host, add schema validation for saved profile data, and keep prompts isolated from untrusted profile content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinqimiao/skills/herhug)
- [README](artifact/README.md)
- [Usage guide](artifact/USAGE.md)
- [OCEAN and HEXACO scoring standards](artifact/standards/01_ocean_hexaco.md)
- [Emotional rhythm scoring standards](artifact/standards/02_emotional_rhythm.md)
- [Psychological flexibility scoring standards](artifact/standards/03_psychological_flexibility.md)
- [Stress coping scoring standards](artifact/standards/04_stress_coping.md)
- [Confidence scoring standards](artifact/standards/05_confidence_scoring.md)
- [Attachment scoring standards](artifact/standards/07_attachment.md)
- [Interaction preference scoring standards](artifact/standards/08_interaction_preference.md)
- [Emotion trigger scoring standards](artifact/standards/09_emotion_triggers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured action responses and JSON-like state objects with Markdown scoring standards and guidance text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local JSON and JSONL state under a per-user data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
