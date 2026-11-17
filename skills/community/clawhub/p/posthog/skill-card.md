## Description:

Interact with PostHog analytics via its REST API to capture events, evaluate feature flags, query data with HogQL, and manage persons, insights, dashboards, experiments, surveys, cohorts, annotations, and session recordings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonfunk](https://clawhub.ai/user/simonfunk)

### License/Terms of Use:


## Use Case:

Developers and analytics engineers use this skill to operate PostHog projects from an agent, including event capture, feature flag checks, HogQL queries, and management of common analytics resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses PostHog API keys that can read, write, expose, or change production analytics data.

Mitigation: Use narrowly scoped PostHog API keys and review planned read, update, delete, and HogQL operations before execution.

Risk: Configurable host variables can direct requests away from the intended PostHog environment.

Mitigation: Verify POSTHOG_HOST and POSTHOG_INGEST_HOST point only to official HTTPS PostHog domains or a trusted self-hosted instance.

Risk: Broad HogQL queries can expose more analytics data than intended.

Mitigation: Prefer time-bounded, limited HogQL queries and review query text before running it against sensitive projects.

## Reference(s):

- [PostHog API Endpoint Reference](references/api-endpoints.md)
- [PostHog OpenAPI Schema](https://app.posthog.com/api/schema/)
- [ClawHub Skill Page](https://clawhub.ai/simonfunk/skills/posthog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PostHog API requests through the bundled shell helper when credentials and project settings are provided.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
