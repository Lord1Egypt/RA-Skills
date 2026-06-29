## Description: <br>
海关数据分析专家Skill — 海关查询系统，海关数据查询平台，海关数据分析，海关数据统计，全球海关数据查询，外贸数据，国外进出口数据，提单数据，关单数据，国外采购商平台，海关数据查询，全球进出口数据，中国进出口数据，找国外客户，国外采购商订单。支持按HS编码/产品名称、采购商、供应商进行多维度贸易数据分析 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oraagent](https://clawhub.ai/user/oraagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trade analysts use this skill to query Ora Trade customs data, analyze import and export activity, compare buyers and suppliers, review HS-code or product trends, and summarize shipping or order details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses a local OraAgent API key and sends it to the Ora Trade service for queries. <br>
Mitigation: Install only if you trust Ora Trade and its h.smtso.com service with that key; remove or revoke the key when you stop using the skill. <br>
Risk: The security scan marked the release for review because it depends on sensitive credentials and scripted service requests. <br>
Mitigation: Review the skill before installing, keep the key file access limited to the intended user, and scan the artifact before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oraagent/ora-customs-pro) <br>
- [Publisher profile](https://clawhub.ai/user/oraagent) <br>
- [Topeasy China](https://www.topeasychina.com) <br>
- [Ora Trade](https://www.oraskl.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown trade-data analysis with inline shell commands when a service query is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local OraAgent API key file for authenticated Ora Trade service queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
