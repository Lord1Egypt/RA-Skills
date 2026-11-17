## Description:

Reads indexed memory segments on demand based on trigger scenarios, prioritizing context rebuilding and controlled partial retrieval up to 50KB per request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to decide when and how to retrieve indexed memory, recent daily reports, project progress notes, shared knowledge, or explicitly requested archived chat fragments while rebuilding or extending conversational context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to access private work logs, progress reports, or archived chats.

Mitigation: Install it only where accessible memory directories are already limited to data the current user is allowed to read.

Risk: Cold chat retrieval is sensitive and may expose private historical conversation content.

Mitigation: Require explicit scope and consent before cold chat retrieval, and keep the documented 50KB per-read limit.

Risk: Vague conversational triggers may cause broader memory lookup than intended.

Mitigation: Start retrieval from indexes, read only what the current task needs, and avoid proactive cold archive reads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/memory-read)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance with retrieval rules and trigger scenarios]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory retrieval is scoped by trigger scenario, starts from indexes, and limits cold chat retrieval to explicit requests of up to 50KB per read.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
