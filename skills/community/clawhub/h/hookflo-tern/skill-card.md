## Description:

Helps agents provide webhook guidance for verification, alerting, logging, troubleshooting, and event-driven HTTP callback architecture using Tern and Hookflo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prateek32177](https://clawhub.ai/user/prateek32177)

### License/Terms of Use:


## Use Case:

Developers and integration teams use this skill to implement and debug webhook receivers, verify signatures for providers such as Stripe, GitHub, Clerk, and Supabase, and configure Hookflo alerting or logging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook forwarding examples may send complete payloads and incoming headers to a third-party service.

Mitigation: Before using forwarding patterns, allowlist outbound headers, redact or minimize payload fields, require HTTPS, and confirm the Hookflo destination and data sharing are approved.

Risk: Webhook payloads can contain secrets, regulated data, or sensitive customer and account events.

Mitigation: Avoid forwarding sensitive events unless that sharing is explicitly intended and compliant with the deployment's data-handling requirements.

## Reference(s):

- [Hookflo homepage](https://hookflo.com)
- [Tern source repository](https://github.com/Hookflo/tern)
- [Tern documentation](https://tern.hookflo.com)
- [Hookflo documentation](https://docs.hookflo.com)
- [Hookflo Webhooks on ClawHub](https://clawhub.ai/prateek32177/skills/hookflo-tern)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, JavaScript, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference optional environment variables for provider webhook secrets and tokens.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
