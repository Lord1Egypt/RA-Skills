## Description: <br>
Configures MindStudio HTTP Request blocks for REST APIs, webhooks, and external services with request setup, response handling, and safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sol1986](https://clawhub.ai/user/sol1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
MindStudio builders and workflow developers use this skill to configure HTTP Request blocks for fetching data, sending payloads, updating or deleting records, and triggering external automations. It helps them collect the right endpoint, authentication, body, output variable, and downstream error-handling details before building the block. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTP Request blocks can send workflow data to external services. <br>
Mitigation: Use trusted endpoints, send only necessary fields, and keep credentials in workflow variables or a secret store. <br>
Risk: Update, replacement, or delete requests can modify or remove external records. <br>
Mitigation: Require explicit review for DELETE and full-record replacement operations, and prefer PATCH when only partial updates are needed. <br>
Risk: Broad HTTP guidance can produce incorrect configurations if endpoint requirements or variable names are assumed. <br>
Mitigation: Use the scenario-specific interview questions and verify endpoint URLs, auth headers, content types, required variables, and response handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sol1986/mindstudio-http-request-block-skill) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/examples.md) <br>
- [Skill metadata](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with ready-to-paste HTTP Request block configuration and downstream handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include URL, method, content type, headers, query parameters, body examples, output variable names, and success or failure handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
