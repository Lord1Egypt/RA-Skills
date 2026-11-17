## Description:

Search and analyze your own session logs (older/parent conversations) using jq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search previous local conversation sessions, extract messages, inspect tool usage, and summarize session costs when a user asks about earlier context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad searches can expose private local conversation transcripts.

Mitigation: Use narrow dates, keywords, or known session IDs, and avoid broad searches across all sessions unless the requester is authorized to see the logs.

Risk: Installing the skill gives the agent direct read access to local conversation transcripts.

Mitigation: Install only in environments where that access is acceptable, and review retrieved excerpts before sharing or reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-session-logs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local access to session JSONL files and the jq and rg command-line tools.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
