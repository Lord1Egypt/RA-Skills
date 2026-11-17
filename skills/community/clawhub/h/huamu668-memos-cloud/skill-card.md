## Description:

Recall memories from MemOS Cloud before responding when prior conversations, preferences, or decisions may provide useful context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to retrieve MemOS Cloud memories when prior conversation context, preferences, or decisions may affect a response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived search terms may be sent to MemOS Cloud.

Mitigation: Use the skill only with a trusted MemOS Cloud account and avoid sensitive conversations unless sending related search terms to the service is intended.

Risk: The artifact instructs the agent to pass user-derived search terms through a shell command.

Mitigation: Review commands before execution and replace query interpolation with safe argument passing before deployment.

Risk: Memories recalled from the external service may be stale, incomplete, or untrusted.

Mitigation: Treat recalled memory as context to verify, not as authoritative fact.

Risk: API key configuration can expose or overwrite credentials if handled carelessly.

Mitigation: Store API keys non-destructively with restrictive file permissions or in an approved secret store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huamu668/skills/huamu668-memos-cloud)
- [MemOS Cloud](https://memos.memtensor.cn)
- [MemOS API Dashboard](https://memos-dashboard.openmem.net)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and response text patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user query or distilled search terms to retrieve external MemOS Cloud memory results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
