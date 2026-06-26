## Description: <br>
零配置即装即用，提供5项酒店搜索工具，支持万豪品牌查询、酒店详情、套餐推荐、周边餐饮搜索，基于飞猪与高德数据直连 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to search domestic hotels, Marriott-brand hotels, hotel packages, hotel details, and nearby dining from natural-language travel queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel and location queries are sent to external proxy services. <br>
Mitigation: Avoid entering sensitive itinerary details, private addresses, loyalty or account data, or traveler identity information unless the skill clearly documents where that data goes and why. <br>
Risk: Hotel prices and availability can change after the skill returns results. <br>
Mitigation: Confirm current price, availability, and booking terms on the final booking page before making travel decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/hotel-smart-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text or Markdown-style search results with hotel, package, dining, price, address, rating, booking-link, and source notes when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on external proxy services and real-time travel data availability.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact/version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
