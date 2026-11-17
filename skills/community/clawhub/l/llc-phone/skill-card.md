## Description:

Low-latency inbound and outbound AI phone calls via the OpenAI Realtime API and Twilio, covering pre-warm and pre-accept patterns, IVR and receptionist flows, customer-service routing, VAD tuning, function calling, prompt caching, and implementation caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cygnostik](https://clawhub.ai/user/cygnostik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and troubleshoot low-latency AI phone-call systems that connect OpenAI Realtime API sessions with Twilio media streams. It supports inbound IVR, receptionist, customer-service, and outbound calling flows with guidance for warm starts, audio handling, turn detection, and tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference instructions can lead to unsafe production deployment of billable phone calls, customer records, or caller audio.

Mitigation: Review before production use and add Twilio signature validation, outbound endpoint authentication, and strict request and tool-argument schemas.

Risk: Outbound calling flows can create cost, abuse, or policy exposure if destinations and call volume are uncontrolled.

Mitigation: Use destination allowlists, spending limits, rate limits, campaign controls, and audit logging before connecting real phone numbers or campaigns.

Risk: Customer-service and receptionist examples may touch personal data and call recordings.

Mitigation: Add record-level authorization, consent and notice language, and data-handling review before using customer records or caller audio.

Risk: Latency and behavior claims include practitioner observations that may vary by model, region, prompt, and transport path.

Mitigation: Benchmark the selected models, voices, prompts, and Twilio edge configuration in a production-like environment before rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cygnostik/skills/llc-phone)
- [Promethean Dynamic](https://promethean-dynamic.com)
- [Overview and model selection notes](docs/01-overview.md)
- [Session configuration reference](docs/02-session-config.md)
- [Pre-warm outbound calls](docs/03-prewarm-outbound.md)
- [Inbound call modes](docs/04-inbound-modes.md)
- [Operational notes and known issues](docs/08-known-issues.md)
- [OpenClaw configuration](docs/09-openclaw-config.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenAI and Twilio credentials for applied deployment.]

## Skill Version(s):

3.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
