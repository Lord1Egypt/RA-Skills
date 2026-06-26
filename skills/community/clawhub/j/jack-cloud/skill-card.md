## Description: <br>
Deploy web services to the cloud with Jack, including APIs, websites, backends, project creation, deployment, databases, logs, and Jack Cloud services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellno](https://clawhub.ai/user/hellno) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create, deploy, and manage Jack Cloud web services, including Cloudflare Workers projects with databases, storage, logs, secrets, cron, and custom domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill can upload source code and modify live Jack Cloud resources. <br>
Mitigation: Before deployment or resource-changing commands, confirm the project directory, logged-in Jack account, target repository contents, and intended cloud resources. <br>
Risk: Database-write, secret, and domain commands can change production application state or expose sensitive configuration if run in the wrong project. <br>
Mitigation: Review command targets and parameters before execution, and use read-only status or list commands when verifying context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hellno/jack-cloud) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hellno) <br>
- [ClawHub metadata homepage](https://github.com/getjack-org/skills) <br>
- [Jack Cloud services guide](reference/services-guide.md) <br>
- [Jack documentation](https://docs.getjack.org) <br>
- [Jack CLI npm package](https://www.npmjs.com/package/@getjack/jack) <br>
- [Jack homepage](https://getjack.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend Jack MCP tools when available and CLI commands otherwise.] <br>

## Skill Version(s): <br>
0.3.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
