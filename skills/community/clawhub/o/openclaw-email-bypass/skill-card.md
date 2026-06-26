## Description: <br>
Send emails via Google Apps Script when traditional SMTP ports (25/465/587) are blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RISHIKREDDYL](https://clawhub.ai/user/RISHIKREDDYL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let agents send plain text or HTML email through a self-hosted Google Apps Script relay when direct SMTP is blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad email-sending capability through a public Google Apps Script relay. <br>
Mitigation: Use only an account approved for automated email, require per-send approval or recipient allowlists, and add rate controls before deployment. <br>
Risk: The reviewed package does not include the Google Apps Script relay code referenced by the skill. <br>
Mitigation: Inspect or supply the relay code before installing, and verify that the deployment URL is an HTTPS Google Apps Script endpoint. <br>
Risk: A leaked relay token could let an unauthorized caller send email through the relay. <br>
Mitigation: Store the token as a secret, use a long random value, rotate it if exposed, and avoid logging it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RISHIKREDDYL/openclaw-email-bypass) <br>
- [Setup Guide](references/setup.md) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, GOOGLE_SCRIPT_URL, GOOGLE_SCRIPT_TOKEN, and a deployed Google Apps Script relay.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
