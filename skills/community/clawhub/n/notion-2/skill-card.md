## Description:

Integrates Notion so agents can search pages and databases, create, update, and archive pages, read or append block content, and query databases through the MorphixAI proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to connect an agent to a Notion workspace for knowledge-base search, page management, content updates, and project database workflows. Access is limited to Notion pages and databases explicitly shared with the integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, append to, and archive content in shared Notion workspaces through an external plugin and API key.

Mitigation: Install only a trusted MorphixAI/OpenClaw plugin source, use a revocable MORPHIXAI_API_KEY, and approve write or archive actions deliberately.

Risk: The agent may read or modify any Notion pages or databases shared with the integration.

Mitigation: Share only the pages and databases the agent truly needs, and review shared Notion access before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paul-leo/skills/notion-2)
- [MorphixAI API Keys](https://morphix.app/api-keys)
- [MorphixAI Connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with shell commands and YAML-like tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY, the OpenClaw MorphixAI plugin, a linked Notion account, and explicitly shared Notion pages or databases.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
