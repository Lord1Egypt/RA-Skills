## Description: <br>
Query nearby restaurants, shops, promotions, and points of interest by address using AMap, Baidu Maps, or Tencent Maps geocoding and search APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UyNewNas](https://clawhub.ai/user/UyNewNas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to geocode addresses and query nearby restaurants, merchants, promotions, and other points of interest through a configured map provider. <br>

### Deployment Geography for Use: <br>
Global, subject to selected map-provider availability and terms. <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation instructs agents to print map-provider API key values while checking configuration. <br>
Mitigation: Use presence-only environment checks and never echo API key values into logs, terminals, or responses. <br>
Risk: Address queries are sent to external map-provider APIs and may include sensitive home, workplace, or travel locations. <br>
Mitigation: Warn users before submitting sensitive addresses and use less precise locations when exact addresses are not required. <br>
Risk: Map-provider API keys may be misused if unrestricted. <br>
Mitigation: Use provider-side key restrictions, quotas, and monitoring for AMap, Baidu Maps, or Tencent Maps credentials. <br>


## Reference(s): <br>
- [ClawHub map-query Release Page](https://clawhub.ai/UyNewNas/map-query) <br>
- [AMap API](https://lbs.amap.com/) <br>
- [Baidu Maps API](https://lbsyun.baidu.com/) <br>
- [Tencent Maps API](https://lbs.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one configured map-provider API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
