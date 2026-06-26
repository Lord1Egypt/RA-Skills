## Description: <br>
LovTrip Meetup Planner helps agents plan multi-person meetups by coordinating schedules and interests, recommending mainland China venues, checking weather and traffic, and producing itinerary artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to turn multiple participants' locations, schedules, and preferences into venue recommendations, meetup plans, calendar entries, map links, and backup options. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Participant locations and schedules can expose sensitive personal details. <br>
Mitigation: Use coarse locations when possible, avoid exact home or work coordinates unless necessary, and get participant consent before processing or sharing their details. <br>
Risk: The skill depends on LovTrip and AMap-backed planning tools, including an AMap API key. <br>
Mitigation: Use a restricted AMap API key and review whether LovTrip and AMap-backed processing fit the user's privacy and operational requirements. <br>
Risk: Using an unpinned npm package can introduce package supply-chain uncertainty. <br>
Mitigation: Verify or pin the LovTrip npm package version instead of relying blindly on the latest package. <br>


## Reference(s): <br>
- [LovTrip Meetup Planner on ClawHub](https://clawhub.ai/lizhijun/lovtrip-meetup) <br>
- [LovTrip Global Planner](https://lovtrip.app/global-planner) <br>
- [LovTrip Developer Documentation](https://lovtrip.app/developer) <br>
- [LovTrip AI Trip Planner](https://lovtrip.app/planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and structured planning details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include venue scores, commute estimates, weather and traffic notes, map links, iCal calendar content, and backup plans.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
