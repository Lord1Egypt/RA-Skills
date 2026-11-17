## Description:

Manage Microsoft 365 Planner plans, buckets, and tasks via Microsoft Graph API. Use when creating, listing, updating, or deleting Planner resources. Supports group-based plan management, task assignment, progress tracking, and recurring tasks. Requires Azure AD app registration with Group.Read.All and Tasks.ReadWrite.All permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felox63](https://clawhub.ai/user/felox63)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to manage Microsoft 365 Planner plans, buckets, and tasks from an agent workflow through Microsoft Graph. It is intended for creating, listing, assigning, updating, deleting, and cleaning up Planner resources in Microsoft 365 groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup documentation may lead administrators to grant broader Microsoft 365 group-write permissions than the scripts need.

Mitigation: Use Group.Read.All instead of Group.ReadWrite.All unless a separate reviewed use case requires group write access.

Risk: The skill relies on a Microsoft 365 client secret stored in a local environment file.

Mitigation: Store the secret in a dedicated restricted file, keep file permissions tight, and rotate any secret previously used with overbroad permissions.

Risk: Connection-test output may expose tenant, client, secret-suffix, and group details.

Mitigation: Avoid sharing test output and redact operational identifiers before posting logs or support traces.

## Reference(s):

- [Planner API Overview](references/planner-api.md)
- [Setup Guide](references/setup-guide.md)
- [Common Patterns](references/common-patterns.md)
- [Microsoft Graph API Docs](https://docs.microsoft.com/en-us/graph/api/overview)
- [Planner REST API Reference](https://docs.microsoft.com/en-us/graph/api/resources/planner-overview)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance and helper-script usage for Microsoft Graph Planner operations; scripts may print tenant, client, secret-suffix, group, plan, bucket, and task details.]

## Skill Version(s):

1.2.3 (source: frontmatter, package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
