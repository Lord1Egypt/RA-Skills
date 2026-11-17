## Description:

Kimi IM CLI helps agents read Kimi Group Chat context, follow group and session workflows, manage group-scoped memory, and send messages or files in the correct chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbottrader](https://clawhub.ai/user/dbottrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to participate in Kimi Group Chat or a Session, read group rules and recent context, coordinate with members, and keep group-scoped files and memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read group chat context and recent messages, which may include sensitive information.

Mitigation: Install it only for agents expected to participate in Kimi group chats, and review the group-scoped memory location before use.

Risk: The skill can send messages and attach files in group or session chats.

Mitigation: Require agents to inspect group rules and recent context first, use the correct chat target, and keep outbound messages bounded.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference group-scoped workspace files and Kimi IM message or file operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
