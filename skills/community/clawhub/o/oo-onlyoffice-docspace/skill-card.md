## Description:

ONLYOFFICE DocSpace (onlyoffice.com). Use this skill for ANY ONLYOFFICE DocSpace request — searching and reading data. Whenever a task involves ONLYOFFICE DocSpace, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search and read information in their connected ONLYOFFICE DocSpace account, including rooms, folders, files, and user records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup instructions run a remote installer directly, and its contents and system changes are unverified.

Mitigation: Review and install the CLI separately from a version-pinned source; require approval before running any fallback installer.

Risk: The connected OOMOL account can access ONLYOFFICE DocSpace data within its granted permissions.

Mitigation: Use read-only credentials and limit the connected account to the DocSpace data needed for the task.

## Reference(s):

- [ONLYOFFICE DocSpace](https://www.onlyoffice.com/docspace.aspx)
- [ONLYOFFICE DocSpace API documentation](https://api.onlyoffice.com/docspace/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Natural-language summaries of DocSpace data, with JSON action responses and shell commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested DocSpace read action and the connected account's access.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
