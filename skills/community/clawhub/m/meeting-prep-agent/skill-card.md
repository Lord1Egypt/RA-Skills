## Description: <br>
Meeting Prep Agent researches meeting attendees from calendar or on-demand inputs and generates briefing documents with attendee profiles, company context, talking points, and icebreakers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audsmith28](https://clawhub.ai/user/audsmith28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and customer-facing teams use this skill to prepare for sales calls, investor meetings, client kickoffs, interviews, networking events, and other scheduled meetings by generating people-first briefing notes before the meeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-prep can overwrite or reset persistent briefing history, which may cause duplicate preparation runs or loss of deduplication state. <br>
Mitigation: Use on-demand dry-run mode first and avoid scheduling auto-prep until the history-file reset behavior is fixed. <br>
Risk: Briefs and logs can contain sensitive meeting, attendee, and company context in the local meeting-prep cache. <br>
Mitigation: Restrict access to the local meeting-prep directory and manually delete old briefs and history until expiry and redaction controls are implemented. <br>
Risk: Research output can contain outdated or inaccurate public information about attendees or companies. <br>
Mitigation: Review generated briefs before use and verify important claims against cited sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/audsmith28/meeting-prep-agent) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing documents and CLI text output, with JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefs may be stored under the user's meeting-prep configuration directory and can include cited public sources when implemented.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
