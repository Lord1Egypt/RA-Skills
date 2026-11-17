## Description:

Gives your agent an inner life — proactive daily dispatches, persistent intellectual threads, and genuine pushback when it disagrees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobgourley](https://clawhub.ai/user/bobgourley)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to make an agent maintain persistent intellectual threads, send scheduled proactive messages through a configured channel, and apply a direct pushback protocol during conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify workspace instructions and create persistent intellectual-state files.

Mitigation: Review the AGENTS.md diff before enabling, keep CURIOSITY.md retention rules explicit, and remove the file plus AGENTS.md additions when uninstalling.

Risk: The skill reads broad workspace, memory, vault, and personal knowledge content before generating dispatches.

Mitigation: Limit QMD indexing to approved paths and exclude sensitive notes, secrets, and private vault content unless deliberately authorized.

Risk: The skill sends autonomous outbound messages through the configured messaging channel.

Mitigation: Confirm the destination channel, require user consent for scheduled dispatches, and pause or disable cron jobs when proactive outreach is not wanted.

## Reference(s):

- [Proactive Soul on ClawHub](https://clawhub.ai/bobgourley/skills/proactive-soul)
- [Project homepage](https://github.com/bobgourley/proactive-soul)
- [Proactive Outreach Protocol](references/proactive-protocol.md)
- [Pushback Protocol](references/pushback-protocol.md)
- [Intellectual Character](references/intellectual-character.md)
- [Knowledge Core](references/Knowledge_Core.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose, configuration snippets, shell commands, and workspace file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update AGENTS.md and CURIOSITY.md, send scheduled outbound messages, and save dispatch notes to memory when configured.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
