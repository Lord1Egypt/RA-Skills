## Description: <br>
房产信息查询 helps agents research Chinese real-estate listings, compare prices, review transactions, analyze communities and school districts, and generate an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather public housing information for second-hand homes, rentals, new homes, bargain listings, transactions, communities, school districts, and multi-property comparisons. It is intended to produce a concise finding summary and a local HTML report for review, not to replace official property, pricing, or school-district sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-estate prices, listings, transaction records, and school-district policies may be stale, incomplete, or inaccurate. <br>
Mitigation: Verify material property, pricing, transaction, and school-district claims against official or current sources before acting. <br>
Risk: Broad housing, school, or neighborhood phrases may trigger the skill even when the user has not provided enough search parameters. <br>
Mitigation: Confirm the query type and at least the target city before using web research or generating a report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/house-market-query) <br>
- [主流房产平台数据源参考](artifact/references/platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, HTML, Files, Guidance] <br>
**Output Format:** [Markdown response plus a local interactive HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under outputs/house_market_report_{city}_{timestamp}.html and should include source links, timestamps, analysis, suggestions, and disclaimers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
