## Description: <br>
Luma Event Manager helps Clawdbot users discover Luma events by topic or location, view event details and guest lists, RSVP, and sync events to Google Calendar without a Luma API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariovallereyes](https://clawhub.ai/user/mariovallereyes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Event hosts and attendees use this skill to find Luma events, inspect event details, manage their RSVPs, review host guest lists when authorized, and create Google Calendar entries through Clawdbot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Luma session cookies grant access to private Luma account data. <br>
Mitigation: Store cookies only in pass, treat them like passwords, and install the skill only if that access is acceptable. <br>
Risk: Guest-list features can expose private attendee information. <br>
Mitigation: Use guest-list commands only for events where you are authorized to view attendees. <br>
Risk: RSVP and calendar-sync commands can change Luma or Google account data. <br>
Mitigation: Run those commands only when you intend to update RSVP status or create a calendar entry, and confirm the target event and account first. <br>
Risk: Web scraping can fail or return incomplete data when Luma changes page structure or rate limits requests. <br>
Mitigation: Review returned event details before acting on them and retry later if the skill reports scraping or rate-limit errors. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mariovallereyes/luma-event-manager) <br>
- [Luma](https://lu.ma) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text and JSON-like tool results with occasional Markdown instructions and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include public event listings, authenticated account-specific event data, RSVP status, calendar sync status, and setup guidance.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
