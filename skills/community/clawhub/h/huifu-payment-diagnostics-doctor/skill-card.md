## Description:

A Chinese-language, evidence-based diagnostic skill for Huifu/DouGong payment integration failures across order creation, query, close, refund, reconciliation, signing, webhooks, checkout-js launch, final payment state confirmation, and release readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edhahrehh-ship-it](https://clawhub.ai/user/edhahrehh-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment integration engineers use this skill to diagnose Huifu/DouGong payment integration failures from redacted logs, request and response payloads, webhook traces, SDK errors, merchant configuration, and production-readiness evidence. It helps classify the failure into a diagnostic bucket and produce verification steps, repair actions, and prevention guidance without relying on guesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment troubleshooting can expose secrets or sensitive personal and transaction data through logs, webhook payloads, certificates, keys, tokens, passwords, card numbers, or identity numbers.

Mitigation: Redact keys, tokens, passwords, certificates, card or identity numbers, and other secrets before sharing diagnostic logs or payloads.

Risk: Incorrect diagnosis could cause unsafe payment state changes, such as trusting a browser callback as final payment success or using guessed transaction identifiers.

Mitigation: Base conclusions on scoped evidence such as server-side query results, verified webhooks, persisted order identifiers, and reconciliation records before recommending state changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edhahrehh-ship-it/skills/huifu-payment-diagnostics-doctor)
- [Huifu Payment Diagnostic Playbook](artifact/references/diagnostic-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown diagnostic guidance with checklists, tables, structured evidence requests, and occasional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts users to redact secrets and avoids treating browser callbacks as final payment success.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
