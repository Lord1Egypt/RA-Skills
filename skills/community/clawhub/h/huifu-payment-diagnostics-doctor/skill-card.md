## Description: <br>
基于证据的汇付/斗拱支付联调诊断 Skill，用于依据日志、请求响应、Webhook 轨迹、SDK 错误、商户配置和生产检查证据来排查下单、查单、关单、退款、对账、签名验签、异步通知、checkout-js 拉起、最终支付状态确认和上线验收问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edhahrehh-ship-it](https://clawhub.ai/user/edhahrehh-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment integration engineers use this skill to diagnose Huifu/DouGong payment integration failures from sanitized logs, request and response payloads, webhook evidence, SDK behavior, configuration, and order-state records. It helps classify issues, identify likely causes, propose verification steps, and outline code, data, or operations fixes without inventing merchant values or treating front-end callbacks as final payment success. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment logs, webhook payloads, merchant identifiers, credentials, or customer data may be exposed during troubleshooting. <br>
Mitigation: Share only sanitized evidence, redact private keys, certificates, tokens, passwords, card and identity numbers, personal data, and unnecessary merchant identifiers, and rotate any secret that was pasted. <br>
Risk: A browser callback or page redirect may be mistaken for final payment success. <br>
Mitigation: Confirm final payment state through server-side query, verified webhook, or reconciliation before updating durable business state. <br>
Risk: Production-impacting changes may be made from incomplete evidence or placeholder merchant values. <br>
Mitigation: Use the skill as a diagnostic checklist, require real redacted configuration evidence before production code changes, and verify fixes against official Huifu/DouGong documentation or support. <br>


## Reference(s): <br>
- [Huifu Payment Diagnostic Playbook](references/diagnostic-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown diagnostic report with checklists, evidence summaries, verification steps, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to redact payment logs, credentials, private keys, tokens, certificates, card data, identity numbers, and unnecessary merchant identifiers before sharing evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
