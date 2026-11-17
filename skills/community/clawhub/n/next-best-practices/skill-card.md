## Description:

Next.js best practices - file conventions, RSC boundaries, data patterns, async APIs, metadata, error handling, route handlers, image/font optimization, bundling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanvidev](https://clawhub.ai/user/tuanvidev)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when writing or reviewing Next.js applications for App Router conventions, React Server Component boundaries, async APIs, metadata, routing, optimization, deployment, and debugging patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may be copied into application code without enough security review.

Mitigation: Require authentication checks, runtime validation, and field allowlists before accepting generated route handlers, server actions, or data access patterns.

Risk: Examples involving analytics or third-party scripts may create privacy or consent issues.

Mitigation: Review analytics and third-party script usage for consent, data minimization, and privacy requirements before deployment.

Risk: Shell examples using npx could fetch unreviewed package versions.

Mitigation: Use pinned, reviewed package versions and run commands in a controlled development environment.

Risk: Generated code or review suggestions may expose secrets or sensitive request data.

Mitigation: Apply secret redaction and avoid logging credentials, cookies, authorization headers, or personal data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tuanvidev/skills/next-best-practices)
- [Next.js Project Structure](https://nextjs.org/docs/app/getting-started/project-structure)
- [Next.js File Conventions](https://nextjs.org/docs/app/api-reference/file-conventions)
- [Next.js Functions API Reference](https://nextjs.org/docs/app/api-reference/functions)
- [Next.js Error Handling](https://nextjs.org/docs/app/getting-started/error-handling)
- [Next.js Package Bundling](https://nextjs.org/docs/app/guides/package-bundling)
- [React use client Directive](https://react.dev/reference/rsc/use-client)
- [React use server Directive](https://react.dev/reference/rsc/use-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JavaScript, configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; agents may apply the guidance and examples to Next.js codebases.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
