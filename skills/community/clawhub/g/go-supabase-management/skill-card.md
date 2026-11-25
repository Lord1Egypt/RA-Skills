## Description:

Provides Go developers with a typed client for managing Supabase organizations, projects, branches, and project settings through the Supabase Management API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill when building Go code to list or manage Supabase organizations, projects, branches, and project settings with the typed Management API client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Supabase personal access token can carry the user's full rights across organizations.

Mitigation: Store the token in SUPABASE_ACCESS_TOKEN, do not commit or log it, and use an OAuth token with only the scopes needed when possible.

Risk: Write operations can change live Supabase projects.

Mitigation: Run write methods only after the user requests the specific change and confirms the project ref or branch.

## Reference(s):

- [Setup and API usage](references/setup.md)
- [go-supabase-management on pkg.go.dev](https://pkg.go.dev/github.com/psyb0t/go-supabase-management)
- [Project repository](https://github.com/psyb0t/go-supabase-management)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and concise Markdown setup guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples configure Bearer-token authentication and call the Supabase Management API.]

## Skill Version(s):

0.6.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
