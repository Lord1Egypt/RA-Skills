## Description: <br>
Finds real-world events in a requested city, area, or region, scores them against the user's preferences and availability context, and returns a ranked shortlist with source links and caveats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to discover local events for a requested geography and date window, compare candidates against their configured interests and dealbreakers, and receive a concise ranked shortlist. When explicitly requested, it can use Google Calendar availability or create one selected calendar event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores event preferences, source choices, and run summaries in its skill folder. <br>
Mitigation: Configure only the preferences and source lists needed for event recommendations, and avoid storing raw private data or unapproved liked/disliked event logs. <br>
Risk: Optional Google Calendar access can expose availability information if enabled. <br>
Mitigation: Enable the calendar connector only when availability-aware recommendations or calendar creation are wanted, review connector permissions, and prefer busy/free availability over event details. <br>
Risk: Calendar event creation may add the wrong event if event details are incomplete or ambiguous. <br>
Mitigation: Create calendar events only after an explicit user request and confirm title, date/time, location or link, and description before writing to Google Calendar. <br>
Risk: Public event listings can be incomplete, stale, or missing practical details. <br>
Mitigation: Preserve source links, confidence levels, and caveats so the user can verify details before attending, registering, or buying tickets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobiaswestholm/local-event-scanner) <br>
- [Operating Model](artifact/references/operating-model.md) <br>
- [Privacy And Access](artifact/references/privacy-and-access.md) <br>
- [Scoring Rubric](artifact/references/scoring-rubric.md) <br>
- [Availability Rules](artifact/references/availability-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown shortlist and run-note content with source links, recommendation labels, caveats, confidence, and optional calendar-add confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates run notes and preference/source configuration files within the skill folder; optional calendar access is user-directed.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
