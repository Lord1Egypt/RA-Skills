## Description: <br>
Kamis Cli helps agents query Korean agricultural, livestock, and aquatic wholesale and retail price data from the official KAMIS OpenAPI for daily prices, trends, regional comparisons, and code lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, buyers, restaurants, reporters, and agent developers use this skill to retrieve and compare Korean food and produce price data for market checks, ingredient-cost monitoring, inflation analysis, and trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires KAMIS API credentials for full endpoint access. <br>
Mitigation: Use credentials only in a trusted shell or agent environment, avoid committing KAMIS_CERT_KEY or KAMIS_CERT_ID, and use TEST credentials only for limited smoke testing. <br>
Risk: KAMIS endpoint access may be limited by credential approval, endpoint restrictions, or API error responses. <br>
Mitigation: Check API responses for KAMIS error codes, confirm selected dates and product codes, and verify important market conclusions before operational use. <br>
Risk: Returned price values may be comma-formatted strings, which can cause incorrect calculations if treated as raw numbers. <br>
Mitigation: Normalize price strings before arithmetic, for example by removing commas and converting to numbers in jq or downstream code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chloepark85/kamis-cli) <br>
- [KAMIS OpenAPI Application](https://www.kamis.or.kr/customer/reference/openapi_list.do) <br>
- [KAMIS Price API Endpoint](https://www.kamis.or.kr/service/price/xml.do) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Configuration, Guidance] <br>
**Output Format:** [JSON from CLI scripts, Markdown summaries from examples, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KAMIS API credentials for full endpoint access; TEST credentials support limited smoke testing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
