## Description:

生成中国大陆争议解决与诉讼管理场景下的《案件初步评估报告》，适用于接案评估阶段对案件基本事实、初步证据材料、我方诉求和管辖法院信息进行结构化梳理、法律关系识别、风险标注、司法裁判检索，并量化估算胜诉概率、诉讼周期、资金与时间成本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

Lawyers and litigation teams use this skill during China mainland dispute-resolution intake to structure facts, identify legal relationships and risks, search legal and case materials, estimate litigation likelihood, duration, and costs, and draft an initial case assessment report for internal decision-making and client communication.

### Deployment Geography for Use:

China mainland

## Known Risks and Mitigations:

Risk: Legal search can send matter details and API credentials to a third-party service without server identity checks.

Mitigation: Do not use confidential or privileged matter details until TLS verification is fixed; redact names, identifiers, account data, trade secrets, and unnecessary facts before external search.

Risk: Generated legal conclusions, case matches, and quantified estimates may be incomplete or misleading if inputs are sparse or searches are unavailable.

Mitigation: Treat outputs as preliminary assessment only, mark search limitations, lower confidence when evidence is incomplete, and verify legal results against official sources before client or filing use.

Risk: A real Delilegal API key may be exposed or reused if configured carelessly.

Mitigation: Store the API key carefully, avoid sharing configured skill copies, and rotate any key previously used on untrusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolalam/skills/litigation-intake-assessment)
- [Publisher profile](https://clawhub.ai/user/coolalam)
- [Assessment metrics](references/assessment-metrics.md)
- [Prompt template](references/prompt-template.md)
- [Search query patterns](references/search-query-patterns.md)
- [Delilegal API key setup](https://open.delilegal.com/personal/keys)
- [Delilegal case search endpoint](https://platform.delilegal.com/api/v1/generice/case/list)
- [Delilegal law search endpoint](https://platform.delilegal.com/api/v1/generice/law/list)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown report with optional shell command examples for legal and case searches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs conditional legal assessment prose; search results depend on a configured Delilegal API key and available public legal data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
