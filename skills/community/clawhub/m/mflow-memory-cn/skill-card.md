## Description:

Provides a Chinese-language long-term memory engine for agents, adding emotion-aware memory storage, commitment tracking, relationship context, timing guidance, and preference inference on top of M-flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add Chinese-language long-term memory behavior to an agent, including recall of user preferences, emotion and relationship context, commitment reminders, and response-timing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain personal conversation content, emotions, commitments, relationship metadata, and inferred preferences in readable local files.

Mitigation: Use only with explicit user consent, define retention and deletion practices before deployment, and consider filesystem encryption or another protected storage layer for sensitive profiles.

Risk: The parent mflow-memory setup path is unpinned and should be reviewed before execution.

Mitigation: Inspect and pin the parent setup source before running installation commands in a production or shared environment.

Risk: Limited user controls for memory retention can lead to over-retention or unwanted recall of sensitive context.

Mitigation: Add opt-in capture, review, prune, and delete workflows before using the skill with real user data.

## Reference(s):

- [M-flow homepage](https://github.com/FlowElement-ai/m_flow)
- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/skills/mflow-memory-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, Python API examples, shell commands, and structured dictionary-style analysis outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSONL files under ~/.mflow-memory-cn/ for memory, promise, relationship, and wisdom data.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
