## Description:

Search past session transcripts to recover lost conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hchen13](https://clawhub.ai/user/hchen13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to find prior session context when users refer to earlier conversations, then read targeted transcript lines before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search local OpenClaw transcript history and expose sensitive snippets or file paths.

Mitigation: Use narrow agent and time-window filters, review returned snippets before using them, and avoid sharing transcript content that may contain secrets or private context.

Risk: Omitting an agent filter can broaden recall across available agents' session histories.

Mitigation: Prefer the current agent with --agent and use all-agent searches only when cross-agent recall is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hchen13/skills/openclaw-session-recall)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with file paths, line numbers, snippets, and session summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports agent, time-window, limit, and offset filters for targeted transcript recall.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
