## Description: <br>
Pan Pac helps agents handle Pan Pacific Travel email, calendar, and booking communications by extracting travel details and routing booking or Outlook work to the appropriate supporting skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredguile](https://clawhub.ai/user/fredguile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel operations staff and their agents use this skill to interpret Pan Pacific Travel communications, extract booking details such as dates, destinations, passengers, statuses, confirmations, changes, and cancellations, and route booking or Outlook tasks to supporting skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for sensitive Pan Pacific Travel email, calendar, booking, document, and attachment workflows. <br>
Mitigation: Install it only for agents that should access those workflows, and confirm account and record access boundaries in the delegated lynx-skill and outlook-entra skills. <br>
Risk: Delegated booking operations, uploads, and attachment handling could affect travel records or expose business data. <br>
Mitigation: Require user confirmation before uploads, attachment handling, booking changes, or other record-modifying actions. <br>
Risk: Cancelled bookings may be omitted by default when retrieving itineraries through the delegated Lynx workflow. <br>
Mitigation: Use the documented cancelled-booking option when cancelled reservations are relevant to the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fredguile/pan-pac) <br>
- [Publisher profile](https://clawhub.ai/user/fredguile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with referenced supporting-skill commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve sensitive email, calendar, attachment, document, and booking data through delegated skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
