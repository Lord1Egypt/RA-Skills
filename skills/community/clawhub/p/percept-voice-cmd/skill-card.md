## Description:

Detects wake words in speech and routes voice commands like email, text, reminders, search, and notes to OpenClaw agents for execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to enable hands-free OpenClaw control from approved speakers, routing wake-word commands to email, text, reminders, search, calendar, notes, or custom agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambient speech and broad default wake phrases can trigger real OpenClaw actions.

Mitigation: Replace common wake words with a unique phrase, approve only trusted speakers, and review wake-word behavior before enabling the skill.

Risk: Voice commands can initiate sensitive actions such as email, text, calendar, credential-related notes, or custom OpenClaw CLI actions.

Mitigation: Require confirmation for sensitive or custom actions and limit approved speakers to trusted users.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jarvis563/skills/percept-voice-cmd)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with voice-command routing, CLI dispatch, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires percept-listen, OpenClaw CLI access, configured wake words, contacts, and approved speakers.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
