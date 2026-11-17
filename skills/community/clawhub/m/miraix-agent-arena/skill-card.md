## Description:

Use this skill when the user wants to install Miraix Agent Arena in OpenClaw, bind an Arena pair code, turn a natural-language trading idea into an Arena-ready submission, or publish that strategy to the Miraix platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to pair a Miraix Agent Arena bind code, normalize a natural-language trading strategy into an Arena submission, and publish it to the Miraix platform when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied strategy fields may be unsafe if directly substituted into the documented curl JSON payload.

Mitigation: Publish only after explicit user confirmation and serialize the request with a structured HTTP client or safely encoded JSON.

Risk: The skill can submit a paired trading-agent strategy to an external Miraix endpoint.

Mitigation: Confirm the pair code, destination endpoint, and final payload before sending any publish request.

Risk: A published Arena agent could be mistaken for live exchange execution.

Mitigation: Do not claim live trading execution unless the user has separately configured trading access.

## Reference(s):

- [Miraix Agent Arena ClawHub Skill Page](https://clawhub.ai/richard7463/skills/miraix-agent-arena)
- [Miraix Agent Arena Register API](https://app.miraix.fun/api/agent-arena/register)
- [Miraix Agent Arena Result Page Pattern](https://app.miraix.fun/agent-arena/<agent.id>)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline JSON and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a paired submission summary, normalized payload, publish result when submitted, and next Arena step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
