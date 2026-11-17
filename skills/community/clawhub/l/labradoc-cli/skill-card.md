## Description:

Use the Labradoc CLI to authenticate and call Labradoc API endpoints for tasks, files, users, API keys, email, Google and Microsoft integrations, and billing from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zamedic](https://clawhub.ai/user/zamedic)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run Labradoc CLI commands for authenticated document, task, user, email, integration, API-key, and billing operations from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Labradoc account tokens and sensitive document or email data.

Mitigation: Install only when the publisher is trusted, prefer narrowly scoped API tokens, avoid command-line secret exposure, and do not ask the agent to print raw tokens.

Risk: The skill can propose state-changing Labradoc operations such as archive, revoke, upload, webhook, checkout, and API-key commands.

Mitigation: Review state-changing commands and target account context before execution, and keep API and authentication URLs on the documented HTTPS defaults unless a trusted override is required.

## Reference(s):

- [Labradoc CLI skill reference](references/labradoc-cli.md)
- [Labradoc CLI integrations](references/integrations.md)
- [Labradoc CLI GitHub releases](https://github.com/zamedic/labradoc-cli/releases)
- [Labradoc profile](https://labradoc.eu/profile)
- [ClawHub skill page](https://clawhub.ai/zamedic/skills/labradoc-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-supplied API request bodies, file paths, and Labradoc CLI commands that call external service endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
