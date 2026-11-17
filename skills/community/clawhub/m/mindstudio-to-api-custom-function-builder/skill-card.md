## Description:

Generates complete MindStudio Run Function integrations for external APIs, including JavaScript code, configuration fields, and test data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sol1986](https://clawhub.ai/user/sol1986)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow builders use this skill to create ready-to-paste MindStudio Run Function blocks that call external APIs, expose configuration fields, and store response outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API functions can send credentials, request bodies, and workflow data to external services.

Mitigation: Review every generated URL, header, request body, and output mapping before running the function; use only approved destinations for personal or regulated data.

Risk: API keys placed in query strings may be exposed through logs or request histories.

Mitigation: Prefer header-based authentication when the API supports it, and use scoped, revocable credentials when query-string authentication is unavoidable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sol1986/skills/mindstudio-to-api-custom-function-builder)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with fenced JavaScript code blocks for the Code Tab, Configuration Tab, and Test Data Tab.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated functions should be reviewed for API-specific URL, authentication, request body, and output mapping accuracy before use.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
