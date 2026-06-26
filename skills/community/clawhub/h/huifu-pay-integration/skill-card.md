## Description: <br>
Helps developers integrate Huifu Pay across first-time builds, existing-system changes, aggregation payments, hosted payments, checkout-js, SDK examples, webhooks, troubleshooting, go-live checks, and version updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huifu](https://clawhub.ai/user/huifu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to choose a Huifu Pay integration path, review payment parameters and callbacks, generate SDK-oriented guidance for PHP, Java, and Python, troubleshoot integration errors, and prepare for launch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merchant credentials, RSA keys, openids, buyer IDs, certificate numbers, order numbers, and transaction logs may be exposed while using the skill. <br>
Mitigation: Keep secrets server-side, store them in secret managers or environment variables, mask logs, and avoid sharing real production values with the model. <br>
Risk: Payment and personal data may be mishandled during integration troubleshooting or launch preparation. <br>
Mitigation: Use masked or sandbox data when possible, review generated changes before deployment, and confirm merchant-specific configuration outside the model. <br>


## Reference(s): <br>
- [Shared Overview](references/shared-overview.md) <br>
- [Copilot Onboarding](references/copilot-onboarding.md) <br>
- [Solution Selection](references/copilot-solution-selection.md) <br>
- [Existing System Integration](references/copilot-existing-system.md) <br>
- [Troubleshooting Playbooks](references/copilot-troubleshooting-playbooks.md) <br>
- [Go-Live Checklist](references/copilot-go-live-checklist.md) <br>
- [Credential Boundary](references/shared-credential-boundary.md) <br>
- [Webhook Signing](references/shared-webhook-signing.md) <br>
- [Official Service Source Index](references/official-service-source-index.md) <br>
- [Huifu AI Skill Support](https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown responses with checklists, code snippets, configuration notes, and local reference lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes each answer to a small set of local references and treats merchant credentials, keys, transaction identifiers, and payment logs as sensitive.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
