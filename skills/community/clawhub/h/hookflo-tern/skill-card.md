## Description: <br>
Provides webhook guidance for signature verification with Tern and no-code Hookflo alerting, logging, and troubleshooting for event-driven HTTP callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Prateek32177](https://clawhub.ai/user/Prateek32177) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to implement, verify, debug, and monitor webhooks across services such as Stripe, GitHub, Clerk, Supabase, and custom HTTP callback providers. It can also guide no-code Hookflo setup for Slack or email notifications from webhook events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook payloads may contain sensitive customer, payment, or account data when forwarded to Hookflo, Slack, or email. <br>
Mitigation: Confirm organizational approval before forwarding production payloads externally and minimize or redact sensitive fields where possible. <br>
Risk: Webhook signing secrets or provider tokens could be exposed if pasted into chat, examples, or source code. <br>
Mitigation: Store secrets in environment variables or platform secret stores and avoid sharing live secret values. <br>
Risk: Incorrect body parsing or verification configuration can cause valid webhooks to fail or invalid requests to be accepted. <br>
Mitigation: Use raw request bodies for HMAC verification, return HTTP 400 on failed verification, and test provider-specific signature settings before production use. <br>


## Reference(s): <br>
- [Hookflo homepage](https://hookflo.com) <br>
- [Tern source](https://github.com/Hookflo/tern) <br>
- [ClawHub skill page](https://clawhub.ai/Prateek32177/hookflo-tern) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; may reference optional environment variables for provider secrets and tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
