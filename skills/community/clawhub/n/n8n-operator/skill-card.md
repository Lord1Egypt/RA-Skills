## Description: <br>
Helps agents design, create, modify, test, and manage n8n workflows through the n8n REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujun2508](https://clawhub.ai/user/lujun2508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation engineers, and DevOps users use this skill to plan n8n workflow architecture, generate workflow JSON, call n8n API endpoints, validate workflow structure, and manage activation or execution after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use API-level control over an n8n instance, including workflow activation, execution, deletion, and credential-related endpoints. <br>
Mitigation: Use a test n8n instance first, scope the API key to the intended instance, and review generated workflow IDs, API requests, and workflow JSON before execution. <br>
Risk: The security summary flags under-scoped guidance for persistent local cron changes and host-mounted Desktop writes. <br>
Mitigation: Do not allow cron edits or host-mounted Desktop writes unless persistent local automation is explicitly intended and rollback steps are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lujun2508/n8n-operator) <br>
- [n8n API reference](references/references/api.md) <br>
- [n8n node templates](references/node-templates.md) <br>
- [n8n workflow patterns](references/workflow-patterns.md) <br>
- [n8n desktop file write notes](references/desktop-write.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON workflow snippets, Python or shell command examples, and API call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow IDs, webhook URLs, validation summaries, and generated n8n workflow JSON for user review.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
