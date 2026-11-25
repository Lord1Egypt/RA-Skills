## Description:

Helps developers choose and implement Neon Auth with Managed Better Auth while preserving existing identity providers when appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Neon authentication, implement login flows, and decide when to retain or migrate an existing identity provider.

### Deployment Geography for Use:

Global; Managed Better Auth is available only in AWS regions.

## Known Risks and Mitigations:

Risk: The security scan noted unpinned tools and incomplete coverage because some local references could not be resolved.

Mitigation: Review commands and referenced content before running them, and pin tool versions where reproducibility matters.

## Reference(s):

- [Managed Better Auth: implement login](references/managed-auth.md)
- [Managed Better Auth as the OAuth server](references/oauth-server.md)
- [Self-managed Better Auth](references/self-managed.md)
- [Neon Auth overview](https://neon.com/docs/auth/overview.md)
- [Neon Auth plugin guide](https://neon.com/docs/auth/guides/plugins.md)
- [Neon Auth OAuth provider guide](https://neon.com/docs/auth/guides/plugins/oauth-provider.md)
- [Supabase Auth migration guide](https://neon.com/docs/auth/migrate/from-supabase.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples depend on the application's framework and existing identity provider.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
