## Description: <br>
Integrates Loop Engine with OpenClaw so workflow steps can require human approval, AI confidence checks, evidence capture, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[betterdataco](https://clawhub.ai/user/betterdataco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to add governed state transitions to OpenClaw workflows, including approval gates, evidence requirements, confidence thresholds, and audit records for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider-backed examples may send prompt and evidence context to external AI providers. <br>
Mitigation: Use local governance mode when external calls are not needed; for provider-backed use, install only required adapters, use scoped API keys, redact sensitive evidence, and review provider retention and contractual controls. <br>
Risk: Governance outcomes depend on configured guards, thresholds, actor permissions, and evidence fields. <br>
Mitigation: Review loop definitions before production use, require human approval for high-impact transitions, and test confidence and evidence gates against representative workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/betterdataco/loop-engine-governance) <br>
- [Loop Engine OpenClaw integration documentation](https://loopengine.io/docs/integrations/openclaw) <br>
- [@loop-engine/adapter-openclaw package](https://www.npmjs.com/package/@loop-engine/adapter-openclaw) <br>
- [@loop-engine/sdk package](https://www.npmjs.com/package/@loop-engine/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with TypeScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local governance mode avoids external LLM calls; provider-backed examples require explicit adapter configuration and provider API keys.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
