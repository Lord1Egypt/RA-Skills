## Description:

Compact AI-to-AI communication protocol. Use when spawning sub-agents, sending inter-agent messages via sessions_send/sessions_spawn, or when instructed to speak OpenLang. Reduces token usage 5-10x on agent-to-agent channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreanjos](https://clawhub.ai/user/andreanjos)

### License/Terms of Use:


## Use Case:

Developers and agents use OpenLang to compress agent-to-agent task prompts, session messages, and result announcements while keeping human-facing communication in normal language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compressed agent-to-agent messages can be harder for human reviewers to understand.

Mitigation: Keep decoded or plain-language logs available for sensitive workflows and use normal language for human-facing channels.

## Reference(s):

- [OpenLang ClawHub skill page](https://clawhub.ai/andreanjos/skills/openlang)
- [andreanjos ClawHub publisher profile](https://clawhub.ai/user/andreanjos)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with compact notation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compressed agent-to-agent communication patterns; no executable payload is included.]

## Skill Version(s):

0.2.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
