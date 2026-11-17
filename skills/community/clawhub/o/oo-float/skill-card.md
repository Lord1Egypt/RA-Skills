## Description:

Float (float.com). Use this skill for ANY Float request — searching and reading data. Whenever a task involves Float, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to search and read Float team data, including accounts, allocations, clients, people, and projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an unpinned remote installer, and its broader local changes are not clearly bounded.

Mitigation: Install a pinned, verified CLI separately, review its bundled agent-skill changes, and connect only the intended Float account.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Float homepage](https://www.float.com/)
- [Float API documentation](https://developer.float.com/api_reference.html)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Float account data and instructions for running supported list actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
