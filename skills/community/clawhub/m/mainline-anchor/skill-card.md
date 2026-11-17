## Description:

Mainline Anchor provides a Chinese-language workflow prompt for keeping multi-agent work aligned with the main task after branch exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liucg3712](https://clawhub.ai/user/liucg3712)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and multi-agent teams use this skill to request a quick mainline-alignment status, classify active work as mainline, branch, or background, and steer branch exploration back to the main task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks agents to update HEARTBEAT.md at session exit, which could create unexpected workspace note changes.

Mitigation: Decide before use whether automatic HEARTBEAT.md updates are allowed; otherwise require agents to present the proposed status text and wait for approval before writing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liucg3712/skills/mainline-anchor)
- [ClawHub Publisher Profile](https://clawhub.ai/user/liucg3712)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown-formatted workflow status, task classification, next-step recommendations, and session handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language response template with a 30-minute branch-task check-in convention]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
