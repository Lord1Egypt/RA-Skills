## Description: <br>
DRG/DIP 医保分组计算 — ICD 编码搜索、DRG/DIP 分组、医保结算、CC/MCC 查询。需使用个人 MedGroup API Key 并连接 MedGroup MCP SSE。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u201013903](https://clawhub.ai/user/u201013903) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and healthcare operations developers use this skill to connect an agent to MedGroup MCP tools for ICD code lookup, DRG/DIP grouping, medical insurance settlement calculations, and CC/MCC status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required MedGroup API key could be exposed if it is embedded directly in MCP URLs, shared configuration files, or screenshots. <br>
Mitigation: Use a scoped, revocable key and prefer client secret storage over putting the key directly in the MCP URL. <br>
Risk: Patient-related data may be sent to the external MedGroup service during grouping, settlement, or code-status checks. <br>
Mitigation: Use synthetic or de-identified data unless MedGroup privacy, retention, logging, and compliance terms meet the user's requirements. <br>


## Reference(s): <br>
- [MedGroup homepage](https://medgroup.medchat.fun) <br>
- [MedGroup MCP SSE endpoint](https://medgroup.medchat.fun/mcp/sse) <br>
- [ClawHub skill listing](https://clawhub.ai/u201013903/medgroup-drgdip-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP tool arguments and structured MedGroup tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEDGROUP_API_KEY and a MedGroup MCP SSE endpoint configuration.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
