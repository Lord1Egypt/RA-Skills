## Description:

Use this skill to read, create, update, and delete Indeed data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Indeed account can inspect employer jobs and user details, retrieve job records, and update sourced job postings or clear previously applied updates through the oo CLI. The skill requires confirmation before write actions and explicit approval before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup fallback executes remote installers without a separate approval step; installation or synchronization can make persistent changes, including to other agent skills.

Mitigation: Review and install the CLI separately using a pinned, verified release, and inspect its persistent changes before use.

Risk: OOMOL is an intermediary for the connected Indeed account.

Mitigation: Review the account connection and retain the skill's required confirmations for job posting changes.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Indeed API documentation](https://docs.indeed.com/)
- [Indeed](https://www.indeed.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [JSON API responses and concise text summaries, with shell commands for invoking the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include Indeed data and an execution ID; the skill does not handle raw access tokens.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
