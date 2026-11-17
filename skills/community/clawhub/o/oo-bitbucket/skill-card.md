## Description:

Bitbucket (bitbucket.org). Use this skill for ANY Bitbucket request — reading, creating, updating, and deleting data. Whenever a task involves Bitbucket, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage Bitbucket workspaces, repositories, branches, commits, pull requests, pipelines, snippets, and supported issue trackers through an OOMOL-connected account. It provides action guidance and requires confirmation for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool setup directs the agent to run remote CLI installers without a separate approval step, and the installer contents were not verified.

Mitigation: Review the CLI installer separately before enabling automatic setup and prefer a verified, user-managed installation.

Risk: Bitbucket actions can change connected-account data, including destructive operations.

Mitigation: Limit connected-account permissions and retain the skill's approval gates for changes.

## Reference(s):

- [Bitbucket](https://bitbucket.org)
- [Bitbucket Cloud REST API documentation](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Natural-language guidance and oo CLI commands with JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Bitbucket action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
