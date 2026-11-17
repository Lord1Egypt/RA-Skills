## Description:

MantisBT Manager helps agents manage Mantis Bug Tracker issues, projects, users, filters, configurations, and related resources through the official REST API with context-aware instance and token selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willykinfoussia](https://clawhub.ai/user/willykinfoussia)

### License/Terms of Use:


## Use Case:

Developers, administrators, and support teams use this skill to inspect and change MantisBT issues, projects, users, tokens, filters, configuration, and related records across one or more Mantis instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be sent to user-selected Mantis base URLs when temporary or session overrides are used.

Mitigation: Install only for trusted Mantis endpoints, keep tokens instance-specific, and require the matching token whenever changing the base URL.

Risk: The skill documents powerful data-changing and administrative actions, including deletes, password resets, token management, configuration changes, and impersonation.

Mitigation: Use least-privilege tokens and require explicit confirmation before destructive, privileged, or admin-level actions.

Risk: Token-derived values or connection context could be exposed while showing current configuration.

Mitigation: Mask tokens in user-facing output and avoid logging or displaying full token values.

## Reference(s):

- [MantisBT Homepage](https://www.mantisbt.org/)
- [MantisBT Documentation](https://mantisbt.org/documentation.php)
- [MantisBT GitHub Repository](https://github.com/mantisbt/mantisbt)
- [ClawHub Skill Page](https://clawhub.ai/willykinfoussia/skills/mantis-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST endpoint examples, JSON request bodies, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MANTIS_BASE_URL and MANTIS_API_TOKEN, with documented temporary and session-level overrides for multi-instance use.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
