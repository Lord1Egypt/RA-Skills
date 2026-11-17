## Description:

Automate PostHog dashboard creation, sync, update, and export via API. Covers dashboard CRUD, insight creation, cohort management, and API-driven analytics workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics teams use this skill to create, sync, update, and export PostHog dashboards and insights from JSON configuration through the PostHog API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A PostHog personal API key could be sent to an arbitrary configured POSTHOG_HOST.

Mitigation: Set POSTHOG_HOST only to trusted PostHog endpoints or a self-hosted PostHog instance you control.

Risk: The required personal API key has read/write access to the current PostHog project.

Mitigation: Use a least-privilege key where possible and review dashboard and insight changes before running create, sync, or update commands.

Risk: Create mode rewrites the JSON config file in place with the created dashboard_id.

Mitigation: Run against version-controlled or backed-up configuration files.

## Reference(s):

- [PostHog API Docs](https://posthog.com/docs/api)
- [PostHog Personal API Keys](https://posthog.com/docs/api/overview#personal-api-keys)
- [ClawHub Skill Page](https://clawhub.ai/solomonneas/skills/posthog-analytics)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can create, sync, update, and export PostHog dashboards; create mode rewrites the JSON config with the created dashboard_id.]

## Skill Version(s):

1.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
