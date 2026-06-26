## Description: <br>
Orchestrates the full-stack Next.js, Supabase, and Vercel development cycle by scaffolding projects, generating executable SQL migrations, guiding configuration, and supporting Vercel deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[studio-hakke](https://clawhub.ai/user/studio-hakke) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to create and configure a Next.js application with Supabase database, authentication, storage, and Vercel deployment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local scaffolding, package installation, build, and Vercel deployment commands from the current project context. <br>
Mitigation: Run it only in a trusted project directory and verify the active Vercel account and linked project before deployment. <br>
Risk: Weak input validation around project names and command arguments could lead to unintended local command behavior. <br>
Mitigation: Use simple project names and numeric ports, and review generated commands or files before committing or deploying. <br>
Risk: Supabase service role keys are high privilege and may be exposed if copied into logs, screenshots, client code, or a repository. <br>
Mitigation: Keep SUPABASE_SERVICE_KEY server-only, avoid committing environment files, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/studio-hakke/next-supabase-vercel-bundle) <br>
- [Publisher profile](https://clawhub.ai/user/studio-hakke) <br>
- [Supabase SQL editor](https://supabase.com/dashboard/project/_/sql/new) <br>
- [Supabase API settings](https://supabase.com/dashboard/project/_/settings/api) <br>
- [Vercel dashboard](https://vercel.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated project files, SQL migrations, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local project files, run npm and Vercel commands, and print setup or deployment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
