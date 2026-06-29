## Description: <br>
Diagnose and fix common Gladia API issues, including authentication errors, rate limits, unexpected behavior, transcription quality issues, billing confusion, audio format problems, WebSocket disconnections, and polling failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladiaio](https://clawhub.ai/user/gladiaio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to diagnose Gladia API integrations before or during production use. It provides targeted troubleshooting guidance for credentials, limits, audio configuration, SDK usage, WebSocket recovery, callbacks, transcription quality, and billing-related surprises. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting may involve API keys, webhook secrets, callback payloads, or other sensitive integration data. <br>
Mitigation: Use test credentials and sample payloads when possible, avoid pasting real secrets into chats or logs, and rotate any credential that may have been exposed. <br>
Risk: Plan limits, billing behavior, feature availability, and API limits may change after the skill release. <br>
Mitigation: Verify current limits and billing behavior against the linked Gladia documentation, dashboard, or support resources before making production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gladiaio/gladia-troubleshooting) <br>
- [Gladia authentication documentation](https://docs.gladia.io/chapters/api/authentication) <br>
- [Gladia rate limits and concurrency](https://docs.gladia.io/chapters/limits-and-specifications/rate-limits) <br>
- [Gladia supported formats and limits](https://docs.gladia.io/chapters/limits-and-specifications/supported-formats) <br>
- [Gladia webhooks documentation](https://docs.gladia.io/chapters/pre-recorded-stt/webhooks) <br>
- [Gladia API reference](https://docs.gladia.io/api-reference) <br>
- [Gladia API status](https://status.gladia.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown diagnostic guidance with JSON, TypeScript, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; may discuss API keys, webhook payloads, billing behavior, and plan limits but does not execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
