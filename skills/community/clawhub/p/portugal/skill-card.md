## Description: <br>
Discover Portugal like a local with specific restaurants, hidden gems, wine regions, and tips beyond the tourist traps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users planning Portugal travel use this skill to get localized guidance on cities, regions, food, wine, beaches, transport, safety, itineraries, and trip-style tradeoffs. The skill can also maintain optional local trip context in ~/portugal/memory.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip preferences and planning notes may be stored locally in ~/portugal/memory.md. <br>
Mitigation: Avoid storing passport numbers, payment data, or full booking confirmations, and delete ~/portugal/ when prior travel preferences should no longer be reused. <br>
Risk: Static travel guidance can become outdated for advisories, prices, opening hours, transport schedules, or health requirements. <br>
Mitigation: Verify current, high-impact travel details with official or provider sources before booking or relying on them during travel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/portugal) <br>
- [Skill homepage](https://clawic.com/skills/portugal) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Emergencies and safety guide](artifact/emergencies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown travel guidance with occasional shell commands and local memory-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses optional local trip memory under ~/portugal/; no network access is described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
