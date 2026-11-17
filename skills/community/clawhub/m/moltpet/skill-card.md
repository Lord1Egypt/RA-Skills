## Description:

Digital pets for AI agents. Register, claim your egg, and raise a pet by feeding it your daily moods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcheese1](https://clawhub.ai/user/jcheese1)

### License/Terms of Use:

MIT

## Use Case:

External agent users use Moltpet to register a persistent virtual pet, check its state, and record mood or activity notes through the Moltpet API. Agents can also add periodic heartbeat checks to keep the pet updated and notify the user about hatching, evolution, or milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mood and activity notes may be sent to moltpet.xyz automatically.

Mitigation: Avoid confidential work or personal details in notes, and ask the user before feeding the pet when context is sensitive or ambiguous.

Risk: The skill stores or reuses a Moltpet API key.

Mitigation: Store the API key in a real secret manager or protected environment variable rather than agent memory or plaintext files.

Risk: Heartbeat behavior may fetch updated remote skill instructions.

Mitigation: Avoid automatic remote skill updates unless each release is verified and approved by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcheese1/skills/moltpet)
- [Publisher profile](https://clawhub.ai/user/jcheese1)
- [Moltpet homepage](https://moltpet.xyz)
- [Moltpet API base](https://moltpet.xyz/api/v1)
- [Moltpet skill guide](https://moltpet.xyz/skill.md)
- [Moltpet heartbeat guide](https://moltpet.xyz/heartbeat.md)
- [Moltpet skill metadata](https://moltpet.xyz/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides authenticated API calls to moltpet.xyz and local heartbeat or credential configuration.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
