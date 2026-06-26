## Description: <br>
Envoie le résultat de l'INR (International Normalized Ratio) à un centre de télémédecine spécialisé ou pour un test. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gillescv](https://clawhub.ai/user/gillescv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Gilles or an authorized helper uses this skill to send an INR self-measurement by email to the configured telemedicine recipient, with an optional test mode. It is intended for transmitting a specific medical measurement after the user supplies the INR value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The email includes identifiable medical information and personal details. <br>
Mitigation: Use only with authorization, verify the INR value and recipient mode before sending, and ensure the email account and recipient are appropriate for medical information. <br>
Risk: The skill depends on an undeclared local gog Gmail tool and configured Gmail account. <br>
Mitigation: Confirm the local Gmail tool path, account configuration, subject, and message body before executing the send command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gillescv/inr-sender) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text] <br>
**Output Format:** [Shell command that sends a formatted email message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local gog Gmail tool and a configured Gmail account; includes the INR value, date, recipient mode, and identifying details in the email body.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
