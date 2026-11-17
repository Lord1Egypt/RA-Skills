## Description:

Provides read-only GitHub repository browsing for agents, including repository listing, file and README reading, code search, commit and branch inspection, and user-directed downloads to file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to inspect accessible public or connected private GitHub repositories, gather code context, audit files, and download selected files or archives for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected GitHub access may expose private repository metadata or contents to the agent.

Mitigation: Use fine-grained read-only GitHub access, scope repository access to the task, and avoid broad private-repository access unless needed.

Risk: Download actions can place repository files or archives in external file storage and return sensitive signed URLs.

Mitigation: Prefer read actions before download actions, download only necessary paths or refs, and treat returned signed URLs as sensitive.

Risk: Setup commands or remote product schemas may change after the artifact freshness date.

Mitigation: Before production use, refresh the skill or fetch the live schema and instructions through the documented AgentPMT lookup flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/github-repo-browser-read-only)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/github-repo-browser-read-only)
- [Action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions with JSON request examples and file outputs from download actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only repository queries can return text content, metadata, pagination details, or signed storage URLs for downloaded files and archives.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
