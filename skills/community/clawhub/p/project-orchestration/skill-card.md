## Description:

Complete project orchestration: model routing, coding workflow, scripts, session logging, decision tracking, price checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to organize AI-assisted projects, choose model routes, scaffold planning files, log sessions and decisions, monitor model pricing, and resume work across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose local orchestration data over the network without authentication.

Mitigation: Run the dashboard only on trusted networks, or change it to bind to 127.0.0.1, remove wildcard CORS, and require authentication or a token before use.

Risk: Generated planning and session files may persist sensitive project context, prompts, model/provider details, prices, or copied notes.

Mitigation: Keep the orchestration data directory private and avoid storing secrets, API keys, database URLs, confidential prompts, or sensitive customer data in generated records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/genortg/skills/project-orchestration)
- [Package Homepage](https://clawhub.com/packages/project-orchestration)
- [README](README.md)
- [Model Routing Table Template](ROUTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated JSON or Markdown project records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, and python3; stores project, session, model, and price records in a local orchestration data directory.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
