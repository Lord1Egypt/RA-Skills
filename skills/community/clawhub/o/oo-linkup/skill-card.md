## Description:

Linkup (linkup.so). Use this skill for ANY Linkup request — searching and reading data. Whenever a task involves Linkup, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Linkup, retrieve webpages and structured data, and check credits through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloaded code with the agent's local permissions.

Mitigation: Review setup first, use a reviewed and version-pinned CLI, and require approval before running downloaded installers. Review automatic skill synchronization and disable it if unwanted.

Risk: Queries and URLs pass through OOMOL to Linkup.

Mitigation: Do not include secrets in queries or URLs.

## Reference(s):

- [Linkup documentation](https://docs.linkup.so/pages/documentation/get-started/quickstart)
- [Linkup homepage](https://www.linkup.so)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Web search results]

**Output Format:** [Provider responses as text, Markdown, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Linkup action and, for structured searches, the requested schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
