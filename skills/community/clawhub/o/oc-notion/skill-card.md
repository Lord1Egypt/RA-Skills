## Description:

Notion CLI/API for pages, Markdown content, data sources, files, comments, search, Workers, and raw API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Notion workspace content through the Notion CLI or API, including pages, data sources, files, comments, search, and Workers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless authentication uses a Notion API token.

Mitigation: Keep the token in a protected environment variable or secret store, and do not expose it in prompts or logs.

Risk: CLI/API examples include operations that can change or remove workspace content.

Mitigation: Check the selected workspace, IDs, and request body before running write or trash commands.

## Reference(s):

- [Notion CLI documentation](https://developers.notion.com/cli/get-started/overview)
- [ClawHub Notion skill release](https://clawhub.ai/hillstreet-ph/skills/oc-notion)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions, Markdown content]

**Output Format:** [Markdown guidance with inline shell commands and Notion API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or change workspace content; Workers may require an eligible plan and workspace enablement.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
