## Description:

Connect ElevenLabs Agents to your OpenClaw via phone with Twilio, including caller ID authentication, voice PIN security, call screening, memory injection, and cost tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cortexuvula](https://clawhub.ai/user/cortexuvula)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to connect an OpenClaw assistant to inbound or optional outbound phone calls through ElevenLabs Agents and Twilio. It helps configure a voice bridge with caller screening, memory context, transcript logging, and cost controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad personal memory, call history, and optional calendar data through a public voice bridge.

Mitigation: Use caller-specific data scopes, retrieve only the minimum context needed for each call, and set explicit transcript and memory retention limits.

Risk: Call content and selected local context may be sent to external voice and LLM providers.

Mitigation: Review provider terms, avoid injecting sensitive data by default, and disclose or restrict what caller information may be processed externally.

Risk: Bridge tokens, API keys, logs, and spoken PINs may become sensitive operational secrets.

Mitigation: Protect environment files and logs, avoid storing spoken PINs in transcripts, rotate secrets, and require strong bridge authentication.

Risk: A public phone bridge can be abused or create unexpected usage costs.

Mitigation: Enable whitelist-based call screening, rate limits, spend monitoring, and per-call cost logging before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cortexuvula/skills/phone-voice)
- [ElevenLabs Conversational AI](https://elevenlabs.io/conversational-ai)
- [Twilio](https://www.twilio.com/)
- [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, Python, and environment variable snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example webhook endpoints, caller whitelist data, bridge secrets, tunnel setup commands, and cost logging guidance.]

## Skill Version(s):

2.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
