## Description:

Integrates Loop Engine with OpenClaw to enforce runtime governance gates, evidence capture, AI confidence checks, human approvals, and audit trails for workflow steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betterdataco](https://clawhub.ai/user/betterdataco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to add Loop Engine governance policies to OpenClaw workflows, including human approval gates and AI-confidence or evidence guards before actions proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider-backed examples can send workflow evidence, prompt context, business data, transaction details, or infrastructure metadata to external LLM providers.

Mitigation: Prefer local governance mode unless LLM analysis is required; when provider adapters are used, apply guardEvidence, allowlist evidence fields, and redact, tokenize, or minimize PII, PCI, PHI, credentials, and infrastructure secrets before submission.

Risk: AI recommendations may affect financial, fraud, supply-chain, or operational decisions if adopted without review.

Mitigation: Require human approval for real financial or operational decisions and keep confidence-threshold and evidence-required guards enabled for provider-backed workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/betterdataco/skills/loop-engine-governance)
- [Loop Engine OpenClaw integration documentation](https://loopengine.io/docs/integrations/openclaw)
- [@loop-engine/adapter-openclaw package](https://www.npmjs.com/package/@loop-engine/adapter-openclaw)
- [@loop-engine/sdk package](https://www.npmjs.com/package/@loop-engine/sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local governance and optional provider-backed usage patterns.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
