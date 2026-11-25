## Description:

Energy-aware proactive nudging for OpenClaw. Analyzes a bounded window of your direct messages plus files you explicitly opt into via CONTEXT_SOURCES; all state stays local, nothing is transmitted, and the skill stays inert until you consent. Use /pulse to inspect, correct, or disable it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adnxone](https://clawhub.ai/user/adnxone)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can opt into bounded local analysis of recent direct messages and explicitly selected context files to receive capacity-aware task suggestions, adjust how the agent nudges them, and review or delete local state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and noted a possible mismatch involving an update command, along with lower-level memory and scope alerts.

Mitigation: Before enabling the skill, review the reported update command and state-file references; opt in deliberately and limit message scope and CONTEXT_SOURCES to what you intend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adnxone/skills/nxt-pulse-agent)
- [Project homepage](https://github.com/adnxone/nxt-pulse-agent)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions]

**Output Format:** [In-chat text and guidance, with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proactive suggestions are gated by consent, confidence, scope, quiet hours, and cooldown; insufficient evidence results in no nudge.]

## Skill Version(s):

0.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
