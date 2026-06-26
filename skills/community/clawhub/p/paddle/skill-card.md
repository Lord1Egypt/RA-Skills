## Description: <br>
Integrate Paddle payments with subscriptions, webhooks, checkout, and tax compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Paddle billing for SaaS products, including checkout setup, subscription management, webhook verification, API calls, and tax compliance configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live billing operations can change subscriptions, access, or charges. <br>
Mitigation: Use Paddle sandbox keys first and require explicit review before any live subscription changes. <br>
Risk: API keys and webhook secrets could be exposed through prompts, logs, or local notes. <br>
Mitigation: Keep API keys and webhook secrets in environment variables or a secret manager, and keep ~/paddle/memory.md limited to non-secret integration notes. <br>
Risk: Customer and payment data is sent to Paddle during billing workflows. <br>
Mitigation: Install and use this skill only for Paddle billing work where sending customer, subscription, and payment data to Paddle is expected. <br>


## Reference(s): <br>
- [ClawHub Paddle Skill Page](https://clawhub.ai/ivangdavila/paddle) <br>
- [Paddle Skill Homepage](https://clawic.com/skills/paddle) <br>
- [Setup Guide](artifact/setup.md) <br>
- [API Reference](artifact/api.md) <br>
- [Webhook Handling](artifact/webhooks.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration notes, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Paddle API calls, webhook handling examples, checkout snippets, and local integration notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
