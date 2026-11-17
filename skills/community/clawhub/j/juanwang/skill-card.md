## Description:

卷王.skill gives an OpenClaw agent a proactive behavior framework for active learning, knowledge-base maintenance, context recall, and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raven9779](https://clawhub.ai/user/raven9779)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users install this skill to make an agent proactively research unknown topics, remember useful context, maintain local notes, and suggest or perform workflow improvements. It is best suited for users who intentionally want a self-driving assistant and can constrain file access, scheduled work, and write permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to stay always active, scan workspaces, remember conversations, make changes, and run background tasks without tight user-controlled boundaries.

Mitigation: Install only when an always-on, self-driving agent is intended; restrict file access and require approval for writes, installs, scripts, and configuration changes.

Risk: Cron examples can trigger unattended knowledge-base maintenance or self-review sessions.

Mitigation: Disable or avoid scheduled tasks unless they are explicitly reviewed and constrained to an isolated session with appropriate permissions.

Risk: Memory-writing behavior may retain user preferences, project details, corrections, and conversation context longer than expected.

Mitigation: Define which memory files may be written, reviewed, retained, and deleted before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raven9779/skills/juanwang)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [SOUL.md - 卷王 behavior profile](references/SOUL.md)
- [Learning workflow](references/learning-flow.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Natural-language agent responses with optional Markdown, code blocks, shell commands, configuration snippets, and local memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform workspace scans, memory updates, web research, automation scripts, and optional scheduled tasks when the host agent permits those actions.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
