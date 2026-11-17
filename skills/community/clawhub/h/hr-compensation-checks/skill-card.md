## Description:

Helps HR teams review compensation bands, market signals, offer decisions, and payroll filing prechecks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashley-aihr](https://clawhub.ai/user/ashley-aihr)

### License/Terms of Use:

MIT-0

## Use Case:

HR and compensation teams use this skill to decide whether an offer fits company bands, market data, internal fairness, and budget constraints, or whether a payroll filing packet has employee, entity, city, tax, social insurance, or housing fund risks that need follow-up.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive payroll and compensation data may be written into local plaintext report files.

Mitigation: Use the skill only in a controlled HR environment, choose a private output directory, avoid shared drives, and retain or delete generated files according to employee-data policy.

Risk: Generated CSV files may be unsafe to open in spreadsheet software when inputs come from untrusted sources.

Mitigation: Review generated files before forwarding or opening them in spreadsheet tools, especially when any input data was supplied by an untrusted party.

Risk: Compensation recommendations can be misleading when band, market, internal peer, budget, or candidate compensation inputs are incomplete.

Mitigation: Require human confirmation for missing or low-confidence inputs and treat public market signals as non-authoritative unless supported by paid survey data and internal company data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashley-aihr/skills/hr-compensation-checks)
- [Project homepage](https://github.com/Ashley-AIHR/hrskill-compensation-module)
- [China compensation policy knowledge base](references/china-compensation-policy-kb-2026.md)
- [China HR compensation workflows](references/compensation-workflows.md)
- [Dynamic market data architecture](references/dynamic-market-data-architecture.md)
- [Real user scenario](references/real-user-scenario.md)
- [Shanghai 2026 social insurance wage declaration notice](https://shanghai.chinatax.gov.cn/zcfw/zcfgk/sbf/202604/t480144.html)
- [Beijing housing fund annual base FAQ](https://gjj.beijing.gov.cn/web/zwfw5/1747335/1747336/743669918/index.html)
- [Shenzhen housing fund rule update](https://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/content/post_12687780.html)
- [Shanghai withholding client operation FAQ](https://shanghai.chinatax.gov.cn/jstax/ztzl/yshj/sycz/202512/t478537.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured fields; optional generated JSON, CSV, and DOCX report files from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local compensation or payroll report files when the user runs the packet-generation scripts.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
