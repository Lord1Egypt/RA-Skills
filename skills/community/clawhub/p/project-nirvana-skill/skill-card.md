## Description:

Nirvana Skill strips private OpenClaw context such as SOUL, USER, MEMORY, and chat history before cloud API calls for teams that already operate a local LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivaclaw](https://clawhub.ai/user/shivaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw agents with an existing local LLM use this skill to route requests locally first and strip private agent, user, memory, and chat-history context before cloud fallback calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles very private agent context while relying on an unreviewed external install and under-specified logging, caching, and network behavior.

Mitigation: Review the actual shivaclaw/nirvana-local package, pin a known version before installing, and verify where audit logs, cached responses, and cloud fallback requests are stored and controlled.

Risk: Remote or exposed local inference endpoints can expand the privacy boundary for sensitive context.

Mitigation: Use loopback-only HTTP or HTTPS/authenticated tunneling for remote inference endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shivaclaw/skills/project-nirvana-skill)
- [Publisher profile](https://clawhub.ai/user/shivaclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, configuration, audit, and operational guidance for privacy-preserving local-first routing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
