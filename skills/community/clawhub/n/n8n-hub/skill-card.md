## Description: <br>
Centralized n8n hub for designing reliable flows (idempotency, retries, HITL) and operating them via the public REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to design dependable n8n workflows and operate workflows or executions through the public REST API. It supports workflow planning, importable JSON generation on request, runbook creation, and lifecycle actions such as listing, activating, deactivating, debugging, and retrying workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API actions can change live n8n workflows, executions, credentials, variables, and related automation resources. <br>
Mitigation: Use least-privilege n8n API keys, confirm whether the target is production or a sandbox before activating or deactivating workflows, and review failed executions before retrying them. <br>
Risk: Webhook calls and workflow imports can process real data or trigger external side effects. <br>
Mitigation: Review generated workflow JSON and runbook steps before use, avoid embedding secrets, and reference environment variables or credential names instead. <br>


## Reference(s): <br>
- [n8n Hub Release Page](https://clawhub.ai/codedao12/n8n-hub) <br>
- [n8n Public API Endpoint Index](assets/endpoints-api.md) <br>
- [n8n Workflow Operations Runbook Template](assets/workflow-lab.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow design specs, importable workflow.json, workflow-lab.md runbooks, and n8n REST API command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
