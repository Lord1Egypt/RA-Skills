## Description: <br>
Plan Indonesia trips with island-routing logic, verified entry guidance, weather-aware logistics, and practical local execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users planning Indonesia trips use this skill to choose island clusters, design realistic routes, check entry and arrival logistics, and produce season-aware itineraries with safety, payment, and mobility notes. <br>

### Deployment Geography for Use: <br>
Global; travel guidance is specific to Indonesia. <br>

## Known Risks and Mitigations: <br>
Risk: Optional local trip memory can retain travel preferences and itinerary details under ~/indonesia/. <br>
Mitigation: Use one-off mode when continuity is not needed, and review or delete ~/indonesia/memory.md when trip details should no longer be retained. <br>
Risk: Entry rules, levies, park permits, weather, volcano status, and sea conditions can change after guidance is written. <br>
Mitigation: Re-check the official source map before buying non-refundable travel, booking boat days, or committing to volcano, diving, or park plans. <br>
Risk: Indonesia route advice can become unsafe or impractical if boats, scooters, heat, rough roads, stairs, or clinic access are understated. <br>
Mitigation: Include transfer buffers, mobility notes, safety tradeoffs, and fallbacks for high-friction routes, especially for families, older travelers, and low-mobility users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivangdavila/indonesia) <br>
- [Skill homepage](https://clawic.com/skills/indonesia) <br>
- [Official source map](artifact/sources.md) <br>
- [Entry and documents guidance](artifact/entry-and-documents.md) <br>
- [Safety and emergencies guidance](artifact/safety-and-emergencies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown travel-planning guidance with optional local Markdown trip notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May keep lightweight local trip context under ~/indonesia/ when continuity is useful; users can request one-off answers without memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
