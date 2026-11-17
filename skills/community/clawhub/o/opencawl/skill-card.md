## Description:

Add phone calling to your agent through OpenCawl. Use this skill to place calls, check outcomes, end active calls, and review voicemails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ammbo](https://clawhub.ai/user/ammbo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use OpenCawl to add outbound and optional inbound phone workflows to an agent, including placing calls, checking outcomes, ending active calls, and reviewing voicemails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers, call goals, context, transcripts, recordings, voicemails, and extracted contact details may be sensitive.

Mitigation: Install only if OpenCawl is trusted with this data and apply appropriate handling, retention, and access controls.

Risk: Outbound and inbound calls may create consent, notice, or recording-law obligations.

Mitigation: Confirm applicable consent and recording requirements before making or receiving calls.

Risk: Inbound webhooks and gateway tokens can expose call-related task data to external endpoints.

Mitigation: Configure callbacks and bearer tokens only for HTTPS endpoints you control and trust.

Risk: The OPENCAWL_API_KEY grants access to the OpenCawl integration.

Mitigation: Store the API key through the agent's normal secret-management path and avoid exposing it in prompts, logs, or shared files.

## Reference(s):

- [OpenCawl Skill Page](https://clawhub.ai/ammbo/skills/opencawl)
- [OpenCawl Homepage](https://opencawl.com)
- [OpenCawl API Reference](api.md)
- [Inbound Call Handling](inbound.md)
- [Personas & Voice Configuration](personas.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command examples and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return call IDs, call status and outcome summaries, transcripts, recording URLs, voicemails, and extracted contact details when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
