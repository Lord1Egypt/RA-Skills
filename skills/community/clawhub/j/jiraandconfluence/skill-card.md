## Description:

CLI tool for interacting with Atlassian Jira and Confluence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[festoinc](https://clawhub.ai/user/festoinc)

### License/Terms of Use:


## Use Case:

Developers, engineers, and operational teams use this skill to manage Jira issues, projects, users, and Confluence pages from an agent-driven command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to globally install an unpinned third-party npm package.

Mitigation: Verify the npm package identity, source repository, publisher, and exact version before installation.

Risk: The CLI can use an Atlassian API token to create, update, transition, comment on, assign, or modify organizational data.

Mitigation: Use a dedicated Atlassian account or token with the narrowest feasible project, space, and write permissions.

Risk: Broad default configuration can allow all commands, projects, or Confluence spaces.

Mitigation: Configure allowed commands, Jira projects, and Confluence spaces before enabling write-capable commands.

Risk: Credential material may be stored in local environment files.

Mitigation: Store environment files securely and rotate Atlassian API tokens regularly.

## Reference(s):

- [jira-ai repository](https://github.com/festoinc/jira-ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue Jira and Confluence read or write operations through the jira-ai CLI when configured with Atlassian credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
