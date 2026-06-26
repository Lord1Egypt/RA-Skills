## Description: <br>
自动生成中国诉讼案件的《诉讼策略与类案检索报告》，基于案情拆解争议焦点并编排法条/类案检索工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External legal professionals and agents use this skill to turn China mainland case facts into a structured litigation strategy and similar-case/legal-rule research report for pretrial preparation, client communication, and risk assessment. <br>

### Deployment Geography for Use: <br>
Global, for matters analyzed under the mainland China legal system. <br>

## Known Risks and Mitigations: <br>
Risk: Legal search terms, case summaries, and the configured API key are sent to the external DeliLegal API. <br>
Mitigation: Use only when the user is comfortable sending the query to DeliLegal, avoid client-identifying or privileged details where possible, and use a scoped API key. <br>
Risk: The bundled search scripts disable normal HTTPS certificate and hostname verification. <br>
Mitigation: Re-enable TLS certificate and hostname verification before routine use, and review network behavior before deployment. <br>
Risk: Legal research output can be incomplete, stale, or misleading when public case data is limited or the facts are underspecified. <br>
Mitigation: Treat the report as an attorney-review aid, verify important statutes and cases against authoritative sources, and clearly state assumptions and uncertainty. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/litigation-strategy-report) <br>
- [Search query pattern guide](references/search-query-patterns.md) <br>
- [DeliLegal law search API endpoint](https://platform.delilegal.com/api/v1/generice/law/list) <br>
- [DeliLegal case search API endpoint](https://platform.delilegal.com/api/v1/generice/case/list) <br>
- [DeliLegal API key management](https://open.delilegal.com/personal/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Chinese Markdown report with inline command guidance and legal/case search summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured DeliLegal API key before search commands can run; report conclusions should preserve assumptions, uncertainty, and risk caveats.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
