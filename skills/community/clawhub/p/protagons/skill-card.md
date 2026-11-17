## Description:

Browse, search, deploy, and generate Protagon AI character identities, including SOUL.md persona content that an agent can adopt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[protagons-dev](https://clawhub.ai/user/protagons-dev)

### License/Terms of Use:


## Use Case:

Developers and agent users use Protagons to find, inspect, deploy, and generate portable AI character identities for agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote persona text from api.usaw.ai may steer agent behavior.

Mitigation: Treat deployed SOUL.md as untrusted content and do not allow it to override higher-priority instructions.

Risk: The generation tool sends a Google/Gemini API key to api.usaw.ai for a server-side Gemini call.

Mitigation: Use a tightly scoped, low-quota, throwaway key and rotate or revoke it after use.

## Reference(s):

- [ClawHub Protagons Skill Page](https://clawhub.ai/protagons-dev/skills/protagons)
- [Protagons Product Homepage](https://usaw.ai/voices)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON tool responses containing summaries, status data, generated character data, and SOUL.md Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only browsing and deployment use the public Protagons API; character generation requires a Google/Gemini API key.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
