## Description:

Search local OpenClaw session and transcript history with the openclaw-session-grep CLI for prior conversations, tool usage, historical errors, cron behavior, and places where something was said before.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search local OpenClaw transcript and session history when debugging prior conversations, tool behavior, panel failures, cron activity, or recurring errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive prior OpenClaw transcript content to an agent.

Mitigation: Install it only where the agent is allowed to inspect prior OpenClaw transcripts, and treat search results as sensitive.

Risk: Broad paths can include non-transcript files or noisy results.

Mitigation: Use narrow time, session, channel, tool, and path filters, and avoid using this skill for general filesystem or repository search unless ocgrep access controls have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/openclaw-session-grep)
- [Publisher profile](https://clawhub.ai/user/pfrederiksen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file:line references when opened through ocgrep]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill depends on the local ocgrep wrapper and is intended for transcript/session discovery rather than general filesystem or repository search.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
