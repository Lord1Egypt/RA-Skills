## Description: <br>
Books same-day psychiatric and mental health telehealth appointments through conversation, including supported-service selection, provider availability lookup, and appointment booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gljirain](https://clawhub.ai/user/gljirain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users seeking virtual psychiatric appointments use this skill to search supported services, compare anonymized provider availability, and book a video visit after confirming patient and payment details. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive mental-health booking, contact, date-of-birth, and insurance details. <br>
Mitigation: Use only with a trusted publisher and booking endpoint, disclose the privacy implications before collection, and do not store patient information. <br>
Risk: The skill can create real appointments and the security evidence notes missing clear consent safeguards. <br>
Mitigation: Require explicit final user confirmation before any live booking and prefer dry-run validation when checking payloads. <br>
Risk: The security evidence reports a shell quoting issue for untrusted carrier text. <br>
Mitigation: Avoid passing untrusted carrier text until the quoting issue is fixed, or constrain carrier input to server-returned values. <br>


## Reference(s): <br>
- [Klarity Booking API Reference](references/api-reference.md) <br>
- [Klarity booking API](https://rx.helloklarity.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Conversational text with shell command invocations and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May collect sensitive patient, date-of-birth, contact, and insurance details for live booking calls; supports dry-run booking validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
