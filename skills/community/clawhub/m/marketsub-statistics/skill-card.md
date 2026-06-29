## Description: <br>
Helps agents request market entity statistics such as active enterprise counts, monthly additions, regional distributions, enterprise scale distributions, and financing statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinxin970620-prog](https://clawhub.ai/user/xinxin970620-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers or operators use this skill when a user needs market entity statistics for a province, city, or district, with a required query year and optional industry or enterprise-nature filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API_KEY is a sensitive credential required by the skill. <br>
Mitigation: Store the key in a local secret or environment mechanism and avoid pasting it into ordinary chat unless explicitly intended. <br>
Risk: The skill is specialized for market entity statistics and may be misapplied to broader business-data tasks. <br>
Mitigation: Use it only for specific market-statistics requests with the required dateValue and exactly one supported region-code level. <br>
Risk: The API response is passed through without additional processing. <br>
Mitigation: Review returned rows and status codes before relying on the data in downstream reports or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinxin970620-prog/marketsub-statistics) <br>
- [Market statistics unified invoke endpoint](https://rcd-test.dfwycredit.com/s1/skill/unified-invoke) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY, category 3.3, dateValue, and one of provinceCode, cityCode, or districtCode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
