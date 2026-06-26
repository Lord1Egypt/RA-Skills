## Description: <br>
Open Health helps users find and book virtual mental health appointments with licensed US providers through conversational availability search and booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gljirain](https://clawhub.ai/user/gljirain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to search for same-day or next-day psychiatric and mental health telehealth appointments, compare provider availability, and book a video visit with insurance or cash-pay options. Agents should use it only when the user clearly wants care booking, not for crisis support, diagnosis, prescription refills, or general medical advice. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive mental-health appointment details, identity, contact information, date of birth, and insurance/member ID to a remote booking service. <br>
Mitigation: Confirm the exact payload and destination with the user before any real booking, prefer dry-run validation first, and never log, persist, or store patient information. <br>
Risk: Users may treat the booking workflow as medical advice or crisis support. <br>
Mitigation: Use the skill only for care booking requests; route crisis language to emergency resources and defer diagnosis or treatment guidance to licensed providers. <br>
Risk: A real booking action can create an appointment, and availability may change before confirmation. <br>
Mitigation: Get explicit user confirmation for the selected provider and time before booking, and search again if the selected slot is unavailable. <br>


## Reference(s): <br>
- [Klarity Booking API Reference](references/api-reference.md) <br>
- [Klarity Booking API](https://rx.helloklarity.com) <br>
- [Open Health on ClawHub](https://clawhub.ai/gljirain/open-health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, API Calls] <br>
**Output Format:** [Conversational text with shell command examples and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; availability and booking depend on the remote telehealth booking API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
