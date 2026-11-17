## Description:

Convex (convex.dev). Use this skill for ANY Convex request — reading, creating, updating, and deleting data. Whenever a task involves Convex, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Convex projects and deployments, run queries, and manage Convex resources through the connected account. It provides action schemas and requires approval for operations that change or delete data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup involves unverified downloads, and automatic skill synchronization may change installed agent skills without clear disclosure.

Mitigation: Review and approve CLI installation separately, verify the downloaded release, and consider setting OO_SKILLS_SYNC_DISABLED=1 before running oo.

Risk: Convex write and destructive actions can change or remove project data.

Mitigation: Connect only the Convex permissions needed and retain approval for mutations and destructive actions.

## Reference(s):

- [Convex](https://www.convex.dev)
- [Convex HTTP API documentation](https://docs.convex.dev/http-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON results and shell commands with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Convex account and the selected action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
