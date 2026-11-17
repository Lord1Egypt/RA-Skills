## Description:

Manage PostHog product analytics from the terminal for analytics, feature flags, experiments, surveys, dashboards, insights, error tracking, logs, HogQL queries, and product health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelsongallardo](https://clawhub.ai/user/nelsongallardo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to have an agent operate phog-cli for PostHog analytics workflows, including product health checks, HogQL queries, and management of flags, experiments, surveys, dashboards, insights, errors, logs, and API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through CLI operations that create, update, or delete PostHog analytics resources.

Mitigation: Use narrowly scoped PostHog credentials, prefer read-only access unless changes are intended, require explicit approval before write or delete commands, and avoid destructive commands with --yes in automated workflows.

Risk: Authentication against an incorrect self-hosted PostHog host could expose credentials.

Mitigation: Verify the PostHog hostname before login and prefer least-privilege API keys supplied through environment variables or an existing authenticated session.

## Reference(s):

- [Complete Command Reference](artifact/references/commands.md)
- [Project Repository](https://github.com/nelsongallardo/posthog-cli)
- [ClawHub Skill Page](https://clawhub.ai/nelsongallardo/skills/phog-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON-producing CLI flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call PostHog APIs and can create, update, or delete analytics resources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
