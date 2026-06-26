## Description: <br>
获取全国各省市油价信息，无需 API Key，适用于查询中国燃油价格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzihao0731](https://clawhub.ai/user/chenzihao0731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch current regional fuel prices in China for lookup, reporting, or lightweight script integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party oil-price API, so availability, rate limits, and returned prices depend on that service. <br>
Mitigation: Use it where outbound API access is acceptable, avoid excessive polling, and verify critical price data with an authoritative source. <br>
Risk: The script requires curl and jq at runtime. <br>
Mitigation: Install those dependencies from trusted package sources before use and review execution environments that restrict shell tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenzihao0731/oil-price) <br>
- [Oil price API endpoint](https://v2.xxapi.cn/api/oilPrice) <br>
- [API service homepage](https://v2.xxapi.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text pipe-delimited rows containing region, 92, 95, 98, and diesel prices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; sends an HTTPS request to a third-party oil-price API and does not use an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
