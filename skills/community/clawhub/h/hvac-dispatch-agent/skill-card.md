## Description: <br>
24/7 Voice & Text Dispatch Agent for HVAC & Plumbing. Qualifies leads, checks service zones, books appointments into ServiceTitan/Housecall Pro, and uses ThumbGate to prevent dangerous misquotes or out-of-zone bookings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home-service operators use this skill to let an agent answer HVAC and plumbing calls or texts, triage emergencies, validate service zones, and book qualified appointments into approved dispatch systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected CRM, calendar, voice, or text-provider access could create bookings outside the intended service area or without required contact details. <br>
Mitigation: Restrict integration permissions to booking-related actions and provide an explicit approved service-zone matrix plus required phone and address checks before live use. <br>
Risk: Emergency calls or messages could be handled incorrectly if automated booking is allowed for urgent situations. <br>
Mitigation: Confirm emergency routing details and test that urgent terms route to a human on-call path before enabling live dispatch. <br>
Risk: Exact repair quotes before technician assessment could create misleading customer expectations or liability. <br>
Mitigation: Allow only approved dispatch or diagnostic fees and verify the no-exact-repair-quote rule in testing. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/igorganapolsky/hvac-dispatch-agent) <br>
- [Publisher profile](https://clawhub.ai/user/igorganapolsky) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API Calls, Configuration] <br>
**Output Format:** [Natural-language dispatch responses with booking, escalation, and integration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform booking-related CRM, calendar, voice, or text-provider actions when connected to approved accounts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
