## Description: <br>
Manage n8n workflows from OpenClaw via the n8n REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DILOmcfly](https://clawhub.ai/user/DILOmcfly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to list, create, activate, deactivate, trigger, and debug n8n workflows on n8n Cloud or self-hosted n8n instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an n8n API key that can change workflows. <br>
Mitigation: Prefer a least-privilege key and test against a non-production n8n instance before production use. <br>
Risk: Activate, deactivate, and delete actions can have high operational impact. <br>
Mitigation: Require explicit confirmation before workflow-changing actions and review commands before execution. <br>


## Reference(s): <br>
- [n8n REST API Endpoint Reference](references/api-endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/DILOmcfly/n8n-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an n8n API URL and API key supplied by the user or environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
