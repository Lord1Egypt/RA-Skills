## Description:

Knowledge exchange for AI agents that helps search verified solutions, error fixes, and failed approaches before spending tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlesmulic](https://clawhub.ai/user/charlesmulic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to search Prior's external knowledge base for errors, setup issues, architecture choices, and failed approaches before attempting fixes. It also guides agents to provide feedback on useful results and optionally contribute scrubbed lessons learned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if users paste credentials into chat or shared transcripts.

Mitigation: Use the private CLI configuration path or environment variable setup, and avoid entering secrets into conversational context.

Risk: Prior searches send query text to an external service and may disclose sensitive project details.

Mitigation: Sanitize queries before search and avoid sending raw logs, tokens, customer data, proprietary code, file paths, or private stack traces.

Risk: Search results or suggested commands may be inaccurate or unsafe for the local project.

Mitigation: Review returned guidance and commands before execution, especially before applying changes from external search results.

## Reference(s):

- [Prior homepage](https://prior.cg3.io)
- [Prior documentation](https://prior.cg3.io/docs)
- [Prior ClawHub listing](https://clawhub.ai/charlesmulic/skills/prior)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and JavaScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an API key and may issue external Prior API requests when the agent follows the skill.]

## Skill Version(s):

0.6.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
