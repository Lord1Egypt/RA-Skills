## Description:

Compact the current conversation into a handoff document for another agent or fresh session to continue the work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilmych](https://clawhub.ai/user/ilmych)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create concise Markdown handoff notes when ending a long session, switching agents, or preserving context for a fresh session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A handoff summary may expose secrets, PII, or highly sensitive conversation details if those details are present in the session.

Mitigation: Redact secrets and PII before writing the handoff, review the generated file before sharing it, and delete the temporary file when it is no longer needed.

## Reference(s):

- [gstack Handoff on ClawHub](https://clawhub.ai/ilmych/skills/gstack-openclaw-handoff)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown handoff document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to save the handoff document to the OS temporary directory and report the absolute path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
