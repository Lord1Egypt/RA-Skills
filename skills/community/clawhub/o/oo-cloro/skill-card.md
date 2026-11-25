## Description:

Cloro (cloro.dev). Use this skill for ANY Cloro request — reading, creating, updating, and deleting data. Whenever a task involves Cloro, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use Cloro through the user's connected OOMOL account to retrieve search and monitoring results, check task and queue status, inspect credits, and submit monitoring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a suspicious instruction to run a remote oo CLI installer that is not clearly related to the stated Cloro data tasks; scan coverage is partial because two local path-like references could not be resolved.

Mitigation: Review the setup instructions, assess whether the oo CLI is needed and whether the OOMOL installer is trusted, and account for the incomplete scan before installing or running the installer.

## Reference(s):

- [Cloro homepage](https://cloro.dev)
- [Cloro API documentation](https://cloro.dev/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Text, Shell commands]

**Output Format:** [JSON action responses and concise text summaries, with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output varies by action; task submissions may return asynchronous task identifiers and require a later status or result lookup.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
