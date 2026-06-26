## Description: <br>
Plan Panama trips with region-aware routing, verified entry rules, island and highland logistics, and practical tourist safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to build practical Panama itineraries, compare regions, handle entry and transport constraints, and keep route-specific safety and weather considerations visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional local trip memory under ~/panama/ may contain personal travel preferences or constraints in plaintext. <br>
Mitigation: Avoid storing passport numbers, medical details, or other highly sensitive information, and edit or delete ~/panama/memory.md when persistent context is no longer wanted. <br>
Risk: Entry, safety, weather, transport, and sea-state details can change after release. <br>
Mitigation: Verify time-sensitive details with official sources before booking or traveling. <br>


## Reference(s): <br>
- [Panama skill release page](https://clawhub.ai/ivangdavila/panama) <br>
- [Tourism Panama travel requirements](https://www.tourismpanama.com/plan-your-vacation/travel-requirements/) <br>
- [National Migration tourist requirements](https://www.migracion.gob.pa/turistas/) <br>
- [Tocumen International Airport](https://www.tocumenpanama.aero/) <br>
- [Tourism Panama official travel hub](https://www.tourismpanama.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown travel guidance with route, logistics, safety, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local trip memory file under ~/panama/ when the user wants persistent trip context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
