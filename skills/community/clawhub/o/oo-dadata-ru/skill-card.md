## Description:

DaData.ru (dadata.ru). Use this skill for ANY DaData.ru request — searching and reading data. Whenever a task involves DaData.ru, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistants use this skill to search DaData.ru for Russian addresses, banks, email addresses, full names, and organizations or individual entrepreneurs through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback downloads and executes installer code whose contents were not verified in the supplied evidence.

Mitigation: Install the CLI separately from a verified release before use, and review its documented skill synchronization controls before running it.

Risk: Search queries are sent to OOMOL and DaData, and may contain sensitive information.

Mitigation: Send only query information that the user intends those services to receive.

## Reference(s):

- [DaData API documentation](https://dadata.ru/api/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance, Shell commands]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search suggestions for Russian addresses, banks, email addresses, names, and organizations.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
