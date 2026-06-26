## Description: <br>
Dashboard Builder helps an agent scaffold a unified Next.js dashboard for NormieClaw skills with Supabase-backed pages, widgets, migrations, and deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to turn NormieClaw skill manifests into a deployed personal dashboard with shared navigation, skill pages, widgets, database tables, and deployment configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through creating project files, installing packages, generating SQL migrations, and deployment steps. <br>
Mitigation: Run it in a controlled workspace, review generated files and migrations before applying them, and use a test Supabase project first. <br>
Risk: The workflow involves Supabase service-role credentials and database writes. <br>
Mitigation: Keep SUPABASE_SERVICE_ROLE_KEY server-only and out of source control, and prefer least-privilege or backend-mediated writes where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-dashboard-builder) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [Dashboard Builder README](artifact/README.md) <br>
- [Dashboard Builder security guidance](artifact/SECURITY.md) <br>
- [Dashboard architecture specification](artifact/dashboard-kit/ARCHITECTURE-SPEC.md) <br>
- [Supabase dashboard](https://supabase.com/dashboard) <br>
- [Vercel deployment](https://vercel.com/new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash, SQL, TypeScript, TSX, CSS, and JSON templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project scaffolding, dashboard templates, Supabase migration files, and deployment steps for review before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
