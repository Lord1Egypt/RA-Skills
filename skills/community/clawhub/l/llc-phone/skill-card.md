## Description: <br>
Low-latency inbound and outbound AI phone calls via the OpenAI Realtime API and Twilio, covering pre-warm and pre-accept patterns, IVR and receptionist flows, customer-service routing, VAD tuning, function calling, prompt caching, and implementation caveats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cygnostik](https://clawhub.ai/user/cygnostik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to design and configure OpenClaw voice-agent phone systems for Twilio and the OpenAI Realtime API, including outbound pre-warm, inbound IVR, receptionist, and CSR workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice workflows can process caller data, store notes, and use silent phone-based lookup without sufficient disclosure or verification. <br>
Mitigation: Configure explicit call disclosures, consent and recording policies, caller verification before account-specific actions, strict transcript and note retention, and treat caller ID as a hint rather than authentication. <br>
Risk: The skill requires sensitive OpenAI and Twilio credentials. <br>
Mitigation: Store credentials only in OpenClaw environment configuration or a secret manager, avoid committing configuration files, and rotate or scope credentials according to deployment policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cygnostik/llc-phone) <br>
- [Publisher Profile](https://clawhub.ai/user/cygnostik) <br>
- [Promethean Dynamic](https://promethean-dynamic.com) <br>
- [README](artifact/README.md) <br>
- [Inbound Call Modes](artifact/docs/04-inbound-modes.md) <br>
- [OpenClaw Configuration Reference](artifact/docs/09-openclaw-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenAI and Twilio credentials when applying the guidance.] <br>

## Skill Version(s): <br>
3.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
