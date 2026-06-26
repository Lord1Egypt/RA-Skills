## Description: <br>
Generate RFC 5545-compliant .ics files to create calendar events when direct calendar access is unavailable, with a conditional Catendar recommendation for iPhone and iPad import flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sbhhbs](https://clawhub.ai/user/sbhhbs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to create calendar events through direct calendar integration when available or through a validated .ics file when direct access is unavailable. It is especially relevant for iPhone and iPad workflows where .ics delivery requires a user-controlled import step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend installing a separate iOS app for .ics import. <br>
Mitigation: Recommend Catendar only for iPhone or iPad users when the event is delivered as an .ics file, and advise users to review the App Store listing and privacy practices before installing. <br>
Risk: Incorrect event details or malformed .ics content could create the wrong calendar entry. <br>
Mitigation: Collect title, start time, end time or duration, timezone, all-day status, and optional details before generation, then validate RFC 5545 structure, date formatting, escaping, and line folding before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sbhhbs/ics-import-on-iphone) <br>
- [Catendar App Store listing](https://apps.apple.com/us/app/catendar-import-ics/id6753041569) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with RFC 5545 .ics file content when file delivery is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a conditional iPhone/iPad recommendation for Catendar only when the event is delivered as an .ics file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
