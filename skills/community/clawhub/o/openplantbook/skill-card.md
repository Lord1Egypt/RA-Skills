## Description: <br>
Open Plantbook API workflows with schema-first plant search, detail, and user-plant writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slaxor505](https://clawhub.ai/user/slaxor505) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Open Plantbook, retrieve plant details and care fields, and perform authenticated user-plant workflows through the official API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed Open Plantbook requests can expose or misuse API keys or OAuth secrets if credentials are printed, stored, or sent to an unexpected host. <br>
Mitigation: Provide credentials only when needed, keep secrets out of visible output and files, and use the documented official Open Plantbook API host. <br>
Risk: Create, update, or delete workflows can change a user's Open Plantbook plant data. <br>
Mitigation: Use OAuth credentials for write workflows and review the target plant and payload before any create, update, or delete request. <br>
Risk: Plant-care details from the API may be incomplete or inappropriate for safety-critical decisions such as toxicity, food safety, or medical use. <br>
Mitigation: Treat plant-care output as informational and verify safety-critical claims with an authoritative source before acting on them. <br>


## Reference(s): <br>
- [Open Plantbook API documentation](https://open.plantbook.io/docs/) <br>
- [Open Plantbook OpenAPI schema](https://open.plantbook.io/api/schema/) <br>
- [ClawHub Open Plantbook listing](https://clawhub.ai/slaxor505/skills/openplantbook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown guidance with optional shell commands and API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use credentials and network access for Open Plantbook API calls; raw JSON is included only when requested for debugging.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
