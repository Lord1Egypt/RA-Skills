## Description:

Dashboard Builder helps an agent scaffold, configure, and deploy a unified Next.js dashboard for NormieClaw skills with Supabase-backed pages, widgets, and migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-tool builders use Dashboard Builder to create a unified dark-mode dashboard that reads NormieClaw skill manifests, generates app pages and database migrations, and prepares deployment to Vercel or Docker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Giving an agent SUPABASE_SERVICE_ROLE_KEY can grant broad database authority and bypass normal row-level access controls.

Mitigation: Prefer a webhook or narrow ingestion endpoint, keep service-role credentials only in server-side environment variables, and avoid exposing them to generated client code.

Risk: Mutable setup commands and dependency installs can change behavior between runs.

Mitigation: Pin npm and Supabase CLI versions, review lockfile changes, and run dependency security checks before deployment.

Risk: Generated migrations can create tables that are not fully protected by row-level security policies.

Mitigation: Run migrations in dry-run or review mode first, then verify every generated table has complete RLS policies before pushing to a real Supabase project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-dashboard-builder)
- [README.md](README.md)
- [SECURITY.md](SECURITY.md)
- [First-Run Setup](SETUP-PROMPT.md)
- [Architecture Specification](dashboard-kit/ARCHITECTURE-SPEC.md)
- [Supabase Dashboard](https://supabase.com/dashboard)
- [Vercel New Project](https://vercel.com/new)
- [NormieClaw](https://normieclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript/TSX code, SQL migrations, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate project files, Supabase migrations, dashboard routes, registry entries, and deployment instructions for the user's selected skills.]

## Skill Version(s):

1.0.3 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
