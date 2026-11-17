## Description:

Manages multiple independent agent work windows by creating local window records, saving summaries, and saving or restoring recent conversation history when switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philonis](https://clawhub.ai/user/philonis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to organize separate work threads, preserve per-window progress, and return to prior context without mixing unrelated conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation transcripts may include secrets or confidential content and are persisted in local window folders.

Mitigation: Use only where transcript persistence is acceptable, avoid sensitive chats, and redact or delete saved transcripts when needed.

Risk: The skill may save the wrong session's transcript into a window during switching.

Mitigation: Confirm the active window before switching and review saved transcript files; prefer explicit session binding before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philonis/skills/multi-windows)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and plain text status output with local JSON, Markdown, and JSONL files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists per-window metadata, summaries, and transcripts under the user's local OpenClaw workspace.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
