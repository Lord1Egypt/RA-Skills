## Description: <br>
零配置即装即用｜景点门票酒店机票一键查｜含预订链接和实时价格｜本地生活特价直达 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents use this skill to look up Meituan travel options for hotels, flights, trains, attraction tickets, and itinerary ideas across supported Chinese cities. It returns prices, schedules, availability details, and booking links for follow-up outside the skill. <br>

### Deployment Geography for Use: <br>
Global, with results focused on China travel inventory. <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches are sent through a cloud proxy, which can expose city names, destinations, timing, and booking intent. <br>
Mitigation: Avoid entering sensitive personal itinerary details unless needed for the query and only use the skill if the proxy operator is trusted. <br>
Risk: Prices, schedules, availability, and booking links can change, and the skill does not complete booking or payment. <br>
Mitigation: Confirm all details on the linked Meituan booking page before relying on them or making a purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/meituan-travel-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [JSON responses summarized by the agent as travel guidance and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a city and natural-language travel query; prices, schedules, availability, and booking links may change.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact version file) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
