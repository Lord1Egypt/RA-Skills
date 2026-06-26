## Description: <br>
Plan Norway trips with fjord and Arctic routing, verified entry rules, multimodal logistics, and practical seasonal safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to design Norway itineraries that account for entry requirements, seasonality, transport tradeoffs, budget constraints, accessibility needs, and outdoor safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store trip preferences, family details, mobility notes, booking status, and route constraints in ~/norway/memory.md. <br>
Mitigation: Use memory only for durable planning facts, avoid storing unnecessary sensitive details, and review or delete ~/norway/memory.md when those details are no longer needed. <br>
Risk: Norway route guidance can become unsafe or impractical if weather, road status, ferry timing, or outdoor conditions are not checked close to travel. <br>
Mitigation: Treat itineraries as planning guidance and confirm current weather, road, ferry, emergency, and official entry information before booking or same-day travel. <br>


## Reference(s): <br>
- [ClawHub Norway skill page](https://clawhub.ai/ivangdavila/norway) <br>
- [Norway skill homepage](https://clawic.com/skills/norway) <br>
- [Norway skill source map](sources.md) <br>
- [UDI visitor and visa guidance](https://www.udi.no/en/want-to-apply/visit-and-holiday/) <br>
- [Entur national journey planner](https://entur.no/) <br>
- [SafeTravel Norway](https://www.safetravel.no/en/) <br>
- [Yr weather service](https://www.yr.no/en) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown travel-planning guidance with optional local memory setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use scoped local trip memory in ~/norway/memory.md when the user chooses to initialize it.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
