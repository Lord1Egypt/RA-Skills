## Description:

Automates Next.js, Supabase, and Vercel project setup by scaffolding files, generating SQL migration guidance, and invoking local development or deployment commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[studio-hakke](https://clawhub.ai/user/studio-hakke)

### License/Terms of Use:


## Use Case:

Developers use this skill to create and configure a Next.js application with Supabase database, authentication, storage, and Vercel deployment workflows. It is suited for fast project setup, prototyping, and guided deployment preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs project setup, deployment preparation, SQL generation, and credential-dependent workflows that are too powerful for automatic trust.

Mitigation: Review before installing or running, and use it only in a disposable or constrained project environment.

Risk: Generated SQL can affect Supabase database, authentication, storage, and row-level security behavior.

Mitigation: Inspect generated SQL before running it in Supabase and apply changes manually with the least privileges needed.

Risk: Untrusted project names, ports, migration names, or bucket names may influence generated files or shell commands.

Mitigation: Avoid untrusted inputs and review generated commands and files before execution.

Risk: A Supabase service-role key can grant broad server-side access if placed in the generated environment file.

Mitigation: Do not add a real service-role key unless a specific server-only operation requires it, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/studio-hakke/skills/next-supabase-vercel-bundle)
- [Supabase API Settings](https://supabase.com/dashboard/project/_/settings/api)
- [Supabase SQL Editor](https://supabase.com/dashboard/project/_/sql/new)
- [Supabase Auth Providers](https://supabase.com/dashboard/project/_/auth/providers)
- [Supabase Storage Buckets](https://supabase.com/dashboard/project/_/storage/buckets)
- [Supabase Storage Policies](https://supabase.com/dashboard/project/_/storage/policies)
- [Vercel Dashboard](https://vercel.com/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated project files, and SQL migration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local project files and invoke npm, npx, git, Supabase, and Vercel CLI workflows.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
