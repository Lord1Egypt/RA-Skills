## Description: <br>
零配置即装即用｜一次调用完成搜索与推荐｜含预订链接和退改政策｜自动识别场景智能推荐 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search global hotels, infer travel scenarios from natural-language requests, compare recommendations across price tiers, and return booking links with cancellation-policy summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel destination, travel dates, preferences, occupancy, and child-related booking details are sent to the skill's cloud proxy. <br>
Mitigation: Avoid unnecessary personal details in hotel queries and install the skill only when this data sharing is acceptable. <br>
Risk: Returned prices and booking links come from external travel services and may change. <br>
Mitigation: Confirm price, availability, and cancellation terms on the linked booking page before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/global-hotel-search-recommend) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendations with hotel search results, price-tier groupings, booking links, and cancellation-policy summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns external-service travel results; prices, availability, and booking terms should be verified on the linked booking page.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and artifact version file) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
