## Description: <br>
Jeju With helps users view booking guidance, open hospital details, submit appointment requests, consult customer service, and check prices for Jeju With Hospital through BeautsGO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to navigate Jeju With Hospital booking options, submit appointment details, contact BeautsGO support, and request service price information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit appointment details and a phone number to an external medical-booking API without a clear separate in-chat confirmation step. <br>
Mitigation: Require users to review the appointment date, time, party size, and contact information, then give explicit final confirmation before any booking submission is sent. <br>
Risk: Appointment details and contact information may be sent to BeautsGO/Yestokr during the booking workflow. <br>
Mitigation: Inform users before collection and submission, and avoid entering personal contact information unless they intend to submit an appointment request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautsgo/jeju-with-clinic-booking) <br>
- [BeautsGO publisher profile](https://clawhub.ai/user/beautsgo) <br>
- [Jeju With Hospital booking page](https://i.beautsgo.com/cn/hospital/jeju-island-with-hospital/skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text string with links, booking summaries, price results, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open approved BeautsGO pages and may return booking or price lookup results from external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
