## Description:

pref0 learns user preferences from conversations and returns preference profiles that agents can use to personalize later responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fliellerjulian](https://clawhub.ai/user/fliellerjulian)

### License/Terms of Use:


## Use Case:

Developers and agent operators use pref0 to send conversation histories to the pref0 API, retrieve learned preference profiles, and apply structured preferences or validated personalization guidance across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversations and stable user identifiers may be sent to pref0, creating privacy and data-minimization risk.

Mitigation: Use only with informed user opt-in, prefer pseudonymous user IDs, and avoid sending secrets or sensitive conversations.

Risk: Returned prompt text may be applied as future instructions and could carry incorrect or unsafe personalization.

Mitigation: Render validated structured preferences where possible and review or constrain returned prompt text before adding it to system instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fliellerjulian/skills/pref0)
- [pref0 signup](https://pref0.com/signup)
- [pref0 API base URL](https://api.pref0.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PREF0_API_KEY and a user identifier; API responses include structured preferences, behavioral patterns, and optional prompt text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
