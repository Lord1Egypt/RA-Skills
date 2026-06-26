## Description: <br>
Hand off tasks to human assistants and track their completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HeyitSaif](https://clawhub.ai/user/HeyitSaif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register with Magic API, create tasks for human assistants, add task conversation messages, and monitor task completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details and owner contact information are sent to Magic and its human assistants. <br>
Mitigation: Require explicit user approval before creating tasks, and avoid sending confidential, sensitive, or unnecessary personal data. <br>
Risk: The Magic API key is needed for requests and may be saved for heartbeat monitoring. <br>
Mitigation: Treat the API key as a secret, avoid plaintext storage where possible, and document how to rotate or revoke it before enabling automated monitoring. <br>
Risk: Human assistants may act on tasks involving purchases, bookings, account access, documents, or third-party communications. <br>
Mitigation: Require human review and explicit approval for consequential tasks before they are submitted to Magic. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/HeyitSaif/magic-api) <br>
- [Magic API Console](https://console.api.getmagic.com) <br>
- [Magic API skill file](https://console.api.getmagic.com/skill.md) <br>
- [Magic API heartbeat guide](https://console.api.getmagic.com/heartbeat.md) <br>
- [Magic API documentation](https://console.api.getmagic.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Magic API key; task instructions are expected to include owner contact information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release; artifact frontmatter reports 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
