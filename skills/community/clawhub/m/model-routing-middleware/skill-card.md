## Description: <br>
Intelligent model selection middleware for AI agents. Route tasks to the best model, manage context, and cut API costs 40-70%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larios613-hub](https://clawhub.ai/user/larios613-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add model-routing middleware to an AI agent or gateway so requests can be classified, routed to configured models, escalated on low confidence, and managed against context-window limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt excerpts may be logged by default, which can expose secrets, private data, proprietary code, or regulated information. <br>
Mitigation: Review and change logging settings before installation; disable prompt previews or reduce retained prompt content for sensitive deployments. <br>
Risk: Broad activation terms can route unintended requests through the middleware. <br>
Mitigation: Narrow activation triggers and confirm the router is only invoked for intended model-selection workflows. <br>
Risk: Cloud routes or escalation targets may send data to providers that do not match the user's data-handling policy. <br>
Mitigation: Verify configured model providers, endpoints, and escalation chains before connecting the router to real model providers. <br>


## Reference(s): <br>
- [Model Routing Middleware on ClawHub](https://clawhub.ai/larios613-hub/model-routing-middleware) <br>
- [Model Routing Integration Guide](artifact/references/integration-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes include model choice, think-mode setting, task type, confidence, context status, and escalation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
