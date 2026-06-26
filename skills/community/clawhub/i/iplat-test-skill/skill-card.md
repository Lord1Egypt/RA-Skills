## Description: <br>
京东国际物流数据查询技能，支持物流轨迹追踪、国际供应链运营指标查询和跨境小包体验指标查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdl-external-skills](https://clawhub.ai/user/jdl-external-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and logistics operations users use this skill to query JD international logistics tracking data and compare supply chain or cross-border package KPIs from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for JD logistics API access. <br>
Mitigation: Install only for authorized users, use a narrowly scoped token, and avoid sharing or committing credentials. <br>
Risk: The security summary reports HTTPS requests with certificate checks disabled. <br>
Mitigation: Patch or require an updated release that removes disabled certificate verification before sending real credentials or business data. <br>
Risk: The skill can disclose logistics tracking and operational KPI data returned by external APIs. <br>
Mitigation: Limit use to approved business contexts and review outputs before sharing outside authorized audiences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jdl-external-skills/iplat-test-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jdl-external-skills) <br>
- [Artifact README](artifact/README.md) <br>
- [Logistics trace skill documentation](artifact/skills/joy-logistics-trace/SKILL.md) <br>
- [Logistics indicator skill documentation](artifact/skills/joy-logistics-indicator/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses token-authenticated HTTPS calls to JD logistics endpoints and prints request and response data for agent interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
