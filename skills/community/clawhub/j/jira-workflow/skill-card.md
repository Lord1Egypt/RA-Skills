## Description:

Integrates Jira Cloud project management workflows so an agent can search, create, update, transition, and comment on issues, plus inspect projects and boards through MorphixAI-mediated Jira access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Developers, project managers, and support teams use this skill to manage Jira Cloud issues and common Jira workflows from an agent session. It is useful for issue lookup, triage, creation, status transitions, comments, and daily work planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an unpinned third-party MorphixAI plugin and proxy access that may read or change live Jira data without clear scope controls.

Mitigation: Review before installing, verify or pin the MorphixAI plugin version where possible, and use a dedicated Jira account limited to the needed projects.

Risk: Jira create, update, comment, and transition actions can modify production project records.

Mitigation: Confirm every create, update, comment, and transition action before running it.

Risk: Compromise or overuse of the MorphixAI API key or Jira connection could expose Jira access.

Mitigation: Know how to rotate or revoke the MorphixAI API key and Jira connection, and revoke them when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paul-leo/skills/jira-workflow)
- [MorphixAI API Keys](https://morphix.app/api-keys)
- [MorphixAI Connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML-style Jira tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Jira account before Jira actions can run.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
