## Description:

网贷还款援助助手，帮助借款人分析贷款合规性、生成还款方案、评估可行性概率；内容由 AI 结合公开资料生成，仅供参考，不构成正式法律意见或金融建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[naive1024](https://clawhub.ai/user/naive1024)

### License/Terms of Use:

MIT-0

## Use Case:

External users with online-loan repayment concerns use this local Node.js CLI to enter loan amount, interest rate, overdue days, platform name, and monthly income, then receive compliance analysis, debt calculations, repayment options, feasibility estimates, and negotiation wording. The generated material is informational and should be checked with a licensed lawyer or relevant financial institution before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI asks for debt amount, interest rate, overdue days, platform name, and monthly income, which can be sensitive financial information.

Mitigation: Run it only in a trusted local environment, enter the minimum information needed, and avoid adding identity, contact, bank-account, or repayment details.

Risk: The generated report promotes an external assistance channel without enough privacy or independence disclosure.

Mitigation: Independently verify the external service and its privacy policy before contacting it, and do not share personal financial, identity, contact, or repayment details unless you trust the service.

Risk: The repayment and legal guidance is generated from public references and may be incomplete, outdated, or jurisdiction-specific.

Mitigation: Treat the output as informational planning material and confirm legal or financial decisions with a licensed lawyer, qualified adviser, or the relevant financial institution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/naive1024/skills/netloan-aid)
- [Publisher Profile](https://clawhub.ai/user/naive1024)
- [Free Plan Assistance Site](https://loan-aid-test-3g6whqku662d13c8.webapps.tcloudbase.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and Markdown-style guidance with repayment-plan sections and negotiation scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a local Node.js CLI in interactive or argument mode.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
