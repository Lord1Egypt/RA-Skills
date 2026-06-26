## Description: <br>
Generates a clean WhatsApp pairing QR code PNG from a running OpenClaw agent and delivers it to the user through the active conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanblanchfield](https://clawhub.ai/user/seanblanchfield) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People linking an agent to WhatsApp use this skill to generate a time-limited pairing QR code PNG and send it through the active conversation so it can be scanned immediately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated WhatsApp pairing QR code can link an account if it is posted to the wrong conversation or scanned by the wrong person. <br>
Mitigation: Generate it only after the user confirms they are ready, send it only in the intended private conversation, confirm the destination before posting, and delete the temporary image after use. <br>
Risk: The Mattermost thread delivery path uses a local Mattermost bearer token for authenticated file upload and posting. <br>
Mitigation: Install only in environments that trust this skill with that token, review the token access scope before use, and prefer the normal message delivery path when thread-specific posting is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanblanchfield/jentic-whatsapp-qr) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG file plus concise user-facing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a short-lived WhatsApp pairing QR code image and sends scanning guidance to the user.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
