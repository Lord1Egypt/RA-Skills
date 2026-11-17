## Description:

JSON验证工具 uses the Expanso Edge pipeline to validate JSON syntax and structure, including large-dataset streaming and multi-source association workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprise teams, and automation workflow builders use this skill to validate JSON syntax and structure during API integration, platform connection, webhook configuration, and data synchronization work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad command, file, API, and credential-related authority for a loosely defined JSON validation workflow.

Mitigation: Review the skill before installation and use only non-sensitive JSON until the publisher clarifies the Expanso Edge service, exact API endpoint, data handling, command allowlists, file write locations, and confirmation requirements.

Risk: External calls or command execution could expose input data if the service endpoint and execution boundaries are not clear.

Mitigation: Require explicit user confirmation before external calls or command execution and avoid secrets, credentials, and sensitive payloads in validation inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/json-validator)
- [Publisher Profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce validation results, execution logs, configuration guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
