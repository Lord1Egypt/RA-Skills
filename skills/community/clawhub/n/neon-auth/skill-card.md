## Description:

Add authentication to new apps with Neon Auth while preserving existing identity providers unless migration is requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to choose an identity provider and implement authentication in Neon-backed applications. It covers login flows, supported OAuth options, and when to retain or migrate an existing provider.

### Deployment Geography for Use:

Global (Managed Auth is available in AWS regions)

## Known Risks and Mitigations:

Risk: Unpinned npx commands and external components can introduce supply-chain changes.

Mitigation: Pin versions after review and inspect generated changes before adopting them.

Risk: The security scan was partial because some referenced paths could not be resolved.

Mitigation: Inspect unresolved referenced paths and their downstream effects before relying on the related guidance.

## Reference(s):

- [Managed Better Auth implementation guide](artifact/references/managed-auth.md)
- [Neon Auth as an OAuth server](artifact/references/oauth-server.md)
- [Self-managed Better Auth guidance](artifact/references/self-managed.md)
- [Neon Auth overview](https://neon.com/docs/auth/overview.md)
- [Neon Auth plugin support](https://neon.com/docs/auth/guides/plugins.md)
- [Supabase Auth migration guide](https://neon.com/docs/auth/migrate/from-supabase.md)
- [Production checklist](https://neon.com/docs/auth/production-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and commands are tailored to the application's framework and identity setup.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
