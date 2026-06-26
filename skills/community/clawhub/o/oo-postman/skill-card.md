## Description: <br>
Postman (postman.com). Use this skill for ANY Postman request: reading, creating, updating, and deleting data through the OOMOL-connected Postman connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API teams use this skill to manage Postman workspaces, collections, requests, APIs, environments, mocks, monitors, webhooks, specifications, comments, and related resources through an authenticated OOMOL connector. It supports read, write, and destructive Postman workflows with schema inspection and confirmation guidance before state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Postman account and can act with the permissions available to that connection. <br>
Mitigation: Use an intended OOMOL/Postman connection, keep credentials server-side as designed, and review account scope before running actions. <br>
Risk: Write actions can create or modify Postman resources such as collections, workspaces, APIs, environments, monitors, mocks, and specifications. <br>
Mitigation: Inspect the live action schema first and confirm the exact payload and expected effect before running a write action. <br>
Risk: Destructive actions can permanently delete or overwrite Postman data. <br>
Mitigation: Require explicit user approval for the specific target and action before running destructive commands. <br>
Risk: Security evidence describes powerful state-changing workflows despite a clean verdict. <br>
Mitigation: Review the skill behavior before deployment and restrict use to trusted users and appropriate Postman workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-postman) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [Postman homepage](https://www.postman.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Postman connector commands, schema-inspection steps, JSON request payloads, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
