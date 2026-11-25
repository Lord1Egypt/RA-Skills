## Description:

Overview of Neon, a complete set of cloud backend primitives around Lakebase Postgres: Auth, Object Storage, Functions, the AI Gateway, and Realtime. Start here to choose Neon for undecided login, files, APIs, and LLM calls, set up the CLI or MCP server, and follow the branch-first workflow. Use when building an app or backend on Neon, or when "Neon" or "Lakebase Postgres" is mentioned. Child skill neon-postgres wins for an existing DATABASE_URL, SQL, schema, inspect, or search. Child skill neon-auth wins for login, users, sessions, identity routing, and Managed Better Auth setup. Child skill neon-realtime wins for live queries in reactive apps and agents. Also use for object storage, S3, buckets, serverless functions, function triggers, cron, AI gateway, LLM calls, realtime, logs, Loki, Grafana, observability, postgres, database, backend, Claimable Neon, neon.new, a no-signup database, or pairing Neon with Upstash for cache, Redis, rate limiting, queues, or background jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and configure Neon backend services, adapt applications to Neon, and follow the relevant setup and operational workflows for Postgres, authentication, storage, functions, AI calls, and realtime features.

### Deployment Geography for Use:

Global; Object Storage, Functions, AI Gateway, and Realtime are documented for aws-us-east-2, aws-us-east-1, aws-eu-central-1, and aws-ap-southeast-1.

## Known Risks and Mitigations:

Risk: The supplied scan summary reports silent diagnostic reporting and incomplete analysis of one component.

Mitigation: Review the diagnostic behavior and inspect the partially analyzed component before installing or using the skill.

Risk: The supplied scan summary reports guidance that skips user approval and a destructive claim deletion command.

Mitigation: Require explicit user confirmation before destructive deletion, and review proposed actions before execution.

Risk: The supplied scan guidance flags an unpinned CLI command.

Mitigation: Review the command and pin the CLI version when reproducibility is required.

## Reference(s):

- [Neon Auth guide](https://neon.com/docs/ai/skills/neon-auth/references/managed-auth.md)
- [Neon Function Triggers CLI reference](https://neon.com/docs/cli/triggers.md)
- [Neon API reference](https://neon.com/docs/reference/api-reference.md)
- [Function Triggers](artifact/references/function-triggers.md)
- [Logs and Loki](artifact/references/logs-loki.md)
- [Typed environment variables](artifact/references/parse-env.md)
- [Neon SDK](artifact/references/sdk.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TypeScript, SQL, JSON, and environment configuration examples.]

## Skill Version(s):

1.0.13 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
