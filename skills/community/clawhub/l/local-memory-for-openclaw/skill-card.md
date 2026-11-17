## Description:

Manages local AI conversation memory for OpenClaw by extracting, storing, retrieving, and injecting relevant memories without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellofsf](https://clawhub.ai/user/hellofsf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual OpenClaw users use this skill to keep local conversation memory across chats. It extracts facts, preferences, project progress, and to-dos; stores them locally; retrieves relevant memories; and supports manual save, recall, delete, and list commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores conversation content, which may include sensitive details.

Mitigation: Use it in a single-user, non-sensitive environment, avoid storing secrets, and review the local database regularly.

Risk: Memories may be reused across chats with weak user, session, or topic scoping.

Mitigation: Prefer explicit manual memory commands for important facts, remove outdated memories, and disable automatic extraction or injection when broad reuse is not appropriate.

Risk: Injected memories can introduce stale, irrelevant, or sensitive context into later conversations.

Mitigation: Review retrieved memories before relying on them and periodically delete irrelevant or sensitive entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellofsf/skills/local-memory-for-openclaw)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON event payloads containing text replies or injected memory context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and retrieves local SQLite memories; no external API is required.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
