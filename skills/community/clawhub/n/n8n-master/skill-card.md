## Description:

Answers n8n questions and builds n8n workflows, node configurations, Code node JavaScript, HTTP Request setups, API integrations, toolbox-assisted API tests, and importable workflow JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to answer n8n questions, design and debug workflows, generate node configurations and Code node JavaScript, and draft importable workflow JSON with production hardening guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional toolbox actions can send API credentials to arbitrary network destinations or query internal network services if misused.

Mitigation: Run toolbox tests only against verified endpoints and base URLs, and avoid arbitrary test URLs from untrusted prompts.

Risk: Feishu or Firecrawl credentials may be exposed if they are used with an untrusted endpoint.

Mitigation: Keep credentials out of generated outputs and rotate any Feishu or Firecrawl credentials that were used with an untrusted destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billzhuang6569/skills/n8n-master)
- [n8n documentation](https://docs.n8n.io/)
- [n8n HTTP Request node documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [HTTP Request node output template](references/templates/http-node-output.md)
- [Code node output template](references/templates/code-node-output.md)
- [Workflow JSON output template](references/templates/workflow-json-output.md)
- [API tester toolbox reference](references/toolbox/api-tester.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, configuration details, shell commands, and JSON workflow definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflow JSON should remain inactive and use placeholder credential names.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
