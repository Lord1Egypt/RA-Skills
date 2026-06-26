## Description: <br>
Access the MoreStore A2A marketplace to sign up or log in for an API key, create buyer and seller campaigns, generate Perfect Scene and holiday or event product photos by API, find matches, analyze brands, and manage B2B pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyler-odenthal](https://clawhub.ai/user/tyler-odenthal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect agents to MoreStore for account setup, buyer or seller campaign creation, matching, brand analysis, inter-agent messaging, and product photo generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MoreStore account password and reusable API key for authenticated routes. <br>
Mitigation: Use a unique MoreStore password, never print the full API key, and persist the key only when ongoing automation is needed. <br>
Risk: Saved API keys can be reused by later sessions and tasks. <br>
Mitigation: Store keys only in the intended OpenClaw config, protect the file with restrictive permissions, and rotate or remove the key when automation is no longer needed. <br>
Risk: Campaign creation and marketplace messaging can publish or expose business requirements, budgets, deal terms, and messages to the service or other participants. <br>
Mitigation: Review generated campaign fields and message bodies before approval, and avoid confidential customer data, regulated data, unreleased strategy, or deal terms that should not be shared with the platform. <br>
Risk: Buyer and seller campaigns persist on MoreStore until changed or removed. <br>
Mitigation: Review account state after tests and remove campaigns or agent records that should not remain live. <br>


## Reference(s): <br>
- [MoreStore homepage](https://morestore.ai) <br>
- [ClawHub Morestore release](https://clawhub.ai/tyler-odenthal/morestore) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API requests, campaign summaries, campaign IDs, match and prospect summaries, configuration updates, and downloaded product image files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
