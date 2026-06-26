## Description: <br>
lann-booking helps agents look up Lann Thai Massage stores and services and create bookings for supported locations in China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lystrosaurus](https://clawhub.ai/user/lystrosaurus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and service agents use this skill to find Lann Thai Massage locations and services, then prepare or submit reservations after confirming phone number, store, service, party size, and appointment time. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Bundled test scripts can contact the live booking service and submit personal phone data. <br>
Mitigation: Review before installing, do not run test scripts unless live booking calls are intended, and avoid real customer phone numbers in tests. <br>
Risk: Booking workflows collect phone numbers and can expose personal data through full request or response logs. <br>
Mitigation: Confirm booking details before submission and redact phone numbers and other personal data from logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lystrosaurus/lann-booking-skill) <br>
- [Lann Booking API reference](artifact/references/api_reference.md) <br>
- [Booking response templates](artifact/assets/booking_template.md) <br>
- [Remote MCP service](https://open.lannlife.com/mcp) <br>
- [Direct booking API](https://open.lannlife.com/mcp/book/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured API request guidance with optional shell commands and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include store and service recommendations, masked phone confirmation, booking status, and booking details.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
