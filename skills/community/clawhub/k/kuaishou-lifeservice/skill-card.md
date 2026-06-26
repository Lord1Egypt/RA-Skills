## Description: <br>
Kuaishou Life Service merchant operations assistant for querying products, stores, staff, official accounts, sub-accounts, and business performance data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingfeng9924](https://clawhub.ai/user/qingfeng9924) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants and developers use this skill to configure authorized Kuaishou Life Service merchant accounts, query merchant entities, and generate operational reports for business review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles merchant app secrets, access tokens, and broad business data, and stores local credentials or tokens in plaintext under ./.kuaishou-localife-token/. <br>
Mitigation: Install only from a trusted publisher, use least-privileged merchant credentials, keep the token directory out of synced or shared locations, delete it after use when possible, and rotate credentials if exposed. <br>
Risk: Prompts or setup steps may encourage users to share app_secret or other merchant credentials in chat. <br>
Mitigation: Prefer local environment or configuration flows, avoid pasting secrets into chat, and rotate any credential that has been shared accidentally. <br>
Risk: The skill can retrieve and display merchant reports broader than the user's immediate question. <br>
Mitigation: Use only with accounts authorized for the merchant data being requested and review generated reports before forwarding or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qingfeng9924/kuaishou-lifeservice) <br>
- [Kuaishou Life Service Open Platform](https://open.kwailocallife.com/) <br>
- [Kuaishou Life Service OpenAPI Reference](artifact/references/api-reference.md) <br>
- [Merchant Diagnostic Report Notes](artifact/references/report-notes.md) <br>
- [Kuaishou Life Service OpenAPI Documentation](https://docs.corp.kuaishou.com/d/home/fcABGZ7JGTqHnqn4WcaH8DkUp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line guidance; scripts may return JSON or Markdown business reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authorized Kuaishou merchant credentials and API responses for merchant-specific outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
