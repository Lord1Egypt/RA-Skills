## Description: <br>
Park Skill helps answer industrial park operations questions across park overview, recruitment policy, enterprise services, operations management, and data dashboard scenarios in Chinese and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Park operators, recruitment teams, property managers, enterprise service teams, and operations leaders use this skill to retrieve park information, explain tenant policies, guide enterprise services, support property operations, and summarize occupancy or business metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace capability tags include crypto and purchase permissions even though the artifact is a documentation-and-configuration skill. <br>
Mitigation: Verify capability tags before deployment and avoid granting crypto or purchase permissions beyond what the skill files describe. <br>
Risk: The skill can discuss tenant, tax, financing, occupancy, and complaint information that may be sensitive in real operations. <br>
Mitigation: Limit access to operational data and review outputs before using them for business decisions or external communication. <br>
Risk: The artifact mentions Excel, PDF, and PPT export behavior, but no executable export implementation is present in the release evidence. <br>
Mitigation: Require confirmation before any future export implementation writes files, and prevent overwriting existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/park-skill) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [Publisher homepage](https://xiaping.coze.site) <br>
- [README.md](README.md) <br>
- [clawhub.yaml](clawhub.yaml) <br>
- [config/park-config.yaml](config/park-config.yaml) <br>
- [examples/example-query.md](examples/example-query.md) <br>
- [examples/example-output.md](examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Bilingual Markdown, Markdown tables, and structured JSON-style responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize configured park data, policies, service workflows, operational metrics, and report-style exports.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
