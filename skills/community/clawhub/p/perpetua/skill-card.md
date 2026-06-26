## Description: <br>
OAuth proxy for calling external APIs (Oura, Google Calendar, etc.) via Perpetua.sh hosted API using a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DanielKillenberger](https://clawhub.ai/user/DanielKillenberger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to call Perpetua.sh-hosted proxy endpoints for Oura Ring data, Google Calendar events, and OAuth provider connection management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Oura or Google Calendar account data may pass through Perpetua.sh when the skill is used. <br>
Mitigation: Install only if you trust Perpetua.sh and the publisher with the connected account data; connect only the providers needed for the task. <br>
Risk: Broad provider requests can pull more account data than necessary. <br>
Mitigation: Prefer narrow date ranges and targeted endpoints; avoid broad data pulls unless explicitly needed. <br>
Risk: A long-lived or overexposed PERPETUA_API_KEY could allow unintended use of connected provider access. <br>
Mitigation: Store the API key in a secret manager, rotate it when needed, and revoke provider connections when finished. <br>


## Reference(s): <br>
- [Perpetua Skill on ClawHub](https://clawhub.ai/DanielKillenberger/perpetua) <br>
- [DanielKillenberger Publisher Profile](https://clawhub.ai/user/DanielKillenberger) <br>
- [Perpetua Hosted API](https://www.perpetua.sh/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PERPETUA_API_KEY and Perpetua.sh hosted API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
