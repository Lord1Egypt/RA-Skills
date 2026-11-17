## Description:

Interface with WordPress sites through the JRB Remote Site API plugin for site administration, content management, plugin and theme management, and Fluent suite integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrbconsulting-joel](https://clawhub.ai/user/jrbconsulting-joel)

### License/Terms of Use:

GPL-2.0-or-later

## Use Case:

Developers and site operators use this skill to let an agent manage WordPress sites that run the JRB Remote Site API plugin, including content CRUD, media handling, plugin and theme operations, and selected Fluent suite workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad WordPress administration and customer-data access.

Mitigation: Install only for sites the user administers, use scoped tokens where possible, and avoid production-impacting operations unless explicitly requested.

Risk: Deletes, plugin or theme changes, campaign actions, and ticket or customer updates can be destructive or sensitive.

Mitigation: Require human confirmation before those operations.

Risk: API tokens can expose administrative site access if leaked.

Mitigation: Keep tokens out of prompts, logs, shell history, and shared transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jrbconsulting-joel/skills/jrb-remote-site-api-skill-repo)
- [JRB Remote Site API WordPress Plugin](https://wordpress.org/plugins/jrb-remote-site-api-for-openclaw/)
- [JRB Remote Site API Plugin Repository](https://github.com/JRBConsulting/jrb-remote-site-api-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose REST API operations against configured WordPress sites and should request confirmation before destructive or production-impacting changes.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
