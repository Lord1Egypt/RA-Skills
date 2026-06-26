## Description: <br>
Guides agents writing frontend code that uses InsForge or @insforge/sdk for database queries, authentication, file storage, AI features, real-time messaging, edge function calls, and related RLS guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonychang04](https://clawhub.ai/user/tonychang04) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when adding InsForge-backed frontend features, including auth flows, database CRUD, storage, AI calls, real-time subscriptions, and edge function invocation. It also helps reviewers identify when backend-admin setup, RLS policies, or credential-bearing operations need extra approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged backend-admin examples may be applied without sufficient authorization or safeguards. <br>
Mitigation: Require explicit approval, backups, and least-privilege credentials before applying SQL/RLS/SECURITY DEFINER, user deletion, or bulk import examples. <br>
Risk: Admin tokens, API keys, access tokens, or refresh tokens may be exposed in frontend code or logs. <br>
Mitigation: Do not put admin tokens or API keys in frontend code, and do not log access or refresh tokens. <br>
Risk: Incorrect RLS or SECURITY DEFINER changes can weaken data isolation or cause operational failures. <br>
Mitigation: Review generated SQL before applying it, verify policy behavior with non-admin roles, and use least-privilege credentials for backend tasks. <br>


## Reference(s): <br>
- [Insforge ClawHub Skill Page](https://clawhub.ai/tonychang04/insforge) <br>
- [Database SDK Integration](database/sdk-integration.md) <br>
- [Authentication SDK Integration](auth/sdk-integration.md) <br>
- [Storage SDK Integration](storage/sdk-integration.md) <br>
- [Functions SDK Integration](functions/sdk-integration.md) <br>
- [AI SDK Integration](ai/sdk-integration.md) <br>
- [Real-time SDK Integration](realtime/sdk-integration.md) <br>
- [PostgreSQL Row Level Security for InsForge](database/postgres-rls.md) <br>
- [PostgreSQL Row Security Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) <br>
- [PostgreSQL CREATE FUNCTION Documentation](https://www.postgresql.org/docs/current/sql-createfunction.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline JavaScript, SQL, HTTP, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes frontend SDK snippets, backend configuration checks, SQL/RLS examples, common mistakes, and implementation workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
