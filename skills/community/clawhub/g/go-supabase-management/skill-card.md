## Description:

Provides a typed Go client for listing and managing Supabase organizations, projects, branches, and project settings through the Supabase Management API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the Go client to list Supabase organizations and projects or manage project settings, branches, and related Management API resources. It does not cover the per-project data API for PostgREST, Auth, or Storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A personal access token may allow changes across the token owner's organizations, and write operations can affect live projects.

Mitigation: Keep tokens private, use an OAuth token with only the required scopes when practical, and make changes only to the intended project or branch.

Risk: The scan was partial and flagged an unresolved local reference, so its evidence is incomplete.

Mitigation: Review the skill and resolve the referenced local material before relying on it.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-supabase-management)
- [Project homepage](https://github.com/psyb0t/go-supabase-management)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.5.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
