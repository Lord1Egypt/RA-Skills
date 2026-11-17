## Description:

Use Lumos to search and read data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to search Lumos access requests and AppStore apps, retrieve individual records, and summarize the returned data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer contents are unverified, and automatic skill synchronization may introduce changes across agent environments.

Mitigation: Use an independently reviewed, version-pinned CLI installation and disable automatic skill synchronization unless updates across environments are intended.

Risk: Lumos requests pass through OOMOL, and a connection may grant more access than needed.

Mitigation: Connect only the Lumos access needed and account for OOMOL handling requests.

## Reference(s):

- [Lumos](https://www.lumos.com/)
- [Lumos API documentation](https://developers.lumos.com/docs/rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with concise natural-language summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Lumos records and search results]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
