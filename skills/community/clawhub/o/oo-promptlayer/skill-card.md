## Description:

PromptLayer (promptlayer.com). Use this skill for ANY PromptLayer request — searching and reading data. Whenever a task involves PromptLayer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use the connected PromptLayer workspace to search and read prompt templates, request logs, tables, sheets, and table rows. The skill provides read-only retrieval actions and guidance for operating them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run a downloaded CLI installer and may install agent skills without a clear approval step.

Mitigation: Inspect and verify the installer and installation behavior before running setup, and approve installation separately.

Risk: The connected PromptLayer account's prompts and logs may be accessed through OOMOL.

Mitigation: Connect only the intended PromptLayer account and review what prompts and logs may be accessible through OOMOL.

## Reference(s):

- [PromptLayer homepage](https://promptlayer.com/)
- [PromptLayer API documentation](https://docs.promptlayer.com/reference/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Structured PromptLayer data with Markdown operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval actions for prompt templates, requests, tables, sheets, and rows.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
