## Description: <br>
智能驾驶决策支持系统 - 基于 L2 到 L5 级别的自动化和主动风险预测模型，提供实时路况下的情景压力测试、多传感器融合分析及高精度风险预警。集成中国道路交通安全法核心规则与新能源车型数据库。使用场景：自动驾驶算法设计、交通工程模拟、高级辅助驾驶功能评估、极端天气工况决策等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikewongonline](https://clawhub.ai/user/mikewongonline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, simulation teams, traffic-engineering reviewers, and NEV analysts use this skill to generate decision-support guidance for Chinese driving scenarios, traffic-law checks, NEV energy and safety analysis, and market comparisons. Outputs should be treated as reference material that requires expert review before safety, legal, investment, or purchase decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Driving or crash-response guidance could be mistaken for operational vehicle-control logic. <br>
Mitigation: Use the skill only as a static reference or simulation aid, keep it disconnected from vehicle control paths, and require qualified safety review before applying outputs. <br>
Risk: Legal and compliance outputs may be incomplete, outdated, or nonbinding. <br>
Mitigation: Verify cited regulations against official sources and require legal or compliance expert review before making decisions. <br>
Risk: Market ranking and investment-oriented language could influence purchases or investments. <br>
Mitigation: Treat market outputs as reference analysis only and do not authorize purchases, investments, or paid services without explicit human approval and independent review. <br>
Risk: Automatic update or external data language may imply unconfirmed network access or file changes. <br>
Mitigation: Confirm any external data access, refresh process, or file update explicitly before enabling it, and preserve source dates in generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikewongonline/intelligent-driving-dss) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Compliance review guide](artifact/compliance-review-guide.md) <br>
- [Core traffic rules overview](artifact/core-traffic-rules/README.md) <br>
- [NEV system module overview](artifact/nev-system-module/README.md) <br>
- [NEV data structure](artifact/nev-system-module/data-structure.json) <br>
- [Market rankings overview](artifact/market-rankings/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance, structured JSON data, and occasional code or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes legal, safety, market, and energy-analysis reference outputs with source and uncertainty notes when the skill follows its documented self-check flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
