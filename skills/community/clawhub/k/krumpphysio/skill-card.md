## Description:

KrumpPhysio teaches OpenClaw agents to act as Krump-inspired physiotherapy coaches for therapeutic movement scoring, rehab coaching, Laban-style feedback, optional audit logging, and health-and-wellbeing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, coaches, and deploying teams use this skill to build agents that score therapeutic movements from provided joint-angle or video metrics and return concise Krump/Laban-styled coaching feedback. It can also guide optional Canton logging, observability, privacy-preserving attestations, media services, and Stripe payment flows when those integrations are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad exec-based integrations can run local scripts for video analysis, quantum planning, Canton logging, and payment-link creation.

Mitigation: Pin and review external scripts and dependencies, validate all command inputs, and run integrations with least-privilege service accounts.

Risk: Health-data logging and observability can expose sensitive coaching content or tool I/O.

Mitigation: Require explicit user or admin consent before enabling Canton logging or telemetry, disable prompt and tool-I/O capture by default, and keep payloads minimal.

Risk: Stripe payment actions are described near coaching workflows and could blur payment authority with health guidance.

Mitigation: Separate payment authority from coaching behavior and require reviewed, explicit payment commands with clear currency units and test/live mode labeling.

Risk: Third-party media, voice, and attestation services can send patient-adjacent data outside the local environment.

Mitigation: Enable those services only with configured credentials, documented consent, privacy controls, and data minimization.

Risk: The artifact suggests making the agent default for some workflows, while security evidence warns against default-agent deployment before hardening.

Mitigation: Follow the security evidence: install only after review and hardening, and do not make the skill the default agent unless risk controls are approved.

## Reference(s):

- [KrumpPhysio ClawHub Skill Page](https://clawhub.ai/arunnadarasa/skills/krumpphysio)
- [arunnadarasa Publisher Profile](https://clawhub.ai/user/arunnadarasa)
- [KrumpPhysio Skill Reference](artifact/reference.md)
- [KrumpPhysio Publishing Notes](artifact/PUBLISH.md)
- [KrumpPhysio Implementation Guide](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/IMPLEMENTATION-GUIDE-FLOCK-OPENCLAW-CANTON.md)
- [KrumpPhysio Privacy Documentation](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/PRIVACY.md)
- [KrumpPhysio Stripe Documentation](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/STRIPE.md)
- [KrumpPhysio Quantum README](https://github.com/arunnadarasa/krumpphysio/blob/main/quantum/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional inline shell commands and JSON-shaped metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Movement scoring replies usually include a score out of 10, brief feedback, Laban-style notation, a sign-off, and a health tip.]

## Skill Version(s):

1.0.11 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
