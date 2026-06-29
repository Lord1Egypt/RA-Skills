## Description: <br>
酒店降价监控与多平台比价助手，同时搜索多个旅游平台实时价格帮你比价省钱，支持按酒店名称精确比价、按城市搜索酒店列表、创建降价监控任务，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search hotel options, compare current prices across travel platforms, and prepare price-watch requests for selected hotels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel names, cities, stay dates, and occupancy details may be sent to a proxy service for live pricing. <br>
Mitigation: Install and use the skill only when users are comfortable sharing those travel details with the pricing service. <br>
Risk: Booking links are user-operated and some same-price links may use commission channels. <br>
Mitigation: Let users choose whether to open or use booking links, and make clear that the skill does not book on the user's behalf. <br>
Risk: Hotel prices, cancellation terms, and platform availability can change after a comparison is returned. <br>
Mitigation: Treat returned prices and cancellation details as current lookup results and have users verify terms on the booking platform before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/hotel-price-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-formatted hotel search, comparison, and watch-request results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Hotel names, cities, stay dates, occupancy details, and related query parameters may be sent to a proxy service for live pricing.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
