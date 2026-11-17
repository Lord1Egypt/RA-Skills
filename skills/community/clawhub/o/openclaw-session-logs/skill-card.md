## Description:

Search and analyze past OpenClaw session logs stored in JSONL files to retrieve prior conversation details and historical context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronmda](https://clawhub.ai/user/aaronmda)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to locate prior conversations, extract readable messages, summarize costs, and inspect tool usage from local session JSONL logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read complete local OpenClaw session transcripts, which can contain secrets or personal information.

Mitigation: Scope requests to a specific session, date, or phrase, and review or redact sensitive content before sharing results.

Risk: Broad all-session searches can expose more historical conversation content than intended.

Mitigation: Use narrow searches first and avoid raw transcript display unless it is needed for the task.

## Reference(s):

- [ClawHub skill page: OpenClaw Session Logs](https://clawhub.ai/aaronmda/skills/openclaw-session-logs)
- [ClawHub publisher profile: aaronmda](https://clawhub.ai/user/aaronmda)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local OpenClaw session JSONL files selected by agent id, session id, date, or phrase.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
