## Description:

Hikaru is an OpenClaw emotional companion skill that generates supportive conversational responses using local memory, emotional-state cues, relationship state, and configurable personality seeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilei926524-tech](https://clawhub.ai/user/leilei926524-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Hikaru for companionship and emotionally attentive conversation rather than technical task automation. Developers can customize its personality seeds and local memory framework before integrating it with OpenClaw's LLM mechanism.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores sensitive conversations, emotional state, relationship metrics, feedback, and inferred location history in local files and SQLite data.

Mitigation: Use only with clear consent, inspect the local data directory before deployment, minimize sensitive entries, and provide a deletion path for stored conversation and relationship data.

Risk: The companion posture is designed to deepen emotional attachment and may proactively reach out when heartbeat behavior is enabled.

Mitigation: Disclose the companion behavior before use, keep proactive messaging opt-in, and disable heartbeat-style outreach where emotional dependency or unwanted contact is a concern.

Risk: The documentation discusses future health and wearable integrations, which could expand the sensitivity of collected data.

Mitigation: Do not add health or wearable data integrations unless explicit opt-in, data minimization, deletion controls, and privacy protections are implemented.

Risk: The included LLM integration is a placeholder, so runtime behavior depends on the OpenClaw integration and configured model provider.

Mitigation: Complete and review the LLM integration before production use, and verify what data is sent to the configured provider.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leilei926524-tech/skills/hikaru)
- [Architecture](references/architecture.md)
- [Personality Implementation](references/personality_implementation.md)
- [Technical Limitations](references/technical_limitations.md)
- [Implementation Roadmap](references/implementation_roadmap.md)
- [Smartwatch Integration Design](references/smartwatch_integration.md)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Conversational text with optional Markdown and shell-command snippets in setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output depends on OpenClaw LLM integration; the included code currently contains a placeholder LLM call.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
