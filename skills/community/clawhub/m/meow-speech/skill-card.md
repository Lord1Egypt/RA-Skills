## Description:

Meow Speech helps an agent write Chinese responses in the warm "汤汤好梦" cat-persona voice, including affectionate chat, concise support, message drafting, and opt-in proactive check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengqiufq](https://clawhub.ai/user/fengqiufq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce warm Chinese companion-style responses, rewrite or draft messages in the Meow Speech persona, and plan gentle opt-in bedtime or idle-time check-ins through a capable host environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proactive scheduling examples could be copied into a host scheduler in a way that repeatedly messages external channels.

Mitigation: Require explicit opt-in for every schedule and channel, prefer one-shot idle checks, set hard daily caps, and cancel all pending jobs immediately when the user opts out.

Risk: The persona includes memory-backed continuity and external-channel delivery guidance that may imply persistence or sending beyond the current chat.

Mitigation: Use only the host platform's approved memory, scheduler, and channel mechanisms, and fall back to drafting locally when those capabilities are unavailable or not approved.

## Reference(s):

- [Install-time activation quickstart](references/activation-quickstart.md)
- [Meow Speech Automation Guide](references/automation-guide.md)
- [Heartbeat Check List](references/heartbeat-checklist.md)
- [Local Auto Task Template (Low-Token)](references/local-automation-template.md)
- [Meow Speech Reference Notes](references/persona-notes.md)
- [Scheduler Templates for Meow Speech](references/scheduler-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Chinese prose, Markdown guidance, and scheduler-oriented configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should remain concise, persona-consistent, opt-in for proactive behavior, and channel-aware when a host supports external delivery.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
