## Description:

Loop Returns (loopreturns.com). Use this skill for ANY Loop Returns request — searching and reading data. Whenever a task involves Loop Returns, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and read Loop Returns destinations, returns, and return details through a connected OOMOL account. It guides agents to inspect each action's schema before submitting a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs unverified remote code, and the CLI may make broader changes to agent skills than this workflow explains.

Mitigation: Review and install a verified CLI release yourself before enabling automatic use, and decide whether to allow bundled-skill synchronization.

Risk: The hosted connector implementation is unverified and mediates access to Loop Returns data.

Mitigation: Connect only the intended Loop Returns account.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Loop Returns](https://www.loopreturns.com)
- [Loop Returns API documentation](https://docs.loopreturns.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request payloads and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads return and destination data; requires an installed, signed-in oo CLI and a connected Loop Returns account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
