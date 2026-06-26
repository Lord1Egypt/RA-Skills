## Description: <br>
View and manage a Hybrid Training Plan by checking today's workout, logging strength sets and runs, marking days complete or skipped, and viewing exercise 1RMs and session history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulkennethkent](https://clawhub.ai/user/paulkennethkent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with a Hybrid Training Plan account use this skill to inspect training-plan details and update workout records through the Hybrid Training Plan API. It is intended for account-specific workout management with a user-provided API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with the configured API key can read and update Hybrid Training Plan workout data. <br>
Mitigation: Use a dedicated revocable API key and install the skill only when account access is intended. <br>
Risk: Incorrect dates, plan IDs, session IDs, weights, or log details could update the wrong workout record. <br>
Mitigation: Confirm dates, plan IDs, session IDs, weights, and log details before asking the agent to modify the plan. <br>
Risk: Changing HYBRID_API_URL can route account API requests to a different server. <br>
Mitigation: Keep HYBRID_API_URL at the default unless the alternate server is trusted. <br>


## Reference(s): <br>
- [Hybrid Training Plan API Reference](references/api.md) <br>
- [Hybrid Training Plan API](https://api.hybridtrainingplan.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/paulkennethkent/hybrid-training-plan) <br>
- [Publisher Profile](https://clawhub.ai/user/paulkennethkent) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and HYBRID_API_KEY; HYBRID_API_URL is optional and defaults to https://api.hybridtrainingplan.app.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
