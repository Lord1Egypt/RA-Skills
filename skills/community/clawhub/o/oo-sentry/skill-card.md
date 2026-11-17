## Description:

Sentry (sentry.io). Use this skill for ANY Sentry request — reading, creating, updating, and deleting data. Whenever a task involves Sentry, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Sentry users can use this skill to inspect issues, events, projects, releases, alerts, replays, integrations, and Sentry Apps through their connected OOMOL account. It can also update issue attributes when the user has confirmed the change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute changing remote code without a separate approval or integrity check.

Mitigation: Review and approve CLI installation separately, preferably using a fixed, verified release.

Risk: Sentry requests pass through OOMOL, and the remote installers' exact behavior could not be verified in this review.

Mitigation: Review the bundled-skill installation behavior and grant only the Sentry access needed.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Sentry API documentation](https://docs.sentry.io/api/)
- [Sentry](https://sentry.io)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the user's connected Sentry account.]

## Skill Version(s):

1.0.6 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
