## Description:

noCRM.io (nocrm.io). Use this skill for ANY noCRM.io request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

CRM users can use this skill to manage leads and list teams in a connected noCRM.io account through the oo CLI, following the action schemas and confirmation safeguards documented by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI may change other agents’ installed skills during startup, and the skill does not explain that behavior.

Mitigation: Review and verify the installer; set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if automatic skill writes are unwanted.

Risk: Lead write and destructive actions can change or remove CRM data.

Mitigation: Connect only the intended CRM account and retain the documented requirement to confirm the exact payload and effect before write actions, with explicit approval for destructive actions.

## Reference(s):

- [noCRM.io](https://www.nocrm.io)
- [noCRM.io API documentation](https://www.nocrm.io/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [noCRM.io ClawHub release](https://clawhub.ai/oomol/skills/oo-nocrm-io)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector responses, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive CRM actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
