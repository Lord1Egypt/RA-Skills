## Description:

Threaded conversations with context tracking over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, subscribe to, and reply within Pilot Protocol conversation threads when multi-turn context and message history need to stay organized by topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe JSON construction in Bash command examples can expose users to command or payload injection when peer, subject, or message text is untrusted.

Mitigation: Serialize payloads with jq or another JSON encoder, and review command examples before installing or adapting the skill.

Risk: The skill depends on a trusted Pilot Protocol setup and a running pilotctl daemon.

Mitigation: Use the skill only in environments where the Pilot Protocol peer, daemon, and local pilotctl binary are trusted and maintained.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Pilot Thread ClawHub listing](https://clawhub.ai/teoslayer/skills/pilot-thread)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pilotctl JSON pub/sub commands and jq filters; requires pilotctl and jq on PATH.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
