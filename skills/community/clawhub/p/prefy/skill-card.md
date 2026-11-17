## Description:

Connect to Prefy AI platform — Conductor API (19 models, OpenAI-compatible), server management, web search, image generation, phone calls (AutoCall). Use when agent needs multi-model AI routing, dedicated server provisioning, web intelligence, or restaurant/hotel phone calls. Base URL https://prefy.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runrelay](https://clawhub.ai/user/runrelay)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call Prefy APIs for multi-model chat routing, web search, image generation, event lookup, server management, and venue phone-call workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server command, checkout, cron, bot, and shell actions can have high impact if executed without clear user approval.

Mitigation: Require explicit confirmation before any server command, checkout, cron change, bot action, or shell command.

Risk: AutoCall can initiate real-world phone calls to venues.

Mitigation: Require explicit confirmation of the phone number, venue, task, and language before placing a call.

Risk: Chat, search, image, and agent endpoints may receive sensitive user data.

Mitigation: Send private data or credentials only when Prefy's handling is acceptable for the user's use case.

## Reference(s):

- [Prefy Documentation](https://prefy.com/docs)
- [Prefy ClawHub Skill](https://clawhub.ai/runrelay/skills/prefy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Prefy API credentials, Supabase JWT authentication for server and agent APIs, and user confirmation before high-impact actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
