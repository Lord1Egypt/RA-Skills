## Description:

Provides command-line access to Notion so an agent can search, create, update, and manage pages, databases, blocks, users, and comments with JSON, table, or CSV output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[froemic](https://clawhub.ai/user/froemic)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure and run a Notion CLI for workspace search, content management, database queries, and comment workflows. It is intended for agents that need token-backed Notion operations from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable third-party code globally.

Mitigation: Verify and pin the upstream repository to a trusted commit or release, avoid global npm link when possible, and run the CLI in an isolated environment before use.

Risk: Token-backed commands can modify or delete Notion workspace content.

Mitigation: Grant the Notion integration only the minimum pages and write permissions needed, and manually review create, update, archive, and delete operations before running them on important workspace data.

Risk: Notion API credentials may be exposed through unsafe storage, command arguments, or debug logs.

Mitigation: Store the token in a protected secret mechanism rather than shell startup files, avoid passing it with --api-key, and use debug logging carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/froemic/skills/notion-cli-agent)
- [Notion integration setup](https://www.notion.so/profile/integrations)
- [Notion API base endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI command output may be JSON, table, or CSV depending on the selected Notion CLI format option.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
