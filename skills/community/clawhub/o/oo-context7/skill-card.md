## Description:

Context7 (context7.com). Use this skill for ANY Context7 request — searching and reading data. Whenever a task involves Context7, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search for libraries and retrieve relevant documentation and code examples from Context7 through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run remote CLI installers whose system changes have not been verified.

Mitigation: Review setup before enabling the skill; install and verify the CLI yourself or require approval before running either installer.

Risk: Documentation requests use the connected OOMOL account and may incur charges.

Mitigation: Check the connected account's billing terms before making documentation requests.

## Reference(s):

- [Context7](https://context7.com)
- [Context7 API Guide](https://context7.com/docs/api-guide)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md)
- [Context7 ClawHub Release](https://clawhub.ai/oomol/skills/oo-context7)

## Skill Output:

**Output Type(s):** [Text, Code]

**Output Format:** [Documentation excerpts and code snippets, returned as text or structured action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies with the requested library and query.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
