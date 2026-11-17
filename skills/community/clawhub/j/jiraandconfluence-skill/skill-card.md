## Description:

Automates retrieval and summarization of Jira Cloud issues and Confluence Cloud pages using API tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arkiant](https://clawhub.ai/user/arkiant)

### License/Terms of Use:


## Use Case:

Developers and workflow automation users use this skill to fetch Jira issues and Confluence pages, summarize content, and surface suggested improvements for support, project, and documentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing helper scripts may expose Atlassian API tokens to local process inspection.

Mitigation: Use least-privilege read-only tokens, avoid shared or monitored hosts, and prefer a safer secret-passing mechanism before production use.

Risk: The helper scripts may source an unexpected local auth.sh when run from an untrusted directory.

Mitigation: Run scripts only from a trusted installation path and anchor authentication loading to the script directory before treating the skill as low risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arkiant/skills/jiraandconfluence-skill)
- [Usage examples](examples/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON API output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Atlassian API tokens and a configured Jira or Confluence Cloud domain.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact Version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
