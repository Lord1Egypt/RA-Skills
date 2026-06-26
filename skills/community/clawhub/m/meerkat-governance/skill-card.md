## Description: <br>
Meerkat Governance provides API endpoints for scanning untrusted content for prompt injection and checking AI output against source data, returning structured trust scores, threat details, audit identifiers, and remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7789996399](https://clawhub.ai/user/7789996399) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers configure agents to call Meerkat before processing untrusted content or before acting on generated output, using returned trust scores and remediation guidance to gate, sanitize, or correct agent behavior. <br>

### Deployment Geography for Use: <br>
Global use; the skill documentation states that API processing stays in Canada. <br>

## Known Risks and Mitigations: <br>
Risk: Selected content is sent to Meerkat's external API when the agent calls the shield or verify endpoints. <br>
Mitigation: Send only content approved for external processing, and avoid secrets, credentials, regulated records, or proprietary documents unless the service terms have been reviewed. <br>
Risk: The skill requires a Meerkat API key for authenticated requests. <br>
Mitigation: Store MEERKAT_API_KEY in the agent environment, limit access to trusted operators, and rotate the key if it may be compromised. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/7789996399/meerkat-governance) <br>
- [Meerkat platform](https://meerkatplatform.com) <br>
- [Meerkat documentation](https://meerkatplatform.com/docs) <br>
- [Meerkat privacy and data handling](https://meerkatplatform.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Guidance] <br>
**Output Format:** [Structured JSON responses with trust scores, threat details, audit identifiers, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEERKAT_API_KEY and sends selected content to Meerkat's external API only when the agent calls the endpoints.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
