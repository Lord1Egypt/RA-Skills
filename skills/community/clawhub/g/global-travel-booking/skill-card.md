## Description: <br>
Defines an agent helper for aggregating hotel search results, room details, price comparisons, and booking handoffs across Fenbeitong, Ctrip, Meituan, Tongcheng, Huazhu, and Jinjiang. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, booking assistants, and business travel operators can use this skill to compare hotel options and format source-attributed search results across supported travel platforms. Users should verify availability, prices, and booking actions directly with the source platform before relying on the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary identifies this as an incomplete hotel-search aggregation scaffold with overstated live pricing and booking claims. <br>
Mitigation: Verify prices, room availability, and booking actions directly with the relevant hotel or travel platform before acting. <br>
Risk: Future full implementations may send travel or corporate booking details to multiple providers. <br>
Mitigation: Avoid sharing sensitive travel, employee, or corporate booking information unless the providers and data handling are acceptable for the user's environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/global-travel-booking) <br>
- [Publisher profile](https://clawhub.ai/user/ryan-zry) <br>
- [Fenbeitong API endpoint](https://openapiv2.fenbeitong.com) <br>
- [Ctrip API endpoint](https://api.ctrip.com) <br>
- [Meituan API endpoint](https://api.meituan.com) <br>
- [Tongcheng API endpoint](https://api.tongcheng.com) <br>
- [Huazhu API endpoint](https://api.huazhu.com) <br>
- [Jinjiang API endpoint](https://api.jinjiang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown tables and JSON-compatible function results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; prices, availability, and bookings should be checked against source platforms.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
