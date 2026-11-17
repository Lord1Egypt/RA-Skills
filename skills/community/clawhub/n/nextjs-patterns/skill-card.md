## Description:

Apply Next.js 15 best practices and modern patterns for App Router, Server Components, Server Actions, caching, performance, routing, and migration work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building, reviewing, or migrating Next.js 15 applications so agents can suggest idiomatic App Router structure, caching choices, Server Component boundaries, Server Actions, route handlers, metadata, and performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration guidance includes mutable canary/latest package commands that may execute external code or change behavior over time.

Mitigation: Pin and review versions of Next.js, React, React DOM, and @next/codemod; run codemods in a clean branch or disposable environment; inspect generated changes before merging.

Risk: Generated Next.js code or configuration may not match an application's runtime, caching, authentication, or deployment requirements.

Mitigation: Treat outputs as implementation guidance, then run the project's tests, build, linting, and security review before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goldath/skills/nextjs-patterns)
- [Next.js 15 Caching Deep Dive](artifact/references/caching-guide.md)
- [Next.js 15 Migration & Configuration Guide](artifact/references/migration-config.md)
- [Next.js 15 Routing Patterns](artifact/references/routing-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before applying generated code or commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
