## Description: <br>
Map Search aggregates place and nearby search across Amap, Baidu Maps, and Tencent Maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoucangjia1qu](https://clawhub.ai/user/shoucangjia1qu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search Chinese map providers for places by keyword, city or region, or nearby coordinates and compare concise map results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches and nearby-search location data may be sent to Amap, Baidu, or Tencent. <br>
Mitigation: Use only for queries appropriate to share with those providers, avoid sensitive searches, and prefer explicit coordinates over automatic IP location when privacy matters. <br>
Risk: The skill requires third-party map API keys that may be subject to quotas, billing, or exposure if mishandled. <br>
Mitigation: Use map-only API keys with quotas, keep them in the documented config or environment variables, and rotate or revoke keys if exposed. <br>
Risk: Search terms, regions, and coordinate inputs are embedded into provider request URLs. <br>
Mitigation: Review inputs before execution and treat the URL-encoding issue noted by the security guidance as something the publisher should fix before handling untrusted or special-character input. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shoucangjia1qu/map-search) <br>
- [Amap Maps Platform](https://lbs.amap.com/) <br>
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/) <br>
- [Tencent Location Service](https://lbs.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text search results with place names, addresses, distances, and locations; Markdown usage guidance with shell and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and at least one configured map-provider API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
