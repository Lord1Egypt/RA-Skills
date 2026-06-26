## Description: <br>
Guide users through Infini's basic API integration and webhook integration with step-by-step explanations, sandbox-first setup, and directly runnable Node.js or Python examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cola234](https://clawhub.ai/user/cola234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Infini payments with guided Hosted Checkout or Advanced Payment API steps, request signing, sandbox payment testing, webhook setup, and production switch-over guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook testing may send sandbox callback data to webhook.cool, a third-party debugging receiver. <br>
Mitigation: Use webhook.cool only with sandbox or dummy data, avoid production callbacks, and do not send secrets, customer data, or real transaction details through the test receiver. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cola234/infini-api) <br>
- [Infini English Overview](https://developer.infini.money/docs/en/1-overview) <br>
- [Infini Hosted Checkout Documentation](https://developer.infini.money/docs/en/3-checkout-mode) <br>
- [Infini Authentication Documentation](https://developer.infini.money/docs/en/4-authorization) <br>
- [Infini API Documentation](https://developer.infini.money/docs/en/6-api-ducumentation) <br>
- [Infini Webhook Documentation](https://developer.infini.money/docs/en/7-webhook) <br>
- [Infini API Notes](references/api-notes.md) <br>
- [Infini Basic Integration Workflow](references/workflow.md) <br>
- [Infini Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and step-by-step status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese or English responses, selected to match the user's language.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
