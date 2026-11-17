## Description:

Provides guidance for integrating @insforge/sdk into frontend applications for database, authentication, storage, AI, real-time messaging, and serverless function workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonychang04](https://clawhub.ai/user/tonychang04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when adding InsForge-backed frontend features such as CRUD operations, login and OAuth flows, file uploads, AI calls, real-time subscriptions, and function invocation. It also helps agents choose the right InsForge SDK patterns and avoid common integration mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes frontend guidance alongside admin and backend operations.

Mitigation: Use it only for intentional InsForge work, review generated changes carefully, and keep admin tokens and backend-only operations on the server side.

Risk: Examples may expose or mishandle security-sensitive values if copied directly.

Mitigation: Do not copy examples that log tokens, pin the SDK version, and remove placeholder credentials before use.

Risk: Destructive operations and RLS helper functions can affect production data access.

Mitigation: Require explicit confirmation for destructive actions and harden SECURITY DEFINER functions before deployment.

## Reference(s):

- [ClawHub Insforge skill page](https://clawhub.ai/tonychang04/skills/insforge)
- [InsForge SDK skill overview](artifact/SKILL.md)
- [Database SDK integration](artifact/database/sdk-integration.md)
- [Authentication SDK integration](artifact/auth/sdk-integration.md)
- [PostgreSQL RLS guide](artifact/database/postgres-rls.md)
- [PostgreSQL Row Security documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [PostgreSQL CREATE FUNCTION documentation](https://www.postgresql.org/docs/current/sql-createfunction.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript, TypeScript, SQL, HTTP, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
