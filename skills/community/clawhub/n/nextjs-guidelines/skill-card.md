## Description:

Next.js App Router best practices - Server Components, data fetching, caching, routing, middleware, metadata, error handling, streaming, Server Actions, and performance optimization for Next.js 14-16+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when building, reviewing, migrating, optimizing, or debugging Next.js App Router applications. It provides guidance for Server Components, data fetching, caching, routing, metadata, error handling, streaming, Server Actions, and performance patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may lead an agent to expose session tokens, server-only environment values, or configuration data to clients.

Mitigation: Review generated code for client/server boundaries, keep secrets in server-only code paths, and avoid returning cookie tokens or server-only environment values to client components or public APIs.

Risk: Install and migration examples use mutable remote packages such as latest-tagged installer or codemod commands.

Mitigation: Prefer pinned package versions for installer and codemod commands, and review diffs before applying generated migrations.

Risk: Third-party scripts, analytics, maps, or embedded services can affect user privacy or consent obligations.

Mitigation: Add privacy and consent checks before using analytics, tag-manager, maps, or embedded third-party scripts.

## Reference(s):

- [Skill Page](https://clawhub.ai/wpank/skills/nextjs-guidelines)
- [Async Patterns](references/async-patterns.md)
- [Bundling](references/bundling.md)
- [Data Patterns](references/data-patterns.md)
- [Error Handling](references/error-handling.md)
- [File Conventions](references/file-conventions.md)
- [Font Optimization](references/font-optimization.md)
- [Hydration Errors](references/hydration-errors.md)
- [Image Optimization](references/image-optimization.md)
- [Metadata](references/metadata.md)
- [Parallel Routes](references/parallel-routes.md)
- [Route Handlers](references/route-handlers.md)
- [RSC Boundaries](references/rsc-boundaries.md)
- [Scripts](references/scripts.md)
- [Self Hosting](references/self-hosting.md)
- [Next.js Error Handling Documentation](https://nextjs.org/docs/app/getting-started/error-handling)
- [Next.js Redirect Behavior Documentation](https://nextjs.org/docs/app/api-reference/functions/redirect#behavior)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Next.js implementation patterns, migration commands, configuration snippets, checklists, and debugging guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
